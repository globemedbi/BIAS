# DB Agent Service

**Port:** 8003 | **Owner:** DB Specialist | **Category:** Data Domain

## Responsibility
The ONLY service that touches any database. All other services call this service for data.

## Key Files
- `legacy_db/legacy_connector.py` — On-premise PostgreSQL
- `dwh/dwh_connector.py` — Data Warehouse
- `vector_db/vector_connector.py` — Vector storage and search
- `logging_db/logging_connector.py` — Audit log store
- `nl2sql/translator.py` — Safe NL→SQL translation

## Running Locally
```bash
cd db-agent
pip install -r requirements.txt
uvicorn api.main:app --port 8003 --reload
```

## API
See `docs/api-contracts/db-agent.md`
