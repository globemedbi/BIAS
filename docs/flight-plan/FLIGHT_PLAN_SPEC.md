# Flight Plan Specification v1.0

## Overview

The Flight Plan is a JSON artifact created by the Orchestrator at the start of every
claim request. It defines every processing step, tracks execution state, carries
context data, and routes the request through the BIAS service pipeline.

## Schema

See `shared/schemas/flight_plan_v1.json` for the full JSON Schema.
See `shared/models/flight_plan.py` for the Pydantic model.

## Lifecycle

1. **Created** by Orchestrator from a business template
2. **Populated** with live service URLs from the registry
3. **Persisted** to DB Agent before first hand-off
4. **Updated** at each stage: status, timestamps, output_uri
5. **Completed** when routing returns `"COMPLETE"`
6. **Recovered** via Stage 99 on unrecoverable failure

## Stage Routing

Each step defines:
```json
{
  "routing": {
    "next_on_success": 2,
    "next_on_failure": 99,
    "callback_agent": null
  }
}
```

- `next_on_success`: stage number or `"COMPLETE"`
- `next_on_failure`: always `99` (recovery stage)
- `callback_agent`: optional service to notify on completion

## Stage 99 — Recovery

Stage 99 is a reserved error recovery stage. When any service fails, it calls:
`POST /plan/{plan_id}/recover` on the Orchestrator with the failure details.

The Orchestrator then:
1. Updates `overall_status` to `FAILED_RETRYING`
2. Logs the error via DB Agent
3. Attempts to re-run from the last successful stage
4. If recovery fails, sets `overall_status` to `FAILED`

## Templates

Business-specific Flight Plan templates live in `orchestrator/flight_plan/templates/`:
- `claim_audit.json` — full OCR → audit → format pipeline
- `doc_anonymization.json` — OCR → anonymize only pipeline
