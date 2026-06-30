"""
M14: OCR + Document Analysis Pipeline
======================================
Extract text from scanned documents using vision models,
then analyze with structured output.

Key skills:
- OCR for scanned PDFs and images
- Table extraction from document images
- Combining OCR with LLM analysis
- Handling multi-page documents
- Layout-aware text extraction
"""

import base64
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

class ExtractedField(BaseModel):
    """A single field extracted from a document."""
    name: str
    value: str
    confidence: float = Field(..., ge=0.0, le=1.0)


class TableData(BaseModel):
    """Extracted table from a document."""
    headers: list[str]
    rows: list[list[str]]
    page_number: Optional[int] = None


class DocumentExtraction(BaseModel):
    """Complete extraction from a document page."""
    page_number: int
    raw_text: str
    structured_fields: list[ExtractedField] = Field(default_factory=list)
    tables: list[TableData] = Field(default_factory=list)
    document_type: str = "unknown"
    language: str = "en"
    confidence: float = Field(0.0, ge=0.0, le=1.0)


class BatchExtractionResult(BaseModel):
    """Result from processing multiple pages."""
    pages: list[DocumentExtraction]
    total_pages: int
    combined_text: str
    all_fields: list[ExtractedField]
    all_tables: list[TableData]


# ──────────────────────────────────────────────
# 2. OCR Client
# ──────────────────────────────────────────────

class DocumentOCR:
    """
    Extract text and structure from document images using vision models.
    
    This approach uses GPT-4o Vision directly for OCR + understanding,
    which is often more accurate than traditional OCR for complex layouts.
    """

    def __init__(self, api_key: str, model: str = "gpt-4o"):
        self.api_key = api_key
        self.model = model
        self.client = httpx.Client(timeout=120.0)

    def extract_page(
        self,
        image_path: str,
        page_number: int = 1,
        extraction_type: str = "full",
    ) -> DocumentExtraction:
        """
        Extract all content from a single document page image.
        
        Args:
            image_path: Path to the page image (PNG, JPG)
            page_number: Page number for reference
            extraction_type: "full", "fields_only", "tables_only"
        """
        b64 = self._encode_image(image_path)

        prompts = {
            "full": """
                Extract ALL content from this document page.
                
                1. All visible text (preserve structure and layout)
                2. Structured fields (name-value pairs, form fields)
                3. Any tables (with headers and rows)
                4. Document type (invoice, receipt, form, letter, report)
                5. Language detected
                
                Return JSON with:
                - raw_text: complete text content
                - structured_fields: list of {name, value, confidence}
                - tables: list of {headers, rows}
                - document_type: classification
                - language: detected language
                - confidence: overall extraction confidence (0-1)
            """,
            "fields_only": """
                Extract only structured fields from this form/invoice.
                Look for: dates, amounts, names, IDs, addresses, totals.
                
                Return JSON with:
                - raw_text: brief text summary
                - structured_fields: list of {name, value, confidence}
                - document_type: classification
                - confidence: overall confidence
            """,
            "tables_only": """
                Extract any tables from this document.
                Identify column headers and all data rows.
                
                Return JSON with:
                - tables: list of {headers, rows}
                - raw_text: surrounding text
                - confidence: extraction confidence
            """,
        }

        prompt = prompts.get(extraction_type, prompts["full"])

        try:
            response = self.client.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": self.model,
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": prompt},
                                {
                                    "type": "image_url",
                                    "image_url": {
                                        "url": f"data:image/png;base64,{b64}",
                                        "detail": "high",
                                    },
                                },
                            ],
                        }
                    ],
                    "response_format": {"type": "json_object"},
                    "max_tokens": 4096,
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()
            content = json.loads(data["choices"][0]["message"]["content"])

            # Parse structured fields
            fields = [
                ExtractedField(**f)
                for f in content.get("structured_fields", [])
            ]

            # Parse tables
            tables = [
                TableData(**t)
                for t in content.get("tables", [])
            ]

            return DocumentExtraction(
                page_number=page_number,
                raw_text=content.get("raw_text", ""),
                structured_fields=fields,
                tables=tables,
                document_type=content.get("document_type", "unknown"),
                language=content.get("language", "en"),
                confidence=content.get("confidence", 0.0),
            )

        except Exception as e:
            logger.error(f"Page {page_number} extraction failed: {e}")
            raise

    def extract_pdf_pages(
        self,
        pdf_path: str,
        dpi: int = 200,
    ) -> list[DocumentExtraction]:
        """
        Extract text from all pages of a PDF.
        
        Note: Requires pdf2image (poppler) for PDF-to-image conversion.
        Install: pip install pdf2image
        """
        try:
            from pdf2image import convert_from_path
        except ImportError:
            logger.error("pdf2image not installed. Run: pip install pdf2image")
            logger.error("Also install poppler: brew install poppler")
            return []

        logger.info(f"Converting PDF to images: {pdf_path}")
        images = convert_from_path(pdf_path, dpi=dpi)
        logger.info(f"Found {len(images)} pages")

        extractions = []
        with tempfile.TemporaryDirectory() as tmpdir:
            for i, img in enumerate(images):
                page_path = os.path.join(tmpdir, f"page_{i+1}.png")
                img.save(page_path, "PNG")

                logger.info(f"Extracting page {i+1}/{len(images)}...")
                extraction = self.extract_page(page_path, page_number=i + 1)
                extractions.append(extraction)

        return extractions

    def _encode_image(self, image_path: str) -> str:
        """Encode image to base64."""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def close(self):
        self.client.close()


