# Getting Started with BIAS

## Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Git

## First-Time Setup

```bash
# 1. Clone the repository
git clone <repo-url>
cd BIAS

# 2. Run the setup script (installs hooks, dev tools, copies .env)
make setup

# 3. Fill in .env with real values
# Edit .env — see .env.example for all required variables

# 4. Start all services
make up

# 5. Verify all services are healthy
make health
```

## Directory Structure

```
BIAS/
├── shared/          — Shared models, communication layer, schemas
├── orchestrator/    — Brain: Flight Plan creation and service coordination
├── communicator/    — External gateway: JWT auth, rate limiting
├── db-agent/        — Data domain: all database access
├── llm-agent/       — AI domain: all LLM provider access
├── file-management/ — Document pipeline: OCR, anonymize, translate
├── claims-expert/   — Business reasoning: audit, reconcile, decide
├── chatbot/         — User interface: conversation, formatting
└── infrastructure/  — Docker, Kubernetes, secrets
```

## Working on a Service

1. `cd <service-name>/`
2. Read `.claude/SKILL.md` — service identity, rules, endpoints
3. Read `docs/api-contracts/<service>.md` — API contract
4. Read `shared/models/` — shared data models
5. Start coding

## Running Tests

```bash
make test                        # all services
make test-service s=orchestrator # single service
```

## Code Quality

```bash
make format    # black + isort
make lint      # flake8 + mypy
make security  # bandit
```

## Logs

```bash
make logs                           # all services
make logs-service s=claims-expert   # single service
```
