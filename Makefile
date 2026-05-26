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