# ──────────────────────────────────────────────
# 3. Batch Processing
# ──────────────────────────────────────────────

def process_document_batch(
    image_paths: list[str],
    api_key: str,
) -> BatchExtractionResult:
    """Process multiple document pages and combine results."""
    ocr = DocumentOCR(api_key=api_key)
    try:
        extractions = []
        for i, path in enumerate(image_paths):
            logger.info(f"Processing page {i+1}/{len(image_paths)}: {path}")
            extraction = ocr.extract_page(path, page_number=i + 1)
            extractions.append(extraction)

        # Combine results
        all_fields = []
        all_tables = []
        combined_text_parts = []

        for ext in extractions:
            all_fields.extend(ext.structured_fields)
            all_tables.extend(ext.tables)
            combined_text_parts.append(f"--- Page {ext.page_number} ---\n{ext.raw_text}")

        return BatchExtractionResult(
            pages=extractions,
            total_pages=len(extractions),
            combined_text="\n\n".join(combined_text_parts),
            all_fields=all_fields,
            all_tables=all_tables,
        )

    finally:
        ocr.close()


# ──────────────────────────────────────────────
# 4. Demo
# ──────────────────────────────────────────────

def demo():
    """Run OCR demo if API key is available."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("No OPENAI_API_KEY set. Skipping demo.")
        logger.info("To run: export OPENAI_API_KEY='your-key'")
        logger.info("Then: python ocr_plus_analysis.py --image invoice.png")
        return

    import argparse
    parser = argparse.ArgumentParser(description="OCR + Document Analysis")
    parser.add_argument("--image", help="Path to document image")
    parser.add_argument("--pdf", help="Path to PDF file")
    parser.add_argument("--type", default="full", choices=["full", "fields_only", "tables_only"])
    args = parser.parse_args()

    ocr = DocumentOCR(api_key=api_key)

    if args.image:
        result = ocr.extract_page(args.image, extraction_type=args.type)
        print(json.dumps(result.model_dump(), indent=2))

    elif args.pdf:
        results = ocr.extract_pdf_pages(args.pdf)
        for r in results:
            print(f"\n=== Page {r.page_number} ===")
            print(f"Type: {r.document_type}")
            print(f"Fields: {len(r.structured_fields)}")
            print(f"Tables: {len(r.tables)}")
            print(f"Text preview: {r.raw_text[:200]}...")

    else:
        logger.info("No input provided. Use --image or --pdf.")
        parser.print_help()

    ocr.close()


if __name__ == "__main__":
    demo()