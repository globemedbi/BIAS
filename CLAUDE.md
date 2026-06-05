# BIAS — BI Agentic System
## Master Claude Code Briefing File
### Version 1.0 | Claims Processing Module

---

## CRITICAL INSTRUCTIONS FOR CLAUDE CODE

Read this entire file before executing any task.
Every decision in this file was made deliberately.
Do not deviate from the structure, naming, or conventions defined here.
When in doubt, refer back to this file.

---

## 1. PROJECT IDENTITY

```
Solution Name:        BIAS (BI Agentic System)
Owner:                BI Unit
First Module:         Claims Processing
Architecture:         Distributed Microservices
Primary Language:     Python 3.11+
Framework:            FastAPI (all services)
Communication:        REST API (Phase 1)
Async Pattern:        202 Accepted + polling/callback
```

---

## 2. THE SEVEN SERVICES

Every service is an independent microservice.
Every service has its own folder, Dockerfile, requirements, and coding agent.
No service shares code except via the shared/ layer.

```
Service             Port    Owner               Category
──────────────────────────────────────────────────────────────
orchestrator        8001    Lead Architect      Brain
communicator        8000    Backend Dev         Gateway
db-agent            8003    DB Specialist       Data
llm-agent           8005    AI Dev              AI
file-management     8002    Backend Dev         Factory
claims-expert       8004    Claims Dev          Reasoning
chatbot             8006    Frontend Dev        Interface
```

---

## 3. FULL FOLDER STRUCTURE TO CREATE

Create every folder and file listed below exactly as shown.
Do not rename. Do not reorganize. Do not skip any file.

```
BIAS/
│
├── CLAUDE.md
├── README.md
├── pyproject.toml
├── .flake8
├── .pre-commit-config.yaml
├── .commitlintrc.json
├── .gitignore
├── .env.example
├── docker-compose.yml
├── Makefile
│
├── .github/
│   ├── PULL_REQUEST_TEMPLATE.md
│   └── workflows/
│       ├── ci.yml
│       ├── cd.yml
│       └── pr-checks.yml
│
├── docs/
│   ├── architecture/
│   │   ├── ARCHITECTURE.md
│   │   ├── DECISIONS.md
│   │   ├── FLOW_DIAGRAMS.md
│   │   └── SECURITY.md
│   ├── api-contracts/
│   │   ├── orchestrator.md
│   │   ├── communicator.md
│   │   ├── db-agent.md
│   │   ├── llm-agent.md
│   │   ├── file-management.md
│   │   ├── claims-expert.md
│   │   └── chatbot.md
│   ├── flight-plan/
│   │   └── FLIGHT_PLAN_SPEC.md
│   ├── standards/
│   │   ├── CODING_STANDARDS.md
│   │   ├── COMMIT_CONVENTION.md
│   │   ├── TESTING_STANDARDS.md
│   │   └── SECURITY_STANDARDS.md
│   └── onboarding/
│       └── GETTING_STARTED.md
│
├── shared/
│   ├── __init__.py
│   ├── communication-layer/
│   │   ├── __init__.py
│   │   ├── app_factory.py
│   │   ├── flight_plan_reader.py
│   │   ├── hand_off.py
│   │   ├── retry_handler.py
│   │   ├── health_check.py
│   │   └── logger.py
│   ├── contracts/
│   │   ├── orchestrator_contract.json
│   │   ├── communicator_contract.json
│   │   ├── db_agent_contract.json
│   │   ├── llm_agent_contract.json
│   │   ├── file_management_contract.json
│   │   ├── claims_expert_contract.json
│   │   └── chatbot_contract.json
│   ├── models/
│   │   ├── __init__.py
│   │   ├── response.py
│   │   ├── claim.py
│   │   ├── flight_plan.py
│   │   └── event.py
│   ├── schemas/
│   │   └── flight_plan_v1.json
│   └── tests/
│       ├── __init__.py
│       └── test_communication_layer.py
│
├── orchestrator/
│   ├── .claude/
│   │   └── SKILL.md
│   ├── agent/
│   │   ├── __init__.py
│   │   └── orchestrator_agent.py
│   ├── flight_plan/
│   │   ├── __init__.py
│   │   ├── builder.py
│   │   └── templates/
│   │       ├── claim_audit.json
│   │       └── doc_anonymization.json
│   ├── service_registry/
│   │   ├── __init__.py
│   │   └── registry.py
│   ├── health_monitor/
│   │   ├── __init__.py
│   │   └── monitor.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── plan_routes.py
│   │       ├── registry_routes.py
│   │       └── metrics_routes.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_flight_plan.py
│   │   ├── test_registry.py
│   │   └── test_recovery.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── communicator/
│   ├── .claude/
│   │   └── SKILL.md
│   ├── agent/
│   │   ├── __init__.py
│   │   └── communicator_agent.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── claims_routes.py
│   │       └── internal_routes.py
│   ├── auth/
│   │   ├── __init__.py
│   │   └── jwt_validator.py
│   ├── routing/
│   │   ├── __init__.py
│   │   └── request_router.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_auth.py
│   │   ├── test_claims.py
│   │   └── test_routing.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── db-agent/
│   ├── .claude/
│   │   └── SKILL.md
│   ├── agent/
│   │   ├── __init__.py
│   │   └── db_agent.py
│   ├── legacy_db/
│   │   ├── __init__.py
│   │   └── legacy_connector.py
│   ├── dwh/
│   │   ├── __init__.py
│   │   └── dwh_connector.py
│   ├── vector_db/
│   │   ├── __init__.py
│   │   └── vector_connector.py
│   ├── logging_db/
│   │   ├── __init__.py
│   │   └── logging_connector.py
│   ├── nl2sql/
│   │   ├── __init__.py
│   │   └── translator.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── claims_routes.py
│   │       ├── auth_routes.py
│   │       ├── query_routes.py
│   │       └── log_routes.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_legacy_db.py
│   │   ├── test_vector_db.py
│   │   └── test_nl2sql.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── llm-agent/
│   ├── .claude/
│   │   └── SKILL.md
│   ├── agent/
│   │   ├── __init__.py
│   │   └── llm_agent.py
│   ├── model_router/
│   │   ├── __init__.py
│   │   └── router.py
│   ├── prompt_engine/
│   │   ├── __init__.py
│   │   ├── prompt_builder.py
│   │   └── templates/
│   │       ├── summarize.txt
│   │       ├── audit.txt
│   │       ├── reconcile.txt
│   │       ├── chat.txt
│   │       └── extract.txt
│   ├── token_governance/
│   │   ├── __init__.py
│   │   └── governor.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── complete_routes.py
│   │       ├── embed_routes.py
│   │       └── usage_routes.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_router.py
│   │   ├── test_prompt_engine.py
│   │   └── test_token_governance.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── file-management/
│   ├── .claude/
│   │   └── SKILL.md
│   ├── agent/
│   │   ├── __init__.py
│   │   └── file_agent.py
│   ├── ocr/
│   │   ├── __init__.py
│   │   └── ocr_engine.py
│   ├── anonymizer/
│   │   ├── __init__.py
│   │   └── anonymizer.py
│   ├── translator/
│   │   ├── __init__.py
│   │   └── translator.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       └── process_routes.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_ocr.py
│   │   ├── test_anonymizer.py
│   │   └── test_translator.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── claims-expert/
│   ├── .claude/
│   │   └── SKILL.md
│   ├── agent/
│   │   ├── __init__.py
│   │   └── claims_agent.py
│   ├── auditor/
│   │   ├── __init__.py
│   │   └── auditor.py
│   ├── reconciler/
│   │   ├── __init__.py
│   │   └── reconciler.py
│   ├── medical_logic/
│   │   ├── __init__.py
│   │   └── medical_rules.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── audit_routes.py
│   │       └── policy_routes.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_auditor.py
│   │   ├── test_reconciler.py
│   │   └── test_policy.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
├── chatbot/
│   ├── .claude/
│   │   └── SKILL.md
│   ├── agent/
│   │   ├── __init__.py
│   │   └── chatbot_agent.py
│   ├── nlu/
│   │   ├── __init__.py
│   │   └── intent_classifier.py
│   ├── conversation/
│   │   ├── __init__.py
│   │   └── session_manager.py
│   ├── formatter/
│   │   ├── __init__.py
│   │   └── response_formatter.py
│   ├── api/
│   │   ├── __init__.py
│   │   ├── main.py
│   │   └── routes/
│   │       ├── __init__.py
│   │       ├── chat_routes.py
│   │       └── format_routes.py
│   ├── tests/
│   │   ├── __init__.py
│   │   ├── test_nlu.py
│   │   ├── test_session.py
│   │   └── test_formatter.py
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── .env.example
│   └── README.md
│
└── infrastructure/
    ├── docker/
    │   └── .gitkeep
    ├── k8s/
    │   ├── orchestrator-deployment.yaml
    │   ├── communicator-deployment.yaml
    │   ├── db-agent-deployment.yaml
    │   ├── llm-agent-deployment.yaml
    │   ├── file-management-deployment.yaml
    │   ├── claims-expert-deployment.yaml
    │   ├── chatbot-deployment.yaml
    │   └── ingress.yaml
    └── secrets/
        └── .gitkeep
```

