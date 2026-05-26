# LLM Agent Service

**Port:** 8005 | **Owner:** AI Dev | **Category:** AI Domain

## Responsibility
The ONLY service that holds LLM API keys. All LLM interactions go through this service.

## Key Files
- `model_router/router.py` — Model selection logic
- `prompt_engine/prompt_builder.py` — Template-based prompts
- `prompt_engine/templates/` — System prompt templates
- `token_governance/governor.py` — Per-service token tracking

## Running Locally
```bash
cd llm-agent
pip install -r requirements.txt
uvicorn api.main:app --port 8005 --reload
```

## API
See `docs/api-contracts/llm-agent.md`
