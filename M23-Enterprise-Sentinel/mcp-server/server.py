"""
MCP Server — Enterprise Sentinel Ingestion Layer
=================================================
Accepts multimodal data (PDFs, images, Slack transcripts, webhooks)
and exposes them via MCP protocol to the Agent Supervisor.
"""

import json
import logging
import os
import tempfile
from pathlib import Path
from typing import Any, Optional
from datetime import datetime

import httpx
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 1. Data Models
# ──────────────────────────────────────────────

class IngestedDocument(BaseModel):
    """A document ingested into the system."""
    id: str
    type: str  # pdf, image, slack, webhook
    content: str
    metadata: dict[str, Any] = Field(default_factory=dict)
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    file_path: Optional[str] = None


class MCPTool(BaseModel):
    """MCP Tool definition for discovery."""
    name: str
    description: str
    input_schema: dict[str, Any]


class MCPResource(BaseModel):
    """MCP Resource definition."""
    uri: str
    name: str
    description: str
    mime_type: str = "text/plain"


# ──────────────────────────────────────────────
# 2. PDF Handler
# ──────────────────────────────────────────────

class PDFHandler:
    """Handle PDF document ingestion."""

    async def extract_text(self, file_path: str) -> str:
        """
        Extract text from a PDF file.
        
        Uses PyMuPDF (fitz) for text extraction.
        Falls back to pdfminer if not available.
        """
        try:
            import fitz  # PyMuPDF
            doc = fitz.open(file_path)
            text = ""
            for page in doc:
                text += f"\n--- Page {page.number + 1} ---\n"
                text += page.get_text()
            doc.close()
            logger.info(f"Extracted {len(text)} chars from PDF: {file_path}")
            return text
        except ImportError:
            logger.warning("PyMuPDF not installed. Install: pip install pymupdf")
            return self._extract_pdfminer(file_path)

    def _extract_pdfminer(self, file_path: str) -> str:
        """Fallback PDF extraction using pdfminer."""
        try:
            from pdfminer.high_level import extract_text
            text = extract_text(file_path)
            return text
        except ImportError:
            logger.error("No PDF library available. Install: pip install pymupdf pdfminer.six")
            return ""

    async def ingest(self, file_path: str, metadata: dict = None) -> IngestedDocument:
        """Ingest a PDF file."""
        text = await self.extract_text(file_path)
        return IngestedDocument(
            id=f"pdf_{Path(file_path).stem}_{int(datetime.now().timestamp())}",
            type="pdf",
            content=text,
            metadata=metadata or {"file_name": Path(file_path).name},
            file_path=file_path,
        )


# ──────────────────────────────────────────────
# 3. Image Handler
# ──────────────────────────────────────────────

