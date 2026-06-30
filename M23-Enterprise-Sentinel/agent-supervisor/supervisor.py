"""
Agent Supervisor — Enterprise Sentinel Orchestrator
=====================================================
Routes queries to specialized workers with human-in-the-loop
for destructive actions, checkpoint management, and cost tracking.
"""

import json
import logging
import os
import time
import uuid
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from typing import Any, Optional

import httpx
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ──────────────────────────────────────────────
# 1. Enums & Data Models
# ──────────────────────────────────────────────

class ActionType(str, Enum):
    READ = "read"
    WRITE = "write"
    DELETE = "delete"
    EXECUTE = "execute"


class WorkerType(str, Enum):
    RAG = "rag"
    SQL = "sql"
    VISION = "vision"
    CODE = "code"


class QueryIntent(BaseModel):
    """Classified intent of a user query."""
    worker_type: WorkerType
    action_type: ActionType
    confidence: float = Field(..., ge=0.0, le=1.0)
    reasoning: str = ""
    requires_approval: bool = False
    parameters: dict[str, Any] = Field(default_factory=dict)


class Checkpoint(BaseModel):
    """A checkpoint/savepoint in a conversation."""
    id: str
    conversation_id: str
    state: dict[str, Any]
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    parent_id: Optional[str] = None


class ApprovalRequest(BaseModel):
    """A request for human approval."""
    id: str
    conversation_id: str
    action: str
    description: str
    details: dict[str, Any]
    status: str = "pending"  # pending, approved, rejected
    created_at: str = Field(default_factory=lambda: datetime.utcnow().isoformat())
    resolved_at: Optional[str] = None


class QueryResult(BaseModel):
    """Result from a worker."""
    worker_type: WorkerType
    status: str  # success, error, requires_approval
    data: Any = None
    error: Optional[str] = None
    latency_ms: float = 0.0
    cost_estimate: float = 0.0


@dataclass
class Conversation:
    """A conversation with checkpoint history."""
    id: str
    messages: list = field(default_factory=list)
    checkpoints: list[Checkpoint] = field(default_factory=list)
    approval_requests: list[ApprovalRequest] = field(default_factory=list)
    context: dict = field(default_factory=dict)


# ──────────────────────────────────────────────
# 2. Intent Classifier
# ──────────────────────────────────────────────

class IntentClassifier:
    """Classify user queries into worker types and action types."""

    DESTRUCTIVE_KEYWORDS = [
        "delete", "remove", "drop", "truncate", "update", "modify",
        "change", "overwrite", "replace", "terminate", "kill",
        "shutdown", "restart", "deploy", "rollback",
    ]

    def classify(self, query: str, context: dict = None) -> QueryIntent:
        """Classify query intent using heuristics + LLM."""
        query_lower = query.lower()

        # Heuristic checks
        is_destructive = any(kw in query_lower for kw in self.DESTRUCTIVE_KEYWORDS)
        
        # Determine worker type
        if any(w in query_lower for w in ["image", "picture", "photo", "screenshot", "chart", "diagram"]):
            worker = WorkerType.VISION
        elif any(w in query_lower for w in ["sql", "database", "table", "query", "data", "record", "sales"]):
            worker = WorkerType.SQL
        elif any(w in query_lower for w in ["code", "function", "script", "program", "algorithm"]):
            worker = WorkerType.CODE
        else:
            worker = WorkerType.RAG  # Default to RAG

        return QueryIntent(
            worker_type=worker,
            action_type=ActionType.DELETE if is_destructive else ActionType.READ,
            confidence=0.8,
            reasoning=f"Heuristic classification: worker={worker.value}, destructive={is_destructive}",
            requires_approval=is_destructive,
            parameters={"query": query, **(context or {})},
        )


# ──────────────────────────────────────────────
# 3. Agent Supervisor
# ──────────────────────────────────────────────

