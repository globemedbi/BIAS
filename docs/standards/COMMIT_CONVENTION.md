# BIAS Commit Convention

Format: `type(scope): subject`

## Types
- `feat` — new feature
- `fix` — bug fix
- `docs` — documentation only
- `refactor` — no feature or fix
- `test` — adding or updating tests
- `chore` — tooling, config, dependencies
- `security` — security fix

## Scopes
`orchestrator`, `communicator`, `db-agent`, `llm-agent`,
`file-management`, `claims-expert`, `chatbot`, `shared`,
`infrastructure`, `docs`, `ci`

## Rules
- Subject max 72 characters
- Body lines max 100 characters
- No commit to `main` directly (enforced by pre-commit hook)

## Examples
```
feat(claims-expert): add discrepancy severity classification
fix(communicator): handle JWT expiry edge case on clock skew
docs(shared): update flight plan spec with Stage 99 detail
chore(ci): upgrade black to 24.x
security(db-agent): sanitize NL2SQL input before translation
```
