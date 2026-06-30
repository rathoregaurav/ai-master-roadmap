# Enterprise Admin Layer - M21 Project

> An enterprise governance layer for AI systems: prompt registry, model registry, audit logging, and multi-tenant access control.

## Architecture

```
Admin Panel → [Prompt Registry → Model Registry → Tenant Config → Audit Log]
AI System → [Auth (Tenant Check) → Rate Limiter → Audit Logger → Response]
```

## Core Components

```python
# registry.py
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
import json

class PromptVersion(BaseModel):
    id: str
    name: str
    version: int
    prompt_text: str
    model_id: str
    parameters: dict = {"temperature": 0.7, "max_tokens": 1024}
    tags: List[str] = []
    author: str
    status: str = "draft"  # draft, active, archived, deprecated
    created_at: str = ""
    change_reason: str = ""

class ModelRegistry(BaseModel):
    id: str
    name: str  # "gpt-4o", "gpt-4o-mini", "claude-3.5"
    provider: str
    capabilities: List[str] = ["chat", "stream", "vision", "tools"]
    cost_per_input_mtok: float
    cost_per_output_mtok: float
    status: str = "active"

class AuditEntry(BaseModel):
    id: str
    timestamp: str
    user_id: str
    tenant_id: str
    action: str  # "query", "invoke_tool", "approve", "reject"
    request_preview: str = ""
    response_preview: str = ""
    model_id: str = ""
    tokens_used: int = 0
    cost: float = 0.0
    safety_checks: str = "passed"
    ip_address: str = ""
    trace_id: str = ""

class EnterpriseAdminLayer:
    def __init__(self):
        self.prompts: List[PromptVersion] = []
        self.models: List[ModelRegistry] = []
        self.audit_log: List[AuditEntry] = []
        self._init_defaults()
    
    def _init_defaults(self):
        self.models.append(ModelRegistry(
            id="gpt-4o", name="GPT-4o", provider="OpenAI",
            capabilities=["chat", "stream", "vision", "tools"],
            cost_per_input_mtok=2.50, cost_per_output_mtok=10.00
        ))
        self.models.append(ModelRegistry(
            id="gpt-4o-mini", name="GPT-4o Mini", provider="OpenAI",
            capabilities=["chat", "stream", "tools"],
            cost_per_input_mtok=0.15, cost_per_output_mtok=0.60
        ))
    
    def register_prompt(self, prompt: PromptVersion):
        prompt.created_at = datetime.now().isoformat()
        self.prompts.append(prompt)
        return prompt.id
    
    def activate_prompt(self, prompt_id: str):
        for p in self.prompts:
            if p.id == prompt_id:
                # Deactivate all other prompts with same name
                for other in self.prompts:
                    if other.name == p.name and other.id != p.id:
                        other.status = "archived"
                p.status = "active"
                return p
        return None
    
    def log_audit(self, entry: AuditEntry):
        entry.timestamp = datetime.now().isoformat()
        self.audit_log.append(entry)
    
    def get_audit_report(self, tenant_id: str = "", limit: int = 100) -> List[dict]:
        entries = [e for e in self.audit_log if not tenant_id or e.tenant_id == tenant_id]
        return sorted(entries, key=lambda x: x.timestamp, reverse=True)[:limit]
```

## Tenant Isolation Model

```python
# tenancy.py
class TenantConfig(BaseModel):
    tenant_id: str
    name: str
    allowed_models: List[str]
    rate_limit_per_minute: int
    max_tokens_per_request: int
    custom_prompts: dict = {}
    data_retention_days: int = 90
    audit_retention_days: int = 365

class MultiTenantManager:
    def __init__(self):
        self.tenants = {}
    
    def get_scoped_context(self, tenant_id: str) -> dict:
        """Get tenant-specific configuration for scoping requests."""
        tenant = self.tenants.get(tenant_id)
        if not tenant:
            raise ValueError(f"Unknown tenant: {tenant_id}")
        return {
            "tenant_id": tenant.tenant_id,
            "allowed_models": tenant.allowed_models,
            "rate_limit": tenant.rate_limit_per_minute,
            "max_tokens": tenant.max_tokens_per_request,
        }
    
    def validate_access(self, tenant_id: str, model_id: str) -> bool:
        """Check if tenant is allowed to use a specific model."""
        tenant = self.tenants.get(tenant_id)
        if not tenant:
            return False
        return model_id in tenant.allowed_models
```

## Project Structure

```
enterprise-admin-layer/
├── registry.py            # Prompt and model registry
├── audit.py               # Audit logging
├── tenancy.py             # Multi-tenant management
├── admin_api.py           # Admin REST API (FastAPI)
├── tests/
│   ├── test_registry.py
│   ├── test_audit.py
│   └── test_tenancy.py
├── requirements.txt
└── README.md