---

## 4. FILE CONTENTS

Generate every file below with exactly the content specified.

---

### ROOT FILES

---

#### `.gitignore`
```
# Environment
.env
.env.*
!.env.example

# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd
.Python
*.egg-info/
dist/
build/
*.egg
.eggs/

# Virtual environments
.venv/
venv/
env/

# Testing
.pytest_cache/
.coverage
htmlcov/
*.xml

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Secrets
secrets/
*.pem
*.key
*.cert

# Git hooks (generated locally)
.git/hooks/

# Docker
*.log
```

---

#### `pyproject.toml`
```toml
[tool.black]
line-length = 88
target-version = ["py311"]
include = '\.pyi?$'
exclude = '''
/(
    \.git
  | \.venv
  | build
  | dist
  | migrations
)/
'''

[tool.isort]
profile = "black"
multi_line_output = 3
line_length = 88
known_first_party = ["shared"]

[tool.mypy]
python_version = "3.11"
strict = true
ignore_missing_imports = true
disallow_untyped_defs = true
disallow_any_generics = true
warn_return_any = true
warn_unused_ignores = true
exclude = ["tests/", "migrations/"]

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
python_functions = ["test_*"]
asyncio_mode = "auto"
addopts = "--cov=. --cov-report=term-missing --cov-fail-under=80"

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "if __name__ == .__main__.:",
    "raise NotImplementedError"
]
omit = [
    "tests/*",
    ".venv/*"
]

[tool.bandit]
exclude_dirs = ["tests", ".venv"]
severity = "medium"
confidence = "medium"
```

---

#### `.flake8`
```ini
[flake8]
max-line-length = 88
extend-ignore = E203, W503, E501
exclude =
    .git,
    __pycache__,
    .venv,
    migrations,
    build,
    dist
per-file-ignores =
    __init__.py: F401
max-complexity = 10
```

---

#### `.pre-commit-config.yaml`
```yaml
repos:
  - repo: https://github.com/psf/black
    rev: 23.12.1
    hooks:
      - id: black
        language_version: python3.11

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort
        args: ["--profile", "black"]

  - repo: https://github.com/pycqa/flake8
    rev: 7.0.0
    hooks:
      - id: flake8

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies:
          - pydantic==2.5.3
          - fastapi==0.109.0
          - types-requests

  - repo: https://github.com/pycqa/bandit
    rev: 1.7.6
    hooks:
      - id: bandit
        args: ["-c", "pyproject.toml"]
        exclude: tests/

  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: check-merge-conflict
      - id: check-yaml
      - id: check-json
      - id: check-toml
      - id: detect-private-key
      - id: end-of-file-fixer
      - id: trailing-whitespace
      - id: no-commit-to-branch
        args: ["--branch", "main"]
      - id: check-added-large-files
        args: ["--maxkb", "500"]
```

---

#### `.commitlintrc.json`
```json
{
  "rules": {
    "type-enum": [
      2,
      "always",
      ["feat", "fix", "docs", "refactor", "test", "chore", "security"]
    ],
    "scope-enum": [
      2,
      "always",
      [
        "orchestrator",
        "communicator",
        "db-agent",
        "llm-agent",
        "file-management",
        "claims-expert",
        "chatbot",
        "shared",
        "infrastructure",
        "docs",
        "ci"
      ]
    ],
    "type-case": [2, "always", "lower-case"],
    "subject-empty": [2, "never"],
    "subject-max-length": [2, "always", 72],
    "body-max-line-length": [2, "always", 100]
  }
}
```

---

#### `.env.example`
```bash
# ================================================================
# BIAS — BI Agentic System
# Environment Variables Template
# Copy this file to .env and fill in real values
# NEVER commit .env to git
# ================================================================

# ── Environment ─────────────────────────────────────────────────
ENVIRONMENT=development
LOG_LEVEL=INFO

# ── Orchestrator :8001 ──────────────────────────────────────────
ORCHESTRATOR_HOST=http://orchestrator
ORCHESTRATOR_PORT=8001
ORCHESTRATOR_SECRET=change-me-orchestrator-secret

# ── Communicator :8000 ──────────────────────────────────────────
COMMUNICATOR_HOST=http://communicator
COMMUNICATOR_PORT=8000
JWT_SECRET_KEY=change-me-jwt-secret
JWT_ALGORITHM=HS256
JWT_EXPIRY_MINUTES=60
RATE_LIMIT_PER_MINUTE=100

# ── DB Agent :8003 ──────────────────────────────────────────────
DB_AGENT_HOST=http://db-agent
DB_AGENT_PORT=8003
LEGACY_DB_URL=postgresql://user:password@host:5432/legacy_db
LEGACY_DB_POOL_SIZE=10
DWH_URL=postgresql://user:password@host:5432/dwh
DWH_POOL_SIZE=5
VECTOR_DB_URL=http://vector-db:6333
VECTOR_DB_API_KEY=change-me-vector-key
LOGGING_DB_URL=postgresql://user:password@host:5432/logging_db

# ── LLM Agent :8005 ─────────────────────────────────────────────
LLM_AGENT_HOST=http://llm-agent
LLM_AGENT_PORT=8005
OPENAI_API_KEY=change-me-openai-key
ANTHROPIC_API_KEY=change-me-anthropic-key
GOOGLE_AI_API_KEY=change-me-google-key
DEFAULT_MODEL_FAST=gpt-3.5-turbo
DEFAULT_MODEL_BALANCED=gpt-4o-mini
DEFAULT_MODEL_POWERFUL=claude-sonnet-4-20250514
MAX_TOKENS_DEFAULT=1000
CACHE_TTL_SECONDS=3600

# ── File Management :8002 ───────────────────────────────────────
FILE_MANAGEMENT_HOST=http://file-management
FILE_MANAGEMENT_PORT=8002
OBJECT_STORAGE_URL=http://minio:9000
OBJECT_STORAGE_BUCKET=bias-claims
OBJECT_STORAGE_KEY=change-me-storage-key
OBJECT_STORAGE_SECRET=change-me-storage-secret
OCR_ENGINE_URL=http://ocr-engine:8080
ANONYMIZER_URL=http://anonymizer:8090
ANONYMIZER_API_KEY=change-me-anonymizer-key

# ── Claims Expert :8004 ─────────────────────────────────────────
CLAIMS_EXPERT_HOST=http://claims-expert
CLAIMS_EXPERT_PORT=8004

# ── Chatbot :8006 ───────────────────────────────────────────────
CHATBOT_HOST=http://chatbot
CHATBOT_PORT=8006
SESSION_TTL_HOURS=24

# ── Internal Security (shared across all services) ──────────────
INTERNAL_SERVICE_TOKEN=change-me-internal-token-min-32-chars
```