class ImageHandler:
    """Handle image document ingestion."""

    async def describe_image(self, file_path: str, api_key: str) -> str:
        """
        Use GPT-4o Vision to describe an image.
        This produces a text representation that can be indexed.
        """
        import base64

        with open(file_path, "rb") as f:
            b64 = base64.b64encode(f.read()).decode("utf-8")

        async with httpx.AsyncClient(timeout=60.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": "gpt-4o",
                    "messages": [
                        {
                            "role": "user",
                            "content": [
                                {"type": "text", "text": "Describe this image in detail. Include all visible text, objects, people, and context."},
                                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{b64}", "detail": "high"}},
                            ],
                        }
                    ],
                    "max_tokens": 1024,
                },
                headers={
                    "Authorization": f"Bearer {api_key}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]

    async def ingest(self, file_path: str, api_key: str, metadata: dict = None) -> IngestedDocument:
        """Ingest an image file."""
        description = await self.describe_image(file_path, api_key)
        return IngestedDocument(
            id=f"img_{Path(file_path).stem}_{int(datetime.now().timestamp())}",
            type="image",
            content=description,
            metadata=metadata or {
                "file_name": Path(file_path).name,
                "original_format": Path(file_path).suffix,
            },
            file_path=file_path,
        )


# ──────────────────────────────────────────────
# 4. Slack Handler
# ──────────────────────────────────────────────

class SlackHandler:
    """Handle Slack transcript ingestion."""

    async def parse_transcript(self, file_path: str) -> str:
        """Parse a Slack export file."""
        path = Path(file_path)
        if path.suffix == ".json":
            data = json.loads(path.read_text())
            messages = []
            for msg in data:
                user = msg.get("user", "unknown")
                text = msg.get("text", "")
                ts = msg.get("ts", "")
                messages.append(f"[{ts}] {user}: {text}")
            return "\n".join(messages)
        else:
            # Plain text transcript
            return path.read_text()

    async def ingest(self, file_path: str, metadata: dict = None) -> IngestedDocument:
        """Ingest a Slack transcript."""
        text = await self.parse_transcript(file_path)
        return IngestedDocument(
            id=f"slack_{Path(file_path).stem}_{int(datetime.now().timestamp())}",
            type="slack",
            content=text,
            metadata=metadata or {"file_name": Path(file_path).name, "source": "slack"},
            file_path=file_path,
        )


# ──────────────────────────────────────────────
# 5. Webhook Handler
# ──────────────────────────────────────────────

class WebhookHandler:
    """Handle webhook-based ingestion."""

    async def ingest(self, payload: dict) -> IngestedDocument:
        """Ingest data from a webhook payload."""
        content = json.dumps(payload.get("data", payload), indent=2)
        event_type = payload.get("type", "webhook")
        return IngestedDocument(
            id=f"webhook_{int(datetime.now().timestamp())}",
            type="webhook",
            content=content,
            metadata={
                "event_type": event_type,
                "source": payload.get("source", "unknown"),
                "raw_payload": payload,
            },
        )


# ──────────────────────────────────────────────
# 6. MCP Server
# ──────────────────────────────────────────────

class MCPServer:
    """
    MCP Server that connects Enterprise Sentinel to external data.
    
    Implements the Model Context Protocol for tool/resource discovery.
    """

    def __init__(self, openai_api_key: str):
        self.api_key = openai_api_key
        self.pdf_handler = PDFHandler()
        self.image_handler = ImageHandler()
        self.slack_handler = SlackHandler()
        self.webhook_handler = WebhookHandler()
        self.documents: list[IngestedDocument] = []

    def list_tools(self) -> list[MCPTool]:
        """List available MCP tools."""
        return [
            MCPTool(
                name="ingest_pdf",
                description="Ingest a PDF document for RAG retrieval",
                input_schema={
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to PDF file"},
                        "metadata": {"type": "object", "description": "Optional metadata"},
                    },
                    "required": ["file_path"],
                },
            ),
            MCPTool(
                name="ingest_image",
                description="Ingest an image for vision analysis",
                input_schema={
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to image file"},
                        "metadata": {"type": "object", "description": "Optional metadata"},
                    },
                    "required": ["file_path"],
                },
            ),
            MCPTool(
                name="ingest_slack_transcript",
                description="Ingest a Slack channel export",
                input_schema={
                    "type": "object",
                    "properties": {
                        "file_path": {"type": "string", "description": "Path to Slack export file"},
                        "metadata": {"type": "object", "description": "Optional metadata"},
                    },
                    "required": ["file_path"],
                },
            ),
            MCPTool(
                name="ingest_webhook",
                description="Ingest data via webhook payload",
                input_schema={
                    "type": "object",
                    "properties": {
                        "payload": {"type": "object", "description": "Webhook payload"},
                    },
                    "required": ["payload"],
                },
            ),
        ]

    def list_resources(self) -> list[MCPResource]:
        """List available MCP resources."""
        resources = []
        for doc in self.documents[-50:]:  # Last 50 docs
            resources.append(MCPResource(
                uri=f"sentinel://documents/{doc.id}",
                name=f"Document: {doc.id}",
                description=f"{doc.type} document from {doc.created_at}",
            ))
        return resources

    async def call_tool(self, tool_name: str, arguments: dict) -> dict:
        """Execute an MCP tool call."""
        if tool_name == "ingest_pdf":
            doc = await self.pdf_handler.ingest(
                arguments["file_path"],
                arguments.get("metadata"),
            )
        elif tool_name == "ingest_image":
            doc = await self.image_handler.ingest(
                arguments["file_path"],
                self.api_key,
                arguments.get("metadata"),
            )
        elif tool_name == "ingest_slack_transcript":
            doc = await self.slack_handler.ingest(
                arguments["file_path"],
                arguments.get("metadata"),
            )
        elif tool_name == "ingest_webhook":
            doc = await self.webhook_handler.ingest(arguments["payload"])
        else:
            raise ValueError(f"Unknown tool: {tool_name}")

        self.documents.append(doc)
        logger.info(f"Ingested document: {doc.id} ({doc.type})")
        return {"status": "success", "document_id": doc.id, "type": doc.type}

    async def handle_query(self, query: str) -> str:
        """Handle a natural language query about ingested documents."""
        if not self.documents:
            return "No documents have been ingested yet. Use the ingest tools first."

        context = "\n\n".join(
            f"[{doc.type} - {doc.id}]\n{doc.content[:500]}"
            for doc in self.documents[-10:]
        )

        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You answer questions based on ingested documents."},
                        {"role": "user", "content": f"Context:\n{context}\n\nQuestion: {query}"},
                    ],
                    "max_tokens": 1000,
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]


# ──────────────────────────────────────────────
# 7. CLI Entry Point
# ──────────────────────────────────────────────

async def main():
    """Run the MCP server as a CLI tool."""
    import argparse

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.error("OPENAI_API_KEY environment variable required")
        return

    server = MCPServer(api_key)

    parser = argparse.ArgumentParser(description="Enterprise Sentinel MCP Server")
    subparsers = parser.add_subparsers(dest="command")

    # ingest command
    ingest_parser = subparsers.add_parser("ingest")
    ingest_parser.add_argument("--type", required=True, choices=["pdf", "image", "slack"])
    ingest_parser.add_argument("--file", required=True)
    ingest_parser.add_argument("--metadata", default=None)

    # query command
    query_parser = subparsers.add_parser("query")
    query_parser.add_argument("--question", required=True)

    # list command
    subparsers.add_parser("list-tools")
    subparsers.add_parser("list-resources")

    args = parser.parse_args()

    if args.command == "ingest":
        metadata = json.loads(args.metadata) if args.metadata else None
        result = await server.call_tool(f"ingest_{args.type}", {
            "file_path": args.file,
            "metadata": metadata,
        })
        print(json.dumps(result, indent=2))

    elif args.command == "query":
        answer = await server.handle_query(args.question)
        print(f"\nAnswer: {answer}")

    elif args.command == "list-tools":
        tools = server.list_tools()
        for t in tools:
            print(f"  {t.name}: {t.description}")

    elif args.command == "list-resources":
        resources = server.list_resources()
        for r in resources:
            print(f"  {r.uri}: {r.description}")

    else:
        parser.print_help()


if __name__ == "__main__":
    import asyncio
    asyncio.run(main())