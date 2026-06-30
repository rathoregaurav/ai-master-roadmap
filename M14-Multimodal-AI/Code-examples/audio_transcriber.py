"""
M14: Audio Transcriber & Analyzer
=================================
Transcribe audio with Whisper, then analyze with LLM.

Key skills:
- Speech-to-Text with OpenAI Whisper API
- Processing local audio files
- Combining STT + LLM for analysis
- Handling different audio formats
- Timestamp extraction for long audio
"""

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Optional

import httpx
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 1. Data Models
# ──────────────────────────────────────────────

class TranscriptionResult(BaseModel):
    """Output from Whisper transcription."""
    text: str = Field(..., description="Full transcribed text")
    segments: list[dict] = Field(default_factory=list, description="Timestamped segments")
    duration_seconds: float = Field(0.0, description="Audio duration")
    language: str = Field("en", description="Detected language")


class MeetingSummary(BaseModel):
    """Structured summary of transcribed meeting."""
    title: str = Field(..., description="Suggested meeting title")
    date_or_context: Optional[str] = Field(None, description="Date or context clues")
    attendees_mentioned: list[str] = Field(default_factory=list)
    key_topics: list[str] = Field(..., description="Main topics discussed")
    decisions: list[str] = Field(default_factory=list, description="Decisions made")
    action_items: list[dict] = Field(
        default_factory=list,
        description="Action items with assignee if mentioned",
    )
    next_steps: list[str] = Field(default_factory=list)


class SentimentAnalysis(BaseModel):
    """Sentiment analysis per segment."""
    overall_sentiment: str = Field(..., description="positive/negative/neutral")
    score: float = Field(..., ge=0.0, le=1.0, description="Confidence score")
    key_emotional_moments: list[dict] = Field(default_factory=list)


# ──────────────────────────────────────────────
# 2. Transcription Client
# ──────────────────────────────────────────────

