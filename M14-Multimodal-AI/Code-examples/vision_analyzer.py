"""
M14: Vision Analyzer
====================
Call GPT-4o / Claude 3.5 Vision with images for analysis.

Key skills:
- Building multimodal message payloads
- Handling image URLs and base64-encoded images
- Extracting structured data from visual content
- Error handling for large/invalid images
"""

import base64
import json
import logging
from pathlib import Path
from typing import Optional
from io import BytesIO

import httpx
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 1. Structured Output Schema
# ──────────────────────────────────────────────

class ImageAnalysis(BaseModel):
    """Structured output from vision model."""
    description: str = Field(..., description="General description of the image")
    objects_detected: list[str] = Field(default_factory=list, description="Objects or elements visible")
    text_found: Optional[str] = Field(None, description="Any text visible in the image")
    tables_or_charts: bool = Field(False, description="Whether image contains tables or charts")
    sentiment_or_tone: Optional[str] = Field(None, description="Overall tone if applicable")
    confidence_issues: list[str] = Field(default_factory=list, description="Areas of uncertainty")


# ──────────────────────────────────────────────
# 2. Image Encoding Utilities
# ──────────────────────────────────────────────

def encode_image_to_base64(image_path: str) -> str:
    """Read an image file and return base64-encoded string."""
    path = Path(image_path)
    if not path.exists():
        raise FileNotFoundError(f"Image not found: {image_path}")
    
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def get_image_media_type(image_path: str) -> str:
    """Determine media type from file extension."""
    ext = Path(image_path).suffix.lower()
    media_types = {
        ".png": "image/png",
        ".jpg": "image/jpeg",
        ".jpeg": "image/jpeg",
        ".gif": "image/gif",
        ".webp": "image/webp",
    }
    return media_types.get(ext, "image/png")


# ──────────────────────────────────────────────
# 3. Vision API Client
# ──────────────────────────────────────────────

class VisionClient:
    """Client for multimodal LLM API calls."""

    def __init__(
        self,
        api_key: str,
        model: str = "gpt-4o",
        base_url: str = "https://api.openai.com/v1",
    ):
        self.api_key = api_key
        self.model = model
        self.base_url = base_url
        self.client = httpx.Client(timeout=60.0)

    def analyze_image_url(
        self,
        image_url: str,
        prompt: str = "Describe this image in detail.",
    ) -> ImageAnalysis:
        """Analyze an image accessible via URL."""
        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": image_url, "detail": "auto"},
                    },
                ],
            }
        ]
        return self._call_vision_api(messages)

    def analyze_image_file(
        self,
        image_path: str,
        prompt: str = "Describe this image in detail.",
    ) -> ImageAnalysis:
        """Analyze a local image file (base64-encoded)."""
        b64 = encode_image_to_base64(image_path)
        media_type = get_image_media_type(image_path)
        data_uri = f"data:{media_type};base64,{b64}"

        messages = [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": data_uri, "detail": "high"},
                    },
                ],
            }
        ]
        return self._call_vision_api(messages)

    def analyze_multiple_images(
        self,
        image_paths: list[str],
        prompt: str = "Compare these images and describe the differences.",
    ) -> ImageAnalysis:
        """Analyze multiple images in one request."""
        content = [{"type": "text", "text": prompt}]
        for path in image_paths:
            b64 = encode_image_to_base64(path)
            media_type = get_image_media_type(path)
            data_uri = f"data:{media_type};base64,{b64}"
            content.append({
                "type": "image_url",
                "image_url": {"url": data_uri, "detail": "high"},
            })

        messages = [{"role": "user", "content": content}]
        return self._call_vision_api(messages)

    def _call_vision_api(self, messages: list) -> ImageAnalysis:
        """Raw API call with structured output parsing."""
        try:
            response = self.client.post(
                f"{self.base_url}/chat/completions",
                json={
                    "model": self.model,
                    "messages": messages,
                    "max_tokens": 1024,
                    "response_format": {"type": "json_object"},
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()
            content = data["choices"][0]["message"]["content"]
            
            # Parse structured output
            parsed = json.loads(content)
            return ImageAnalysis(**parsed)

        except httpx.HTTPStatusError as e:
            logger.error(f"API Error {e.response.status_code}: {e.response.text}")
            raise
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            raise


# ──────────────────────────────────────────────
# 4. Document-Specific Analysis
# ──────────────────────────────────────────────

def analyze_invoice_or_form(image_path: str, client: VisionClient) -> dict:
    """Specialized analysis for business documents."""
    prompt = """
    Extract the following from this document image:
    1. Document type (invoice, form, receipt, letter)
    2. Key fields: date, total amount, vendor name, customer name
    3. All visible text in a structured format
    4. Table data if present (rows and columns)
    5. Any signatures or stamps
    
    Return as JSON with these exact keys:
    document_type, date, total_amount, vendor, customer, extracted_text, table_data, signatures
    """
    return client.analyze_image_file(image_path, prompt=prompt)


# ──────────────────────────────────────────────
# 5. Demo / Example Usage
# ──────────────────────────────────────────────

def demo():
    """Run a demo if API key is available."""
    import os
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("No OPENAI_API_KEY set. Skipping demo.")
        logger.info("To run: export OPENAI_API_KEY='your-key'")
        return

    client = VisionClient(api_key=api_key)

    # Example 1: Analyze from URL
    logger.info("=== Example 1: URL-based image analysis ===")
    result = client.analyze_image_url(
        image_url="https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/PNG_transparency_demonstration_1.png/300px-PNG_transparency_demonstration_1.png",
        prompt="Describe what you see in this image. List all visible objects.",
    )
    logger.info(f"Analysis: {result.model_dump_json(indent=2)}")

    # Example 2: Local file (commented out)
    # result = client.analyze_image_file("screenshot.png", prompt="What's on this screen?")
    # print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    demo()