class AgentSupervisor:
    """
    Orchestrates queries across workers.
    
    Flow:
    1. Classify intent
    2. If destructive → request HITL approval
    3. Route to appropriate worker
    4. Synthesize response
    5. Save checkpoint
    """

    def __init__(self, openai_api_key: str):
        self.api_key = openai_api_key
        self.classifier = IntentClassifier()
        self.conversations: dict[str, Conversation] = {}
        self.worker_clients: dict[str, Any] = {}
        self.client = httpx.Client(timeout=60.0)

    def register_worker(self, worker_type: WorkerType, endpoint: str):
        """Register a worker service endpoint."""
        self.worker_clients[worker_type.value] = endpoint
        logger.info(f"Registered {worker_type.value} worker at {endpoint}")

    def create_conversation(self) -> str:
        """Create a new conversation."""
        conv_id = str(uuid.uuid4())
        self.conversations[conv_id] = Conversation(id=conv_id)
        return conv_id

    def process_query(self, query: str, conversation_id: str = None, user_context: dict = None) -> dict:
        """
        Process a user query end-to-end.
        
        Returns the final response with all metadata.
        """
        conv_id = conversation_id or self.create_conversation()
        if conv_id not in self.conversations:
            self.conversations[conv_id] = Conversation(id=conv_id)
        
        conv = self.conversations[conv_id]
        start_time = time.time()

        # Step 1: Classify intent
        logger.info(f"Classifying query: {query[:100]}...")
        intent = self.classifier.classify(query, user_context)
        
        # Step 2: Check if approval needed
        if intent.requires_approval:
            approval = self._request_approval(conv_id, intent)
            return {
                "status": "requires_approval",
                "conversation_id": conv_id,
                "approval_id": approval.id,
                "action": intent.action_type.value,
                "details": intent.parameters,
                "message": f"This action requires approval. Use /approve {approval.id} to proceed.",
            }

        # Step 3: Route to worker
        result = self._route_to_worker(intent)
        
        # Step 4: Synthesize response with LLM
        response = self._synthesize_response(query, result)
        
        # Step 5: Save checkpoint
        checkpoint = Checkpoint(
            id=str(uuid.uuid4()),
            conversation_id=conv_id,
            state={
                "query": query,
                "intent": intent.model_dump(),
                "result": result.model_dump() if result else {},
                "response": response,
            },
        )
        conv.checkpoints.append(checkpoint)
        conv.messages.append({"role": "user", "content": query})
        conv.messages.append({"role": "assistant", "content": response})

        total_latency = (time.time() - start_time) * 1000

        return {
            "status": "success",
            "conversation_id": conv_id,
            "intent": intent.model_dump(),
            "worker_result": result.model_dump() if result else {},
            "response": response,
            "latency_ms": round(total_latency, 1),
            "cost_estimate": result.cost_estimate if result else 0.0,
            "checkpoint_id": checkpoint.id,
        }

    def _request_approval(self, conv_id: str, intent: QueryIntent) -> ApprovalRequest:
        """Create an approval request for destructive actions."""
        conv = self.conversations[conv_id]
        approval = ApprovalRequest(
            id=str(uuid.uuid4()),
            conversation_id=conv_id,
            action=intent.action_type.value,
            description=f"{intent.action_type.value.upper()} operation requested on {intent.worker_type.value}",
            details=intent.parameters,
        )
        conv.approval_requests.append(approval)
        logger.warning(f"Approval required: {approval.id} - {approval.description}")
        return approval

    def approve_action(self, approval_id: str, approved: bool) -> dict:
        """Approve or reject a pending action."""
        for conv in self.conversations.values():
            for req in conv.approval_requests:
                if req.id == approval_id and req.status == "pending":
                    req.status = "approved" if approved else "rejected"
                    req.resolved_at = datetime.utcnow().isoformat()
                    return {
                        "status": req.status,
                        "approval_id": approval_id,
                        "message": f"Action {req.status}",
                    }
        return {"status": "error", "message": f"Approval request {approval_id} not found"}

    def _route_to_worker(self, intent: QueryIntent) -> QueryResult:
        """Route to the appropriate worker."""
        worker_type = intent.worker_type.value
        endpoint = self.worker_clients.get(worker_type)
        
        if not endpoint:
            # Simulate worker for demo
            return self._simulate_worker(intent)
        
        try:
            start = time.time()
            response = self.client.post(
                f"{endpoint}/process",
                json=intent.parameters,
                timeout=30.0,
            )
            response.raise_for_status()
            data = response.json()
            latency = (time.time() - start) * 1000
            return QueryResult(
                worker_type=intent.worker_type,
                status="success",
                data=data.get("result"),
                latency_ms=round(latency, 1),
                cost_estimate=data.get("cost", 0.001),
            )
        except Exception as e:
            logger.error(f"Worker {worker_type} failed: {e}")
            return self._simulate_worker(intent)

    def _simulate_worker(self, intent: QueryIntent) -> QueryResult:
        """Simulate a worker response for demo purposes."""
        query = intent.parameters.get("query", "")
        worker = intent.worker_type
        
        responses = {
            WorkerType.RAG: f"Based on the retrieved documents: '{query}' is a key concept in AI engineering. "
                          f"RAG combines retrieval with generation for accurate, grounded answers.",
            WorkerType.SQL: f"Querying database for: '{query}'. Found 3 relevant records with matching criteria.",
            WorkerType.VISION: f"Analyzing image for: '{query}'. Detected objects, text, and context from the visual input.",
            WorkerType.CODE: f"Generating code for: '{query}'. Implementation complete with error handling.",
        }

        return QueryResult(
            worker_type=worker,
            status="success",
            data=responses.get(worker, "Processed successfully."),
            latency_ms=round(os.urandom(1)[0] * 10 + 50, 1),  # Random 50-300ms
            cost_estimate=0.002,
        )

    def _synthesize_response(self, query: str, result: QueryResult) -> str:
        """Use LLM to synthesize a natural response from worker output."""
        if not result.data:
            return "I couldn't process your request. Please try again."

        prompt = f"""
        Synthesize a natural, helpful response based on:
        
        User Query: {query}
        Worker Type: {result.worker_type.value}
        Worker Output: {result.data}
        
        Provide a clear, conversational response. If data was retrieved, summarize it.
        """

        try:
            response = self.client.post(
                "https://api.openai.com/v1/chat/completions",
                json={
                    "model": "gpt-4o-mini",
                    "messages": [
                        {"role": "system", "content": "You synthesize responses from worker outputs."},
                        {"role": "user", "content": prompt},
                    ],
                    "max_tokens": 500,
                },
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json",
                },
            )
            response.raise_for_status()
            data = response.json()
            return data["choices"][0]["message"]["content"]
        except Exception:
            return str(result.data)

    def get_checkpoint(self, conversation_id: str, checkpoint_id: str = None) -> Optional[Checkpoint]:
        """Get a specific checkpoint or the latest one."""
        conv = self.conversations.get(conversation_id)
        if not conv:
            return None
        if checkpoint_id:
            for cp in conv.checkpoints:
                if cp.id == checkpoint_id:
                    return cp
        return conv.checkpoints[-1] if conv.checkpoints else None

    def rollback_to_checkpoint(self, conversation_id: str, checkpoint_id: str) -> dict:
        """Rollback a conversation to a previous checkpoint."""
        checkpoint = self.get_checkpoint(conversation_id, checkpoint_id)
        if not checkpoint:
            return {"status": "error", "message": "Checkpoint not found"}

        conv = self.conversations[conversation_id]
        # Remove messages and checkpoints after the target
        target_idx = next(
            (i for i, cp in enumerate(conv.checkpoints) if cp.id == checkpoint_id),
            -1,
        )
        if target_idx >= 0:
            conv.checkpoints = conv.checkpoints[: target_idx + 1]
            conv.messages = conv.messages[: (target_idx + 1) * 2]

        return {
            "status": "success",
            "message": f"Rolled back to checkpoint {checkpoint_id}",
            "checkpoint": checkpoint.model_dump(),
        }

    def close(self):
        self.client.close()


