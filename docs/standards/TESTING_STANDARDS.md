# BIAS Testing Standards

## Coverage Floor
**80% minimum** on every service. CI will fail below this.

## Framework
- `pytest` with `pytest-asyncio` for async tests
- `pytest-cov` for coverage reporting

## Test File Naming
- Files: `test_<module>.py`
- Functions: `test_<behaviour>`

## What to Test
- Happy path for every endpoint
- Auth failure (401, 429)
- Validation failures (400)
- Service unavailable (503)
- Flight Plan stage update logic
- Hand-off routing logic

## What NOT to Mock
- Do not mock the Flight Plan model — use real instances
- Do not mock structlog — it is safe to use in tests

## Async Tests
```python
import pytest

@pytest.mark.asyncio
async def test_my_endpoint(async_client):
    response = await async_client.post("/endpoint", json={...})
    assert response.status_code == 202
```

## Running Tests
```bash
# All services
make test

# Single service
make test-service s=orchestrator

# With coverage report
cd orchestrator && pytest --cov=. --cov-report=html
```
