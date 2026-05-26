# Architecture Decision Records

## ADR-001: REST over gRPC for Phase 1

**Status:** Accepted
**Date:** 2026-05-26

**Context:** Services need to communicate synchronously and asynchronously.

**Decision:** Use REST (HTTP/JSON) for all inter-service communication in Phase 1.

**Rationale:** Simpler debugging, broader tooling support, easier onboarding.
gRPC may be evaluated for Phase 2 high-throughput paths.

---

## ADR-002: Flight Plan as the execution artifact

**Status:** Accepted
**Date:** 2026-05-26

**Context:** Need a way to coordinate multi-step processing across services.

**Decision:** Orchestrator creates a Flight Plan JSON object that travels with every request.
Each service updates its stage and routes to the next.

**Rationale:** Self-describing, traceable, recoverable. Enables Stage 99 error recovery.

---

## ADR-003: Single DB gateway via DB Agent

**Status:** Accepted
**Date:** 2026-05-26

**Context:** Multiple services need data access. Direct DB connections multiply credentials risk.

**Decision:** Only DB Agent holds database credentials. All other services call DB Agent APIs.

**Rationale:** Centralized data access, single point for audit logging, credential isolation.

---

## ADR-004: LLM API key isolation via LLM Agent

**Status:** Accepted
**Date:** 2026-05-26

**Context:** Multiple services need LLM capabilities. API keys must not be distributed.

**Decision:** Only LLM Agent holds provider API keys. All LLM calls go through LLM Agent.

**Rationale:** Token governance, cost tracking, provider abstraction, security isolation.