---

#### `docker-compose.yml`
```yaml
version: "3.9"

services:

  orchestrator:
    build:
      context: ./orchestrator
      dockerfile: Dockerfile
    container_name: bias-orchestrator
    ports:
      - "8001:8001"
    env_file:
      - .env
    networks:
      - bias-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8001/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  communicator:
    build:
      context: ./communicator
      dockerfile: Dockerfile
    container_name: bias-communicator
    ports:
      - "8000:8000"
    env_file:
      - .env
    depends_on:
      orchestrator:
        condition: service_healthy
    networks:
      - bias-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/v1/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  db-agent:
    build:
      context: ./db-agent
      dockerfile: Dockerfile
    container_name: bias-db-agent
    ports:
      - "8003:8003"
    env_file:
      - .env
    networks:
      - bias-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8003/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  llm-agent:
    build:
      context: ./llm-agent
      dockerfile: Dockerfile
    container_name: bias-llm-agent
    ports:
      - "8005:8005"
    env_file:
      - .env
    networks:
      - bias-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8005/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  file-management:
    build:
      context: ./file-management
      dockerfile: Dockerfile
    container_name: bias-file-management
    ports:
      - "8002:8002"
    env_file:
      - .env
    networks:
      - bias-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8002/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  claims-expert:
    build:
      context: ./claims-expert
      dockerfile: Dockerfile
    container_name: bias-claims-expert
    ports:
      - "8004:8004"
    env_file:
      - .env
    networks:
      - bias-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8004/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  chatbot:
    build:
      context: ./chatbot
      dockerfile: Dockerfile
    container_name: bias-chatbot
    ports:
      - "8006:8006"
    env_file:
      - .env
    networks:
      - bias-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8006/health"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

networks:
  bias-network:
    driver: bridge
    name: bias-network
```

---

#### `Makefile`
```makefile
.PHONY: help setup up down restart logs test lint format health clean

help:
	@echo ""
	@echo "BIAS — BI Agentic System"
	@echo "========================"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'
	@echo ""

setup: ## Run once after cloning — installs dev tools and hooks
	pip install pre-commit commitizen
	pre-commit install
	pre-commit install --hook-type commit-msg
	pip install black isort flake8 mypy bandit pytest pytest-cov pytest-asyncio
	cp .env.example .env
	@echo ""
	@echo "✅ BIAS dev environment ready"
	@echo "⚠️  Fill in .env with real values before running services"
	@echo ""

up: ## Start all services
	docker-compose up --build -d

down: ## Stop all services
	docker-compose down

restart: ## Restart all services
	docker-compose restart

logs: ## Tail logs for all services
	docker-compose logs -f

logs-service: ## Tail logs for one service — usage: make logs-service s=orchestrator
	docker-compose logs -f $(s)

test: ## Run all tests across all services
	pytest

test-service: ## Run tests for one service — usage: make test-service s=orchestrator
	cd $(s) && pytest

lint: ## Lint all services
	flake8 .
	mypy .

format: ## Format all code
	black .
	isort .

format-check: ## Check formatting without changing files
	black --check .
	isort --check-only .

security: ## Run security scan
	bandit -c pyproject.toml -r .

health: ## Check health of all running services
	@echo "Checking BIAS services..."
	@curl -sf http://localhost:8001/health && echo " ✅ Orchestrator    :8001" || echo " ❌ Orchestrator    :8001"
	@curl -sf http://localhost:8000/api/v1/health && echo " ✅ Communicator    :8000" || echo " ❌ Communicator    :8000"
	@curl -sf http://localhost:8003/health && echo " ✅ DB Agent         :8003" || echo " ❌ DB Agent         :8003"
	@curl -sf http://localhost:8005/health && echo " ✅ LLM Agent        :8005" || echo " ❌ LLM Agent        :8005"
	@curl -sf http://localhost:8002/health && echo " ✅ File Management  :8002" || echo " ❌ File Management  :8002"
	@curl -sf http://localhost:8004/health && echo " ✅ Claims Expert    :8004" || echo " ❌ Claims Expert    :8004"
	@curl -sf http://localhost:8006/health && echo " ✅ Chatbot          :8006" || echo " ❌ Chatbot          :8006"

clean: ## Remove all containers and volumes
	docker-compose down -v
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type d -name .pytest_cache -exec rm -rf {} +
	find . -name "*.pyc" -delete
	find . -name ".coverage" -delete
```

---

### SHARED LAYER FILES

---

#### `shared/models/response.py`
```python
"""
BIAS Shared Response Models
All services MUST use these models for API responses.
No custom response shapes permitted.
"""
from datetime import datetime
from enum import Enum
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class StatusEnum(str, Enum):
    SUCCESS = "SUCCESS"
    FAILED = "FAILED"
    IN_PROGRESS = "IN_PROGRESS"
    ACCEPTED = "ACCEPTED"
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"


class ErrorDetail(BaseModel):
    error_code: str
    message: str
    field: Optional[str] = None


class BaseResponse(BaseModel):
    """
    Mandatory base for ALL BIAS API responses.
    Every endpoint response must inherit from this.
    """
    status: StatusEnum
    service: str
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    request_id: Optional[str] = None


class SuccessResponse(BaseResponse):
    status: StatusEnum = StatusEnum.SUCCESS
    data: Optional[Any] = None


class ErrorResponse(BaseResponse):
    status: StatusEnum = StatusEnum.FAILED
    errors: List[ErrorDetail]
    support_ref: Optional[str] = None


class AcceptedResponse(BaseResponse):
    status: StatusEnum = StatusEnum.ACCEPTED
    job_id: str
    poll_url: str


class HealthResponse(BaseModel):
    service: str
    status: str = "HEALTHY"
    version: str
    uptime_s: Optional[int] = None
    checks: Optional[dict] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

---

#### `shared/models/flight_plan.py`
```python
"""
BIAS Flight Plan Models
Defines the structure of the Flight Plan JSON
that travels with every claim request.
"""
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class RequestTypeEnum(str, Enum):
    CLAIM_AUDIT = "CLAIM_AUDIT"
    DOC_ANONYMIZATION = "DOC_ANONYMIZATION"
    CLAIM_STATUS = "CLAIM_STATUS"


