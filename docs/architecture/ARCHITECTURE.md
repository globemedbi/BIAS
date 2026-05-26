# BIAS Architecture

## Overview

BIAS (BI Agentic System) is a distributed microservices system for claims processing.
Seven independent services communicate via REST APIs, coordinated by the Orchestrator
using a Flight Plan artifact that travels with every request.

## Services

| Service          | Port | Role                   |
|------------------|------|------------------------|
| orchestrator     | 8001 | Brain / Control Tower  |
| communicator     | 8000 | External Gateway       |
| db-agent         | 8003 | Data Domain            |
| llm-agent        | 8005 | AI Domain              |
| file-management  | 8002 | Document Pipeline      |
| claims-expert    | 8004 | Business Reasoning     |
| chatbot          | 8006 | User Interface         |

## Request Flow

1. External caller → Communicator (JWT validated, 202 Accepted returned)
2. Communicator → Orchestrator (Flight Plan created)
3. Orchestrator → File Management (OCR + Anonymize + Translate)
4. File Management → Claims Expert (Audit + Reconcile)
5. Claims Expert → Chatbot (Format + Deliver)
6. Chatbot → Communicator (Callback with result)

## Flight Plan

The Flight Plan is a JSON artifact created by the Orchestrator that defines
every step of a claim's journey. Each service reads its step, executes, updates
the plan, and hands off to the next service. See `shared/schemas/flight_plan_v1.json`.
