# BIAS Coding Standards

## Language & Runtime
- Python 3.11+
- FastAPI for all HTTP services
- Pydantic v2 for all data models
- structlog for all logging

## Mandatory Patterns

### App Creation
```python
from shared.communication_layer.app_factory import create_app
app = create_app(service_name="MY_SERVICE", version="1.0.0")
```
Never: `app = FastAPI()`

### Logging
```python
from shared.communication_layer.logger import get_logger
logger = get_logger("MY_SERVICE")
logger.info("event_name", key=value)
```
Never: `print()`, `logging.basicConfig()`

### Response Models
```python
from shared.models.response import SuccessResponse, ErrorResponse, AcceptedResponse
```
Never: custom response dicts or unstructured returns

### Flight Plan Hand-off
```python
from shared.communication_layer.hand_off import execute_hand_off
await execute_hand_off(flight_plan, completed_stage=2)
```
Never: manual HTTP calls to next service

## Type Hints
All functions must have complete type hints. No `Any` unless unavoidable.

## Docstrings
All public functions must have a one-line docstring minimum.

## Line Length
88 characters (Black default).

## Imports
Sorted by isort with `profile = "black"`.

## Security
- No credentials in code
- No PII in logs
- No hardcoded URLs
- Validate all inputs at service boundaries