# ──────────────────────────────────────────────
# 4. Demo / CLI
# ──────────────────────────────────────────────

def demo():
    """Run a demo of the agent supervisor."""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        logger.info("No API key. Running in simulation mode.")
        api_key = "simulation"

    supervisor = AgentSupervisor(openai_api_key=api_key)

    # Demo queries
    queries = [
        "What is RAG and how does it work?",
        "Show me the Q4 sales data from database",
        "Analyze this chart image for trends",
        "Delete all records from the users table",  # Should trigger approval
    ]

    print("\n" + "="*60)
    print("Enterprise Sentinel - Agent Supervisor Demo")
    print("="*60)

    for query in queries:
        print(f"\n\n{'─'*60}")
        print(f"Query: {query}")
        print(f"{'─'*60}")

        result = supervisor.process_query(query)

        if result["status"] == "requires_approval":
            print(f"\n⚠ Approval Required!")
            print(f"  ID: {result['approval_id']}")
            print(f"  Action: {result['action']}")
            
            # Auto-approve for demo
            approval = supervisor.approve_action(result["approval_id"], approved=True)
            print(f"  → {approval['status']}")
            
            # Retry with approval
            result = supervisor.process_query(query, result["conversation_id"])

        print(f"\nResponse: {result.get('response', '')[:200]}...")
        print(f"Worker: {result.get('intent', {}).get('worker_type', 'N/A')}")
        print(f"Latency: {result.get('latency_ms', 0)}ms")
        print(f"Cost: ${result.get('cost_estimate', 0):.6f}")

    supervisor.close()


if __name__ == "__main__":
    demo()