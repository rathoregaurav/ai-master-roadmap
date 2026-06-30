# AI Engineering Tools & Setup Guide

> Essential tools and setup for AI engineering. Reference for M0.

## Core Tools

| Tool | Purpose | Install |
|------|---------|---------|
| Python 3.11+ | Runtime | `brew install python@3.11` |
| Docker | Containerization | `brew install docker` |
| VS Code | Editor | Download from code.visualstudio.com |
| Git | Version control | `brew install git` |
| pip | Python package manager | Comes with Python |
| uv | Fast Python package manager | `curl -LsSf https://astral.sh/uv/install.sh | sh` |

## VS Code Extensions for AI Engineering

- Python (ms-python.python)
- Pylance (ms-python.vscode-pylance)
- Docker (ms-azuretools.vscode-docker)
- YAML (redhat.vscode-yaml)
- GitHub Copilot (GitHub.copilot)
- Markdown Preview Mermaid Support (bierner.markdown-mermaid)
- Even Better TOML (tamasfe.even-better-toml)
- Error Lens (usernamehw.errorlens)

## Python Virtual Environment Setup

```bash
# Create
python3 -m venv .venv

# Activate
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Freeze current dependencies
pip freeze > requirements.txt
```

## Docker Quick Reference

```bash
# Build image
docker build -t my-ai-app .

# Run container
docker run -p 8000:8000 --env-file .env my-ai-app

# List running containers
docker ps

# Stop container
docker stop <container_id>

# Docker Compose
docker compose up -d
docker compose down
```

## Environment Variables (.env)

```bash
# .env.example - NEVER commit .env
OPENAI_API_KEY=sk-...
ANTHROPIC_API_KEY=sk-ant-...
COHERE_API_KEY=...
DATABASE_URL=postgresql://user:pass@localhost:5432/db
LOG_LEVEL=INFO
```

## Project Structure Template

```
my-ai-project/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI app
│   ├── schemas.py       # Pydantic models
│   ├── services/        # Business logic
│   │   ├── __init__.py
│   │   └── llm_service.py
│   └── utils/           # Helpers
│       ├── __init__.py
│       └── logging.py
├── tests/
│   ├── __init__.py
│   └── test_main.py
└── data/                # Local data (gitignored)
```

## Common AI Package Versions (2026)

```txt
fastapi>=0.110.0
uvicorn[standard]>=0.27.0
pydantic>=2.5.0
httpx>=0.27.0
openai>=1.12.0
anthropic>=0.23.0
cohere>=5.0.0
loguru>=0.7.2
python-dotenv>=1.0.0
pytest>=8.0.0
pytest-asyncio>=0.23.0