class OverallStatusEnum(str, Enum):
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED_RETRYING = "FAILED_RETRYING"
    FAILED = "FAILED"


class StageStatusEnum(str, Enum):
    PENDING = "PENDING"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    SKIPPED = "SKIPPED"


class ServiceRegistry(BaseModel):
    ORCHESTRATOR: str
    COMMUNICATOR: str
    FILE_MANAGEMENT: str
    DB_AGENT: str
    CLAIMS_EXPERT: str
    LLM_AGENT: str
    CHATBOT: str


class StepRouting(BaseModel):
    next_on_success: Any  # int or "COMPLETE"
    next_on_failure: int = 99
    callback_agent: Optional[str] = None


class FlightPlanStep(BaseModel):
    stage: int
    service: str
    endpoint: str
    status: StageStatusEnum = StageStatusEnum.PENDING
    routing: StepRouting
    config: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    output_uri: Optional[str] = None


class FlightPlanMetadata(BaseModel):
    plan_id: str
    request_id: str
    version: str = "1.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    request_type: RequestTypeEnum


class ExecutionState(BaseModel):
    overall_status: OverallStatusEnum = OverallStatusEnum.IN_PROGRESS
    current_stage: int = 0
    total_stages: int
    last_updated: datetime = Field(default_factory=datetime.utcnow)


class InputData(BaseModel):
    claim_id: str
    member_id: str
    file_uris: List[str] = []


class ErrorLogEntry(BaseModel):
    stage: int
    service: str
    timestamp: datetime
    error_code: str
    message: str


class ContextPayload(BaseModel):
    input_data: InputData
    intermediate_results: Dict[str, Any] = {}
    error_log: List[ErrorLogEntry] = []


class FlightPlan(BaseModel):
    """
    The Flight Plan — the core execution artifact of BIAS.
    Created by Orchestrator. Travels with every claim request.
    Every service reads this, updates its stage, and passes it on.
    """
    flight_plan_metadata: FlightPlanMetadata
    execution_state: ExecutionState
    service_registry: ServiceRegistry
    steps: List[FlightPlanStep]
    context_payload: ContextPayload
```

---

#### `shared/models/claim.py`
```python
"""
BIAS Shared Claim Model
Unified claim data structure used across all services.
"""
from datetime import datetime
from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, Field


class ClaimTypeEnum(str, Enum):
    MEDICAL = "MEDICAL"
    DENTAL = "DENTAL"
    VISION = "VISION"
    PHARMACY = "PHARMACY"


class ClaimStatusEnum(str, Enum):
    SUBMITTED = "SUBMITTED"
    IN_PROGRESS = "IN_PROGRESS"
    APPROVED = "APPROVED"
    PENDING_REVIEW = "PENDING_REVIEW"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


class PriorityEnum(str, Enum):
    NORMAL = "NORMAL"
    HIGH = "HIGH"
    URGENT = "URGENT"


class FileAttachment(BaseModel):
    file_id: str
    file_name: str
    file_type: str
    uri: str
    size_bytes: Optional[int] = None


class Claim(BaseModel):
    """
    Core claim data model shared across all BIAS services.
    """
    claim_id: str
    member_id: str
    claim_type: ClaimTypeEnum
    priority: PriorityEnum = PriorityEnum.NORMAL
    status: ClaimStatusEnum = ClaimStatusEnum.SUBMITTED
    submitted_by: str
    file_attachments: List[FileAttachment] = []
    submitted_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    plan_id: Optional[str] = None
    request_id: Optional[str] = None
```

---

#### `shared/communication-layer/app_factory.py`
```python
"""
BIAS Standard FastAPI App Factory
ALL services MUST use this to create their FastAPI application.
No direct FastAPI() instantiation allowed in any service.
"""
import logging
import os
import time
from typing import Optional

import structlog
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logger = structlog.get_logger()


def create_app(
    service_name: str,
    version: str = "1.0.0",
    description: str = "",
) -> FastAPI:
    """
    Creates a standardized BIAS FastAPI application.

    Args:
        service_name: The BIAS service name (e.g. ORCHESTRATOR)
        version: Service version string
        description: Short service description

    Returns:
        Configured FastAPI application instance
    """
    app = FastAPI(
        title=f"BIAS - {service_name}",
        version=version,
        description=description,
        docs_url="/docs",
        redoc_url="/redoc",
    )

    # Standard CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Standard request logging middleware
    @app.middleware("http")
    async def log_requests(request: Request, call_next):  # type: ignore
        start_time = time.time()
        response = await call_next(request)
        duration_ms = (time.time() - start_time) * 1000
        logger.info(
            "request_handled",
            service=service_name,
            method=request.method,
            path=request.url.path,
            status_code=response.status_code,
            duration_ms=round(duration_ms, 2),
        )
        return response

    # Standard exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        logger.error(
            "unhandled_exception",
            service=service_name,
            path=request.url.path,
            error=str(exc),
        )
        return JSONResponse(
            status_code=500,
            content={
                "status": "FAILED",
                "service": service_name,
                "errors": [
                    {
                        "error_code": "INTERNAL_SERVER_ERROR",
                        "message": "An unexpected error occurred",
                    }
                ],
            },
        )

    # Standard health endpoint
    @app.get("/health", tags=["Health"])
    async def health() -> dict:
        return {
            "service": service_name,
            "status": "HEALTHY",
            "version": version,
            "environment": os.getenv("ENVIRONMENT", "development"),
        }

    return app
```

---

#### `shared/communication-layer/logger.py`
```python
"""
BIAS Standard Logger
ALL services MUST use this logger.
No print() statements. No custom logging setup.
"""
import logging
import os
import sys

import structlog


