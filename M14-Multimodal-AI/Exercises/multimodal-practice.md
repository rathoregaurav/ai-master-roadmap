# M14: Multimodal AI — Practice Exercises

> **Week 25 · Phase 6 · Future-Proofing & Trends**

---

## Exercise 0: Environment Setup

```
pip install httpx pydantic pdf2image
# For PDF support: brew install poppler
```

Set `OPENAI_API_KEY` in your environment.

---

## Exercise 1: Basic Vision Call (15 min)

**Task:** Call GPT-4o Vision with a screenshot of your desktop.

1. Take a screenshot of your current desktop or an application
2. Use `vision_analyzer.py` to describe what's on the screen
3. Modify the prompt to ask specific questions:
   - "What applications are open?"
   - "What's the time and date shown?"
   - "List all visible icons and their positions"

**Success Criteria:** Get a structured `ImageAnalysis` with accurate object detection and text extraction.

---

## Exercise 2: Document OCR (20 min)

**Task:** Extract text from a scanned document.

1. Find a scanned PDF or take a photo of a document
2. Use `ocr_plus_analysis.py` to extract:
   - All visible text
   - Structured fields (dates, names, amounts)
   - Any tables
3. Compare the accuracy with different image qualities

**Challenge:** Process a 3-page document and verify cross-page consistency.

**Success Criteria:** Correct extraction of at least 90% of text and fields.

---

## Exercise 3: Audio Transcription Pipeline (20 min)

**Task:** Transcribe and analyze a short audio recording.

1. Record a 1-2 minute voice memo (or use a sample audio file)
2. Transcribe it with `audio_transcriber.py`
3. Generate a meeting summary with action items
4. Run sentiment analysis

**Challenge:** Try with background noise and compare accuracy.

**Success Criteria:** Get a `MeetingSummary` with at least 3 action items from your recording.

---

## Exercise 4: Multimodal RAG (30 min)

**Task:** Build a knowledge base that handles text + images.

1. Create a markdown document with embedded images (screenshots, diagrams)
2. Use `multimodal_rag_pipeline.py` to ingest it
3. Ask questions that require both text and visual context
4. Verify the answer references the correct chunks

**Challenge:** Add a document with a chart/image and ask "What does this chart show?"

**Success Criteria:** The RAG system returns answers that correctly reference the visual content.

---

## Exercise 5: Invoice Processing (25 min)

**Task:** Create a specialized document analyzer for invoices.

1. Find or create sample invoice images (or generate one with HTML→PDF→PNG)
2. Use the OCR pipeline to extract:
   - Invoice number
   - Date
   - Vendor name
   - Line items (table)
   - Total amount
3. Validate the extracted data against the original

**Success Criteria:** At least 95% field accuracy on clean invoice images.

---

## Exercise 6: Video Frame Analysis (30 min)

**Task:** Extract and analyze frames from a video.

1. Use `ffmpeg` to extract frames every 5 seconds from a short video
2. Analyze each frame with the vision model
3. Create a timeline of what happens in the video
4. Identify key moments or objects

```bash
# Extract frames
ffmpeg -i video.mp4 -vf fps=1/5 frame_%04d.png
```

**Challenge:** Detect when a specific object appears/disappears in the video.

**Success Criteria:** Accurate timeline description of a 30-second video clip.

---

## Exercise 7: Multimodal Chat Interface (45 min)

**Task:** Build a simple CLI chat that accepts both text and images.

```python
# Pseudocode for your multimodal chat
while True:
    user_input = input("You (text or 'image: path'): ")
    if user_input.startswith("image:"):
        path = user_input.split("image:")[1].strip()
        # Analyze image and add to conversation history
    else:
        # Process text query with context
```

**Features:**
- Maintain conversation history with images
- Answer follow-up questions about previously shared images
- Switch between text-mode and vision-mode seamlessly

**Success Criteria:** A working chat where you can share a screenshot, ask about it, then ask follow-up questions.

---

## Exercise 8: Cost Analysis (15 min)

**Task:** Compare costs of different multimodal approaches.

Calculate the cost of processing 1000 invoices using:

| Approach | Cost per page | Cost for 1000 invoices |
|----------|--------------|----------------------|
| GPT-4o Vision (high detail) | ? | ? |
| GPT-4o Vision (low detail) | ? | ? |
| OCR API + GPT-4o-mini | ? | ? |
| Open-source (LLaVA locally) | ? | ? |

Include latency estimates for each approach.

---

## Interview Questions

1. How does cross-attention fusion work in multimodal models?
2. What are the trade-offs between native multimodal models and pipelined approaches?
3. How would you design a multimodal RAG system that handles both text and images?
4. What strategies can reduce the cost of vision API calls without sacrificing accuracy?
5. How would you handle multi-page PDFs with mixed text, tables, and images?

---

## Best Practices Checklist

- [ ] Use `detail: "low"` for simple images to reduce cost
- [ ] Limit image size to <20MB before sending to API
- [ ] Cache vision results for identical images
- [ ] Use structured output (JSON mode) for field extraction
- [ ] Implement retry logic with exponential backoff
- [ ] Log token usage per request for cost tracking
- [ ] Prefer base64 encoding for small images (<1MB)
- [ ] Use URLs for large images when possible
- [ ] Batch multiple questions about the same image into one call
- [ ] Validate extracted data against known formats

---

## Common Mistakes

1. **Sending full-resolution images unnecessarily** — Downscale to 1024x1024 max
2. **Not handling image loading errors** — Images can be corrupted or too large
3. **Assuming OCR is 100% accurate** — Always validate critical fields
4. **Ignoring token limits** — Vision calls consume many tokens; track usage
5. **No fallback for failed vision calls** — Have a text-only backup plan
6. **Mixing up image formats** — Ensure proper MIME type and base64 encoding
7. **Not testing with varied image qualities** — Real-world images vary widely
8. **Over-relying on one model** — Have multiple model options for different tasks