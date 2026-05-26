# Claims Expert Service

**Port:** 8004 | **Owner:** Claims Dev | **Category:** Business Reasoning

## Responsibility
The reasoning engine of BIAS. Reconciles OCR data against authorization records
and produces the Master Summary that drives claim decisions.

## Key Files
- `auditor/auditor.py` — Decision logic (APPROVED/PENDING_REVIEW/REJECTED)
- `reconciler/reconciler.py` — OCR vs authorization comparison
- `medical_logic/medical_rules.py` — Policy/coverage rule engine
- `agent/claims_agent.py` — Full audit workflow

## Decision Rules
- `APPROVED`: within_policy=true + no/LOW discrepancies
- `PENDING_REVIEW`: within_policy=true + MEDIUM discrepancy
- `REJECTED`: within_policy=false OR HIGH discrepancy

## Running Locally
```bash
cd claims-expert
pip install -r requirements.txt
uvicorn api.main:app --port 8004 --reload
```

## API
See `docs/api-contracts/claims-expert.md`