def get_logger(service_name: str) -> structlog.BoundLogger:
    """
    Returns a structured JSON logger bound to the service name.

    Args:
        service_name: The BIAS service name

    Returns:
        Configured structlog BoundLogger

    Usage:
        from shared.communication_layer.logger import get_logger
        logger = get_logger("CLAIMS_EXPERT")
        logger.info("audit_started", claim_id=claim_id, plan_id=plan_id)
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()

    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ],
        wrapper_class=structlog.make_filtering_bound_logger(
            getattr(logging, log_level)
        ),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(file=sys.stdout),
    )

    return structlog.get_logger().bind(
        service=service_name,
        environment=os.getenv("ENVIRONMENT", "development"),
    )
```

---

#### `shared/communication-layer/hand_off.py`
```python
"""
BIAS Flight Plan Hand-off
Handles reading the next stage from a Flight Plan
and making the API call to the next service.
"""
from typing import Any, Dict, Optional

import httpx
import structlog

from shared.models.flight_plan import FlightPlan, StageStatusEnum

logger = structlog.get_logger()

TIMEOUT_SECONDS = 30.0


async def execute_hand_off(
    flight_plan: FlightPlan,
    completed_stage: int,
    output_uri: Optional[str] = None,
    additional_payload: Optional[Dict[str, Any]] = None,
) -> bool:
    """
    Commits the current stage and hands off to the next service.

    CRITICAL ORDER:
    1. Mark current stage as COMPLETED in flight plan
    2. Determine next stage from routing
    3. Look up next service URL from registry
    4. POST to next service with updated flight plan
    5. Return success/failure

    Args:
        flight_plan: The current Flight Plan
        completed_stage: The stage number just completed
        output_uri: Optional S3 URI of output artifact
        additional_payload: Optional extra data for next service

    Returns:
        True if hand-off succeeded, False if failed
    """
    # Step 1: Update current stage status
    for step in flight_plan.steps:
        if step.stage == completed_stage:
            step.status = StageStatusEnum.COMPLETED
            if output_uri:
                step.output_uri = output_uri
            break

    # Step 2: Find next stage
    current_step = next(
        (s for s in flight_plan.steps if s.stage == completed_stage), None
    )
    if not current_step:
        logger.error("stage_not_found", stage=completed_stage)
        return False

    next_stage = current_step.routing.next_on_success
    if next_stage == "COMPLETE":
        logger.info("flight_plan_complete", plan_id=flight_plan.flight_plan_metadata.plan_id)
        return True

    # Step 3: Find next step definition
    next_step = next(
        (s for s in flight_plan.steps if s.stage == next_stage), None
    )
    if not next_step:
        logger.error("next_stage_not_found", next_stage=next_stage)
        return False

    # Step 4: Look up service URL
    registry = flight_plan.service_registry
    service_url = getattr(registry, next_step.service, None)
    if not service_url:
        logger.error("service_not_in_registry", service=next_step.service)
        return False

    # Step 5: POST to next service
    target_url = f"{service_url}{next_step.endpoint}"
    payload = {
        "flight_plan": flight_plan.model_dump(),
        **(additional_payload or {}),
    }

    try:
        async with httpx.AsyncClient(timeout=TIMEOUT_SECONDS) as client:
            response = await client.post(target_url, json=payload)
            response.raise_for_status()
            logger.info(
                "hand_off_success",
                from_stage=completed_stage,
                to_stage=next_stage,
                service=next_step.service,
                url=target_url,
            )
            return True
    except Exception as e:
        logger.error(
            "hand_off_failed",
            from_stage=completed_stage,
            to_stage=next_stage,
            service=next_step.service,
            error=str(e),
        )
        return False
```

---

#### `shared/communication-layer/retry_handler.py`
```python
"""
BIAS Standard Retry Handler
Provides consistent retry logic across all services.
"""
import asyncio
from typing import Any, Callable, Optional, Type

import structlog

logger = structlog.get_logger()


async def with_retry(
    func: Callable,
    max_attempts: int = 3,
    delay_seconds: float = 1.0,
    backoff_multiplier: float = 2.0,
    exceptions: tuple = (Exception,),
    service_name: str = "UNKNOWN",
    operation_name: str = "UNKNOWN",
) -> Any:
    """
    Executes a function with exponential backoff retry.

    Args:
        func: Async callable to retry
        max_attempts: Maximum number of attempts
        delay_seconds: Initial delay between retries
        backoff_multiplier: Multiplier for each retry delay
        exceptions: Exception types that trigger a retry
        service_name: Service name for logging
        operation_name: Operation name for logging

    Returns:
        Result of the function call

    Raises:
        Last exception if all retries exhausted
    """
    last_exception: Optional[Exception] = None
    delay = delay_seconds

    for attempt in range(1, max_attempts + 1):
        try:
            return await func()
        except exceptions as e:
            last_exception = e
            if attempt < max_attempts:
                logger.warning(
                    "retry_attempt",
                    service=service_name,
                    operation=operation_name,
                    attempt=attempt,
                    max_attempts=max_attempts,
                    retry_in_seconds=delay,
                    error=str(e),
                )
                await asyncio.sleep(delay)
                delay *= backoff_multiplier
            else:
                logger.error(
                    "retry_exhausted",
                    service=service_name,
                    operation=operation_name,
                    attempts=max_attempts,
                    error=str(e),
                )

    raise last_exception  # type: ignore
```

---

#### `shared/schemas/flight_plan_v1.json`
```json
{
  "$schema": "http://json-schema.org/draft-07/schema#",
  "title": "BIAS Flight Plan v1.0",
  "type": "object",
  "required": [
    "flight_plan_metadata",
    "execution_state",
    "service_registry",
    "steps",
    "context_payload"
  ],
  "properties": {
    "flight_plan_metadata": {
      "type": "object",
      "required": ["plan_id", "request_id", "version", "created_at", "request_type"],
      "properties": {
        "plan_id": { "type": "string", "format": "uuid" },
        "request_id": { "type": "string" },
        "version": { "type": "string", "enum": ["1.0"] },
        "created_at": { "type": "string", "format": "date-time" },
        "request_type": {
          "type": "string",
          "enum": ["CLAIM_AUDIT", "DOC_ANONYMIZATION", "CLAIM_STATUS"]
        }
      }
    },
    "execution_state": {
      "type": "object",
      "required": ["overall_status", "current_stage", "total_stages"],
      "properties": {
        "overall_status": {
          "type": "string",
          "enum": ["IN_PROGRESS", "COMPLETED", "FAILED_RETRYING", "FAILED"]
        },
        "current_stage": { "type": "integer", "minimum": 0 },
        "total_stages": { "type": "integer", "minimum": 1 },
        "last_updated": { "type": "string", "format": "date-time" }
      }
    },
    "service_registry": {
      "type": "object",
      "required": [
        "ORCHESTRATOR", "COMMUNICATOR", "FILE_MANAGEMENT",
        "DB_AGENT", "CLAIMS_EXPERT", "LLM_AGENT", "CHATBOT"
      ]
    },
    "steps": {
      "type": "array",
      "minItems": 1,
      "items": {
        "type": "object",
        "required": ["stage", "service", "endpoint", "routing"],
        "properties": {
          "stage": { "type": "integer", "minimum": 1 },
          "service": {
            "type": "string",
            "enum": [
              "ORCHESTRATOR", "COMMUNICATOR", "FILE_MANAGEMENT",
              "DB_AGENT", "CLAIMS_EXPERT", "LLM_AGENT", "CHATBOT"
            ]
          },
          "endpoint": { "type": "string" },
          "status": {
            "type": "string",
            "enum": ["PENDING", "IN_PROGRESS", "COMPLETED", "FAILED", "SKIPPED"]
          },
          "routing": {
            "type": "object",
            "required": ["next_on_success", "next_on_failure"],
            "properties": {
              "next_on_success": {},
              "next_on_failure": { "type": "integer" },
              "callback_agent": { "type": "string" }
            }
          }
        }
      }
    },
    "context_payload": {
      "type": "object",
      "required": ["input_data"],
      "properties": {
        "input_data": {
          "type": "object",
          "required": ["claim_id", "member_id"],
          "properties": {
            "claim_id": { "type": "string" },
            "member_id": { "type": "string" },
            "file_uris": { "type": "array", "items": { "type": "string" } }
          }
        },
        "intermediate_results": { "type": "object" },
        "error_log": { "type": "array" }
      }
    }
  }
}
```

---

### PER-SERVICE TEMPLATES

Generate the following for EACH of the 7 services.
Replace {SERVICE_NAME}, {PORT}, {OWNER}, {DESCRIPTION} with values from the service map.

---

#### `{service}/Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy shared layer
COPY ../shared ./shared

# Copy service code
COPY . .

# Non-root user for security
RUN useradd -m -u 1000 biasuser && chown -R biasuser:biasuser /app
USER biasuser

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:{PORT}/health || exit 1

EXPOSE {PORT}

CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "{PORT}"]
```

---

#### `{service}/requirements.txt`
```
# BIAS Standard Base Requirements
# Do not remove any of these without team consensus

# Framework
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
pydantic-settings==2.1.0

# HTTP Client
httpx==0.26.0

# Logging
structlog==24.1.0

# Testing
pytest==7.4.4
pytest-asyncio==0.23.3
pytest-cov==4.1.0

# Code Quality (dev only but kept unified)
black==23.12.1
isort==5.13.2
flake8==7.0.0
mypy==1.8.0
bandit==1.7.6
```

---

#### `{service}/api/main.py`
```python
"""
BIAS {SERVICE_NAME} — FastAPI Application Entry Point
Port: {PORT}
Owner: {OWNER}
"""
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

from shared.communication_layer.app_factory import create_app

# Import all route modules
# from api.routes import example_routes

app = create_app(
    service_name="{SERVICE_NAME}",
    version="1.0.0",
    description="{DESCRIPTION}",
)

# Register routes
# app.include_router(example_routes.router, prefix="/api/v1", tags=["{SERVICE_NAME}"])
```

---

#### `{service}/.env.example`
```bash
# {SERVICE_NAME} Service Environment Variables
# Subset of root .env.example relevant to this service

ENVIRONMENT=development
LOG_LEVEL=INFO

# This service
{SERVICE_UPPER}_PORT={PORT}

# Internal token (required for all internal calls)
INTERNAL_SERVICE_TOKEN=change-me-internal-token

# Add service-specific variables below
```

---

### SERVICE SKILL FILES

Generate the following `.claude/SKILL.md` for each service.
These are read by Claude Code when working on each service.

---

#### `orchestrator/.claude/SKILL.md`
```markdown
# Orchestrator Service — Claude Code Skill File

## Identity
- Name: ORCHESTRATOR
- Port: 8001
- Owner: Lead Architect
- Category: Brain / Control Tower

## Exact Responsibility
The Orchestrator is a pure logic engine.
It creates Flight Plans and manages service health.
It holds NO business logic and NO claim data.

## What This Service Does
1. Receives plan creation requests from Communicator
2. Selects correct business template based on request_type
3. Queries service registry for healthy service addresses
4. Injects addresses into Flight Plan steps
5. Persists Flight Plan via DB Agent
6. Runs health probes on all services every 30 seconds
7. Handles Stage 99 recovery requests
8. Exposes system metrics for BI dashboard

## What This Service Must NEVER Do
- Process or inspect claim document content
- Hold claim state in memory (always persist via DB Agent)
- Make direct database calls (always via DB Agent)
- Call LLM Agent directly
- Hardcode any service URL

## API Endpoints to Implement
- POST /plan/create
- POST /plan/{plan_id}/stage/update
- GET  /plan/{plan_id}/status
- POST /plan/{plan_id}/recover
- POST /registry/register
- GET  /registry
- GET  /metrics
- GET  /health

## Services This Service Calls
- DB Agent: persist/load Flight Plans, write audit logs, save registry
- All services: GET /health for health probes

## Services That Call This Service
- Communicator: POST /plan/create
- Any service: POST /plan/{id}/stage/update (stage commits)
- Any service: POST /plan/{id}/recover (Stage 99)

## Flight Plan Handling
- Read flight_plan_v1.json schema before building any plan
- Always populate service_registry from live registry (not hardcoded)
- Always persist plan to DB Agent before returning to Communicator
- Recovery logic lives in health_monitor/monitor.py

## Error Handling
- Every exception must be logged via DB Agent /logs/audit
- Every recovery attempt must update Flight Plan overall_status
- Health probe failures must update registry status immediately

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use FlightPlan model from shared.models.flight_plan
- Use BaseResponse, ErrorResponse from shared.models.response
- All functions must have type hints
- All functions must have docstrings
- Minimum 80% test coverage
```

---

#### `communicator/.claude/SKILL.md`
```markdown
# Communicator Service — Claude Code Skill File

## Identity
- Name: COMMUNICATOR
- Port: 8000
- Owner: Backend Dev
- Category: External Gateway

## Exact Responsibility
The Communicator is the ONLY service exposed to the outside world.
It validates, packages, and routes. Nothing more.

## What This Service Does
1. Exposes external FastAPI endpoints to .NET applications
2. Validates JWT on every inbound external request
3. Enforces rate limiting per client
4. Uploads files to object storage immediately on receipt
5. Calls Orchestrator to create a Flight Plan
6. Tracks claim progress via session store
7. Returns 202 Accepted immediately to caller
8. Receives callback from Chatbot when processing completes
9. Makes result available for polling

## What This Service Must NEVER Do
- Contain any business logic
- Inspect or process claim content
- Make routing decisions (Orchestrator does this)
- Call DB Agent, LLM Agent, File Management, Claims Expert, or Chatbot directly
- Store files on local disk (always object storage)
- Hardcode any service URL

## API Endpoints to Implement
External:
- POST /api/v1/claims/submit
- GET  /api/v1/claims/{request_id}/status
- GET  /api/v1/claims/history
- GET  /api/v1/claims/{request_id}/report
- GET  /api/v1/health

Internal:
- POST /internal/v1/callback
- GET  /internal/v1/health

## JWT Validation Rules
- Validate on every external endpoint
- Use JWT_SECRET_KEY from environment
- Return 401 with standard ErrorResponse if invalid
- Never log token values

## Rate Limiting Rules
- Per X-Client-ID header
- Default: 100 requests per minute
- Return 429 with retry_after_s field if exceeded

## Session Tracking
- In-memory dict for Phase 1
- Key: request_id, Value: {plan_id, claim_id, status, result}
- TTL: 24 hours
- Never persist session data to disk

## Error Handling
- 503 if Orchestrator unreachable (circuit break immediately)
- 400 for validation failures (return field-level errors)
- All errors use ErrorResponse from shared.models.response

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use Claim model from shared.models.claim
- Use BaseResponse, ErrorResponse from shared.models.response
- All functions must have type hints and docstrings
- Minimum 80% test coverage
```

---

#### `db-agent/.claude/SKILL.md`
```markdown
# DB Agent Service — Claude Code Skill File

## Identity
- Name: DB_AGENT
- Port: 8003
- Owner: DB Specialist
- Category: Data Domain

## Exact Responsibility
The DB Agent is the ONLY service that touches any database.
All other services request data through this service.
No other service has database credentials.

## What This Service Does
1. Routes data requests to correct database (Legacy, DWH, Vector, Logging)
2. Stores OCR extraction results from File Management
3. Fetches authorization and coverage records for Claims Expert
4. Returns member claim history for Claims Expert and Chatbot
5. Translates natural language queries to SQL for Chatbot
6. Writes all audit log entries for all services
7. Persists and loads the Orchestrator service registry

## What This Service Must NEVER Do
- Expose raw database credentials to any other service
- Accept or execute raw SQL from other services
- Return un-sanitized data that contains PII to unauthorized callers
- Call LLM Agent, File Management, Claims Expert, or Chatbot
- Skip writing to the audit log when requested

## API Endpoints to Implement
- POST /claims/store
- POST /authorization/fetch
- POST /claims/history
- POST /query/nl
- POST /logs/audit
- POST /registry/save
- GET  /registry/load
- GET  /health

## Database Routing Rules
- OCR results → Vector DB + Legacy DB
- Authorization data → Legacy DB
- Claim history → Legacy DB
- NL2SQL queries → Legacy DB or DWH
- Audit logs → Logging DB
- Registry → Logging DB

## NL2SQL Safety Rules
- Whitelist of allowed tables only
- No DELETE, UPDATE, DROP, ALTER allowed
- Sanitize all user input before translation
- Log every NL2SQL query to audit log

## Internal Call Validation
- Validate X-Service-Token header on every request
- Validate X-Service-Name header matches allowed callers
- Return 401 if token invalid

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use BaseResponse, ErrorResponse from shared.models.response
- Each database connector in its own module
- All functions must have type hints and docstrings
- Minimum 80% test coverage
```

---

#### `llm-agent/.claude/SKILL.md`
```markdown
# LLM Agent Service — Claude Code Skill File

## Identity
- Name: LLM_AGENT
- Port: 8005
- Owner: AI Dev
- Category: AI Domain

## Exact Responsibility
The LLM Agent is the ONLY service that holds LLM API keys.
All LLM interactions in BIAS go through this service.
It abstracts providers and governs token usage.

## What This Service Does
1. Receives completion requests from Claims Expert and Chatbot
2. Selects appropriate model based on task_type and preference
3. Sanitizes prompts before sending to any external provider
4. Wraps requests in standardized system prompts per task_type
5. Validates response against expected schema
6. Retries with correction prompt if response malformed
7. Caches common responses to reduce cost
8. Tracks and reports token usage per calling service
9. Falls back to secondary provider on primary failure

## What This Service Must NEVER Do
- Share LLM API keys with any other service
- Accept raw prompts from external (internet-facing) sources
- Skip prompt sanitization (injection defense)
- Allow a single service to exceed token budget
- Log prompt content that contains PII

## API Endpoints to Implement
- POST /api/v1/complete
- POST /api/v1/embed
- GET  /api/v1/models
- GET  /api/v1/usage/report
- GET  /health

## Model Routing Rules
- FAST → DEFAULT_MODEL_FAST from env (simple tasks)
- BALANCED → DEFAULT_MODEL_BALANCED from env (standard tasks)
- POWERFUL → DEFAULT_MODEL_POWERFUL from env (complex reasoning)
- task_type overrides model_preference if conflict

## System Prompt Templates
Located in prompt_engine/templates/:
- summarize.txt → document summarization
- audit.txt → claims reconciliation
- reconcile.txt → data matching
- chat.txt → conversational responses
- extract.txt → entity extraction

## Provider Fallback Order
1. Primary: configured by DEFAULT_MODEL_* env vars
2. Fallback: next provider in router.py fallback chain
3. If all fail: return 503 with ALL_PROVIDERS_UNAVAILABLE

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use BaseResponse, ErrorResponse from shared.models.response
- API keys ONLY loaded from environment variables
- Never log API keys even partially
- All functions must have type hints and docstrings
- Minimum 80% test coverage
```

---

#### `file-management/.claude/SKILL.md`
```markdown
# File Management Service — Claude Code Skill File

## Identity
- Name: FILE_MANAGEMENT
- Port: 8002
- Owner: Backend Dev
- Category: Document Pipeline

## Exact Responsibility
File Management transforms raw documents into
structured, anonymized, translated text artifacts.
It manages the OCR → Anonymize → Translate pipeline.

## What This Service Does
1. Receives file URIs from object storage
2. Downloads and processes files through OCR engine
3. Passes OCR output through Anonymizer (removes PII)
4. Optionally translates anonymized text
5. Validates output integrity at each stage
6. Stores results in object storage
7. Returns job_id immediately (202 pattern)
8. Exposes status polling endpoint

## What This Service Must NEVER Do
- Store files on local disk permanently
- Pass non-anonymized data to any external translation engine
- Call DB Agent, LLM Agent, Claims Expert, or Chatbot
- Return PII-containing text in API responses
- Skip anonymization even if translation is not needed

## Pipeline Order (STRICT — never change)
1. Download file from object storage
2. Run OCR extraction
3. Run Anonymization (ALWAYS before translation)
4. Run Translation (if requested)
5. Validate output integrity (count pages, check text loss)
6. Upload results to object storage
7. Return output URIs

## Fallback Rules
- If Translator fails: return Anonymized-only result (partial success)
- If Anonymizer fails: STOP — do not proceed to translation
- If OCR fails: STOP — raise to Stage 99

## API Endpoints to Implement
- POST /api/v1/process
- GET  /api/v1/process/status/{job_id}
- GET  /api/v1/extract/{claim_id}
- GET  /health

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use BaseResponse, AcceptedResponse from shared.models.response
- Job state stored in memory (dict keyed by job_id) for Phase 1
- All functions must have type hints and docstrings
- Minimum 80% test coverage
```

---

#### `claims-expert/.claude/SKILL.md`
```markdown
# Claims Expert Service — Claude Code Skill File

## Identity
- Name: CLAIMS_EXPERT
- Port: 8004
- Owner: Claims Dev
- Category: Business Reasoning

## Exact Responsibility
Claims Expert is the reasoning engine of BIAS.
It reconciles OCR data against authorization records
and produces the Master Summary that drives decisions.

## What This Service Does
1. Receives audit requests from Orchestrator
2. Fetches OCR text from File Management
3. Fetches authorization records from DB Agent
4. Fetches member claim history from DB Agent
5. Calls LLM Agent to summarize each document
6. Calls LLM Agent to reconcile OCR vs authorization
7. Detects discrepancies and assigns severity
8. Generates Master Summary with decision
9. Stores report in object storage
10. Returns audit_id immediately (202 pattern)
11. Hands off to Chatbot via Flight Plan on completion

## What This Service Must NEVER Do
- Call LLM providers directly (always via LLM Agent)
- Access databases directly (always via DB Agent)
- Store claim data permanently (use object storage for reports)
- Return PII in API responses
- Make final approval decisions without reconciliation data

## API Endpoints to Implement
- POST /api/v1/audit
- GET  /api/v1/audit/status/{audit_id}
- GET  /api/v1/summary/{claim_id}
- POST /api/v1/validate/policy
- GET  /health

## Decision Logic
- APPROVED: within_policy=true AND discrepancies=none or LOW only
- PENDING_REVIEW: within_policy=true AND discrepancies=MEDIUM
- REJECTED: within_policy=false OR discrepancies=HIGH

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use execute_hand_off from shared.communication_layer.hand_off
- Use FlightPlan model from shared.models.flight_plan
- Use BaseResponse, AcceptedResponse from shared.models.response
- All functions must have type hints and docstrings
- Minimum 80% test coverage
```

---

#### `chatbot/.claude/SKILL.md`
```markdown
# Chatbot Service — Claude Code Skill File

## Identity
- Name: CHATBOT
- Port: 8006
- Owner: Frontend Dev
- Category: User Interface

## Exact Responsibility
Chatbot is the conversational interface for all users.
It formats technical results into human language
and handles real-time user queries.

## What This Service Does
1. Receives formatted audit result from Claims Expert
2. Calls LLM Agent to adapt tone to user_type
3. Formats discrepancies as readable list
4. Triggers callback to Communicator with final result
5. Handles real-time chat messages from users
6. Classifies user intent via LLM Agent
7. Routes intent to correct service for data
8. Enforces user-level authorization on all data
9. Manages conversation sessions

## What This Service Must NEVER Do
- Display un-anonymized PII to any user
- Allow a MEMBER user to see another member's data
- Call databases directly (always via DB Agent)
- Call LLM providers directly (always via LLM Agent)
- Store conversation history permanently without TTL

## API Endpoints to Implement
- POST /api/v1/format
- POST /api/v1/chat
- GET  /api/v1/chat/history/{session_id}
- POST /api/v1/chat/session
- GET  /health

## Intent Classification Map
- STATUS_CHECK → Orchestrator /plan/{id}/status
- HISTORY_QUERY → DB Agent /claims/history
- POLICY_QUERY → Claims Expert /validate/policy
- DOCUMENT_REQUEST → File Management /extract/{claim_id}
- GENERAL_QUESTION → LLM Agent /complete (no data fetch)

## Tone Rules per user_type
- ADJUSTER: technical detail, include discrepancy codes, amounts
- MEMBER: plain language, no codes, focus on outcome and next steps
- ADMIN: full detail, include all metadata and audit trail

## Session Management
- In-memory dict for Phase 1
- Key: session_id, Value: {user_id, user_type, messages, context}
- TTL: SESSION_TTL_HOURS from environment
- Never log message content that contains PII

## Coding Standards
- Use create_app() from shared.communication_layer.app_factory
- Use get_logger() from shared.communication_layer.logger
- Use execute_hand_off from shared.communication_layer.hand_off
- Use FlightPlan model from shared.models.flight_plan
- Use BaseResponse, SuccessResponse from shared.models.response
- All functions must have type hints and docstrings
- Minimum 80% test coverage
```

---

### GITHUB ACTIONS

---

#### `.github/workflows/pr-checks.yml`
```yaml
name: BIAS PR Checks

on:
  pull_request:
    branches: [main, develop]

jobs:

  convention-check:
    name: Code Convention Check
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install quality tools
        run: |
          pip install black isort flake8 mypy bandit

      - name: Black formatting check
        run: black --check .

      - name: isort import check
        run: isort --check-only .

      - name: Flake8 lint check
        run: flake8 .

      - name: MyPy type check
        run: mypy shared/

      - name: Bandit security scan
        run: bandit -c pyproject.toml -r . --exclude tests/

  test-coverage:
    name: Test Coverage Check
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service:
          - orchestrator
          - communicator
          - db-agent
          - llm-agent
          - file-management
          - claims-expert
          - chatbot
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python 3.11
        uses: actions/setup-python@v4
        with:
          python-version: "3.11"

      - name: Install dependencies
        run: |
          pip install -r ${{ matrix.service }}/requirements.txt

      - name: Run tests with coverage
        run: |
          cd ${{ matrix.service }}
          pytest --cov=. --cov-fail-under=80 --cov-report=term-missing

  secret-scan:
    name: Secret Detection
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          fetch-depth: 0

      - name: TruffleHog secret scan
        uses: trufflesecurity/trufflehog@main
        with:
          path: ./
          base: ${{ github.event.repository.default_branch }}
          head: HEAD

  build-check:
    name: Docker Build Check
    runs-on: ubuntu-latest
    strategy:
      matrix:
        service:
          - orchestrator
          - communicator
          - db-agent
          - llm-agent
          - file-management
          - claims-expert
          - chatbot
    steps:
      - uses: actions/checkout@v4

      - name: Build Docker image
        run: |
          docker build -t bias-${{ matrix.service }}:pr-check \
            ./${{ matrix.service }}/
```

---

#### `.github/PULL_REQUEST_TEMPLATE.md`
```markdown
## Description
What does this PR do? (required)

## Service(s) Affected
- [ ] orchestrator
- [ ] communicator
- [ ] db-agent
- [ ] llm-agent
- [ ] file-management
- [ ] claims-expert
- [ ] chatbot
- [ ] shared

## Type of Change
- [ ] feat — new feature
- [ ] fix — bug fix
- [ ] docs — documentation only
- [ ] refactor — no feature or fix
- [ ] test — adding tests
- [ ] chore — tooling or config
- [ ] security — security fix

## Pre-merge Checklist
- [ ] I ran `make format` before pushing
- [ ] I ran `make lint` and fixed all issues
- [ ] I ran `make test` and coverage is >= 80%
- [ ] I updated the relevant API contract in docs/api-contracts/
- [ ] I updated the service README.md if needed
- [ ] No credentials or API keys in the code
- [ ] No hardcoded service URLs
- [ ] All new functions have type hints
- [ ] All new functions have docstrings

## Testing Done
Describe how you tested this change.

## Related Issues
Closes #
```

---

## 5. SETUP COMMANDS TO RUN AFTER CREATING ALL FILES

Run these commands in order after generating all files:

```bash
# 1. Initialize git repository
git init
git branch -M main

# 2. Install pre-commit
pip install pre-commit

# 3. Install hooks
pre-commit install
pre-commit install --hook-type commit-msg

# 4. Install dev tools
pip install black isort flake8 mypy bandit pytest pytest-asyncio pytest-cov structlog httpx pydantic fastapi

# 5. Copy env template
cp .env.example .env

# 6. Initial commit
git add .
git commit -m "chore(ci): initial BIAS project scaffold"

# 7. Verify structure
make help
```

---

## 6. CODING RULES FOR ALL FUTURE WORK

These rules apply to every task in every service, forever:

```
1.  Read the service .claude/SKILL.md first
2.  Read docs/api-contracts/{service}.md second
3.  Read shared/models/ before writing any model
4.  Use create_app() — never instantiate FastAPI() directly
5.  Use get_logger() — never use print() or logging.basicConfig()
6.  Use shared response models — never create custom response shapes
7.  Use execute_hand_off() — never make next-stage calls manually
8.  Never hardcode any URL — always read from environment or Flight Plan
9.  Never put credentials in code — always from environment variables
10. Never commit to main directly — always via PR
11. Never merge a PR with failing checks
12. Never skip writing tests — 80% coverage is a hard floor
13. Never log PII — mask or omit sensitive fields
14. Always update API contract docs when changing endpoints
15. Always add docstrings and type hints to every function
```

---

## 7. DO NOT DO LIST

```
DO NOT create any file outside the structure defined above
DO NOT rename any service or change any port number
DO NOT add Flask, Django, or any other web framework
DO NOT instantiate FastAPI() directly in any service
DO NOT write raw SQL in any service other than db-agent
DO NOT call LLM APIs from any service other than llm-agent
DO NOT store credentials anywhere except .env
DO NOT commit .env to git
DO NOT write print() statements — use get_logger()
DO NOT skip the shared communication layer
DO NOT create custom response models per service
DO NOT merge failing PRs
```

---

*End of BIAS CLAUDE.md — Version 1.0*
*This file is the ground truth for the entire project.*
*Update this file when architecture decisions change.*