class AudioTranscriber:
    """Transcribe audio using OpenAI Whisper API."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.Client(timeout=300.0)  # Long timeout for audio

    def transcribe(
        self,
        audio_path: str,
        language: Optional[str] = None,
        response_format: str = "verbose_json",
    ) -> TranscriptionResult:
        """
        Transcribe audio file using Whisper API.
        
        Args:
            audio_path: Path to audio file (mp3, wav, m4a, etc.)
            language: Optional language code (e.g., "en", "es")
            response_format: "json" or "verbose_json"
        """
        path = Path(audio_path)
        if not path.exists():
            raise FileNotFoundError(f"Audio file not found: {audio_path}")

        file_size_mb = path.stat().st_size / (1024 * 1024)
        logger.info(f"Processing audio: {path.name} ({file_size_mb:.1f} MB)")

        with open(path, "rb") as f:
            files = {"file": (path.name, f, self._get_mime_type(path))}
            data = {
                "model": "whisper-1",
                "response_format": response_format,
            }
            if language:
                data["language"] = language

            try:
                response = self.client.post(
                    "https://api.openai.com/v1/audio/transcriptions",
                    files=files,
                    data=data,
                    headers={"Authorization": f"Bearer {self.api_key}"},
                )
                response.raise_for_status()
                result = response.json()

                if response_format == "verbose_json":
                    return TranscriptionResult(
                        text=result.get("text", ""),
                        segments=result.get("segments", []),
                        duration_seconds=result.get("duration", 0.0),
                        language=result.get("language", "en"),
                    )
                else:
                    return TranscriptionResult(text=result.get("text", ""))

            except httpx.HTTPStatusError as e:
                logger.error(f"Whisper API Error {e.response.status_code}: {e.response.text}")
                raise
            except Exception as e:
                logger.error(f"Transcription failed: {e}")
                raise

    def _get_mime_type(self, path: Path) -> str:
        """Map file extension to MIME type."""
        ext = path.suffix.lower()
        mime_map = {
            ".mp3": "audio/mpeg",
            ".wav": "audio/wav",
            ".m4a": "audio/mp4",
            ".ogg": "audio/ogg",
            ".flac": "audio/flac",
            ".webm": "audio/webm",
        }
        return mime_map.get(ext, "audio/mpeg")

    def close(self):
        self.client.close()


# ──────────────────────────────────────────────
# 3. Meeting Analysis with LLM
# ──────────────────────────────────────────────

class MeetingAnalyzer:
    """Analyze transcribed meeting content with LLM."""

    def __init__(self, api_key: str):
        self.api_key = api_key
        self.client = httpx.Client(timeout=60.0)

    def summarize(self, transcription: TranscriptionResult) -> MeetingSummary:
        """Generate structured meeting summary from transcription."""
        prompt = f"""
        Analyze this meeting transcription and extract structured information.
        
        Transcription:
        {transcription.text[:8000]}  # Truncate for token limits
        
        Return JSON with: title, date_or_context, attendees_mentioned, 
        key_topics, decisions, action_items (each with task and assignee), next_steps.
        """

        try:
            response = self.client.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You extract structured data from meeting transcripts."},
                        {"role": "user", "content": prompt},
                    ],
                    "response_format": {"type": "json_object"},
                    "max_tokens": 1500,
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()
            parsed = json.loads(data["choices"][0]["message"]["content"])
            return MeetingSummary(**parsed)

        except Exception as e:
            logger.error(f"Meeting analysis failed: {e}")
            raise

    def analyze_sentiment(self, transcription: TranscriptionResult) -> SentimentAnalysis:
        """Analyze sentiment throughout the meeting."""
        segments_text = "\n".join(
            f"[{s.get('start', 0):.1f}s - {s.get('end', 0):.1f}s] {s.get('text', '')}"
            for s in transcription.segments[:30]  # Limit segments
        )

        prompt = f"""
        Analyze the sentiment of this meeting transcript.
        
        Transcript segments:
        {segments_text}
        
        Return JSON with: overall_sentiment (positive/negative/neutral), 
        score (0.0 to 1.0), key_emotional_moments (list of objects with segment, sentiment, reason fields).
        """

        try:
            response = self.client.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You analyze sentiment in conversations."},
                        {"role": "user", "content": prompt},
                    ],
                    "response_format": {"type": "json_object"},
                    "max_tokens": 1000,
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()
            parsed = json.loads(data["choices"][0]["message"]["content"])
            return SentimentAnalysis(**parsed)

        except Exception as e:
            logger.error(f"Sentiment analysis failed: {e}")
            raise

    def close(self):
        self.client.close()


# ──────────────────────────────────────────────
# 4. End-to-End Pipeline
# ──────────────────────────────────────────────

def process_meeting_recording(
    audio_path: str,
    openai_api_key: str,
) -> dict:
    """
    Complete pipeline: transcribe → summarize → analyze sentiment.
    
    Returns dict with all results.
    """
    transcriber = AudioTranscriber(api_key=openai_api_key)
    analyzer = MeetingAnalyzer(api_key=openai_api_key)

    try:
        # Step 1: Transcribe
        logger.info("Step 1: Transcribing audio...")
        transcription = transcriber.transcribe(audio_path)
        logger.info(f"Transcribed {len(transcription.text)} characters")

        # Step 2: Summarize
        logger.info("Step 2: Generating meeting summary...")
        summary = analyzer.summarize(transcription)

        # Step 3: Sentiment
        logger.info("Step 3: Analyzing sentiment...")
        sentiment = analyzer.analyze_sentiment(transcription)

        return {
            "transcription": transcription.model_dump(),
            "summary": summary.model_dump(),
            "sentiment": sentiment.model_dump(),
        }

    finally:
        transcriber.close()
        analyzer.close()


# ──────────────────────────────────────────────
# 5. Demo
# ──────────────────────────────────────────────

def demo():
    """Run demo if API key is available."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("No OPENAI_API_KEY set. Skipping demo.")
        logger.info("To run: export OPENAI_API_KEY='your-key'")
        logger.info("Then: python audio_transcriber.py --file meeting.mp3")
        return

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", required=True, help="Path to audio file")
    parser.add_argument("--language", default=None, help="Language code (e.g., 'en')")
    args = parser.parse_args()

    result = process_meeting_recording(args.file, api_key)
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    demo()