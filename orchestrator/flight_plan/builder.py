"""
Flight Plan builder utilities for the Orchestrator.
"""
import json
from pathlib import Path
from typing import Any, Dict

TEMPLATES_DIR = Path(__file__).parent / "templates"


def load_template(template_name: str) -> Dict[str, Any]:
    """Loads a Flight Plan JSON template by name."""
    template_path = TEMPLATES_DIR / f"{template_name}.json"
    with open(template_path) as f:
        return json.load(f)
