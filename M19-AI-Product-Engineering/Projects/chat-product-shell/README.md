# Chat Product Shell - M19 Project

> A production-ready chat UI shell with streaming, citations, feedback, and A/B testing.

## Architecture

```
User → Chat UI (React/HTML) → FastAPI → (RAG/Agent) → SSE Streaming → UI Updates
                                    → Feedback API → Analytics
                                    → Feature Flags → A/B Test Variants
```

## API Design

```python
# main.py (FastAPI)
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uuid

app = FastAPI()

class ChatRequest(BaseModel):
    message: str
    conversation_id: Optional[str] = None
    user_id: str
    variant: str = "control"  # A/B test variant

class FeedbackRequest(BaseModel):
    message_id: str
    rating: int  # 1-5
    thumbs: str  # "up" or "down"
    comment: Optional[str] = None

@app.post("/chat/stream")
async def chat_stream(request: ChatRequest):
    """Streaming chat endpoint using SSE."""
    conversation_id = request.conversation_id or str(uuid.uuid4())
    
    async def event_generator():
        # Simulate streaming tokens
        response = "Here is the answer to your question about our refund policy..."
        for token in response.split():
            yield f"data: {json.dumps({'token': token, 'conversation_id': conversation_id})}\n\n"
            await asyncio.sleep(0.05)
        yield f"data: {json.dumps({'done': True, 'conversation_id': conversation_id})}\n\n"
    
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/feedback")
async def submit_feedback(feedback: FeedbackRequest):
    """Record user feedback."""
    # Store in database
    return {"status": "ok", "message_id": feedback.message_id}

@app.get("/variants/{user_id}")
async def get_variant(user_id: str):
    """Get A/B test variant for user."""
    # Consistent hashing for user assignment
    variant = "control" if hash(user_id) % 2 == 0 else "treatment"
    return {"user_id": user_id, "variant": variant}
```

## Chat UI Data Model

```python
# models.py
class Message(BaseModel):
    id: str
    role: str  # "user" | "assistant"
    content: str
    citations: List[Citation] = []
    timestamp: str
    feedback: Optional[Feedback] = None

class Citation(BaseModel):
    id: int
    text: str
    source: str
    url: Optional[str] = None

class Feedback(BaseModel):
    rating: int  # 1-5
    thumbs: str  # "up" | "down"
    comment: str = ""
    category: str = ""  # "correct" | "incorrect" | "unsafe" | "other"
```

## Project Structure

```
chat-product-shell/
├── backend/
│   ├── main.py            # FastAPI server
│   ├── models.py          # Data models
│   └── streaming.py       # SSE streaming logic
├── frontend/
│   ├── index.html         # Chat UI
│   ├── styles.css
│   └── app.js             # Streaming + feedback
├── feature_flags/         # A/B test configs
│   └── flags.json
├── requirements.txt
└── README.md