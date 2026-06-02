"""
Claude-powered chat terminal for db-agent.
Usage: python -m db-agent.terminal.chat   (from repo root)
       python chat.py                      (from db-agent/terminal/)
"""
import json
import os

import anthropic
import httpx

BASE_URL = os.getenv("DB_AGENT_URL", "http://localhost:8003")
SERVICE_TOKEN = os.getenv("INTERNAL_SERVICE_TOKEN", "dev-token")
_HEADERS = {
    "x-service-token": SERVICE_TOKEN,
    "x-service-name": "terminal",
    "Content-Type": "application/json",
}

TOOLS = [
    {
        "name": "fetch_claim_history",
        "description": (
            "Fetch all historical claims for a member from the legacy PostgreSQL database. "
            "Use when the user asks about a member's past claims."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "member_id": {"type": "string", "description": "The member ID to look up"},
            },
            "required": ["member_id"],
        },
    },
    {
        "name": "fetch_authorization",
        "description": (
            "Fetch the authorization and coverage record for a specific claim. "
            "Use when the user asks whether a claim was authorized or what coverage applies."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "claim_id": {"type": "string", "description": "The claim ID to look up"},
            },
            "required": ["claim_id"],
        },
    },
    {
        "name": "store_claim",
        "description": (
            "Store OCR extraction results for a claim in the database. "
            "Use when the user wants to record extracted data for a claim."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "claim_id": {"type": "string"},
                "ocr_data": {
                    "type": "object",
                    "description": "Key/value pairs extracted from the claim document",
                },
            },
            "required": ["claim_id", "ocr_data"],
        },
    },
    {
        "name": "nl_query",
        "description": (
            "Translate a natural language question to SQL and execute it safely. "
            "Only SELECT queries are allowed. "
            "target_db choices: LEGACY (on-premise PostgreSQL), DWH (data warehouse), VECTOR (vector store)."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "The natural language question"},
                "target_db": {
                    "type": "string",
                    "enum": ["LEGACY", "DWH", "VECTOR"],
                    "description": "Which database to query",
                },
            },
            "required": ["query", "target_db"],
        },
    },
    {
        "name": "write_audit_log",
        "description": (
            "Write an audit log entry to the logging database. "
            "Use when the user wants to record an event or action."
        ),
        "input_schema": {
            "type": "object",
            "properties": {
                "plan_id": {"type": "string"},
                "stage": {"type": "integer"},
                "service": {"type": "string"},
                "event_type": {"type": "string"},
                "message": {"type": "string"},
                "error_code": {"type": "string"},
            },
            "required": ["plan_id", "stage", "service", "event_type", "message"],
        },
    },
]

SYSTEM = """\
You are a data assistant for BIAS — an insurance claims processing platform.
You interface exclusively with the db-agent service (port 8003), which is the
only component authorised to touch any database.

Your tools let you:
- Look up a member's full claim history
- Fetch authorization and coverage for a specific claim
- Store OCR extraction results for a claim
- Run natural-language SELECT queries against LEGACY, DWH, or VECTOR databases
- Write audit log entries

Rules:
- Always call a tool to fetch real data; never guess or fabricate results.
- When an endpoint returns 501, tell the user that feature is not yet implemented.
- Be concise and factual. Present data in readable plain text or a short table.
- If the user's intent is ambiguous, ask one clarifying question before calling a tool.\
"""


def _call_tool(name: str, inputs: dict) -> str:
    route_map = {
        "fetch_claim_history": ("POST", "/claims/history"),
        "fetch_authorization": ("POST", "/authorization/fetch"),
        "store_claim": ("POST", "/claims/store"),
        "nl_query": ("POST", "/query/nl"),
        "write_audit_log": ("POST", "/logs/audit"),
    }
    if name not in route_map:
        return json.dumps({"error": f"unknown tool: {name}"})

    method, path = route_map[name]
    try:
        with httpx.Client(base_url=BASE_URL, headers=_HEADERS, timeout=30.0) as http:
            resp = http.request(method, path, json=inputs)
    except httpx.ConnectError:
        return json.dumps({"error": f"cannot reach db-agent at {BASE_URL} — is it running?"})

    if resp.status_code == 501:
        return json.dumps({"status": 501, "note": "endpoint not yet implemented"})
    try:
        return json.dumps(resp.json(), ensure_ascii=False)
    except Exception:
        return json.dumps({"status": resp.status_code, "body": resp.text[:500]})


def _fmt_tool_result(result: str) -> str:
    truncated = result if len(result) <= 300 else result[:300] + "…"
    return truncated


def run() -> None:
    client = anthropic.Anthropic()
    messages: list[dict] = []

    print("╔══════════════════════════════════════════╗")
    print("║     BIAS  ·  DB-Agent  ·  Claude CLI     ║")
    print("╠══════════════════════════════════════════╣")
    print(f"║  db-agent : {BASE_URL:<29}║")
    print("║  type 'exit' to quit                     ║")
    print("╚══════════════════════════════════════════╝\n")

    while True:
        try:
            user_input = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nBye.")
            break

        if not user_input:
            continue
        if user_input.lower() in ("exit", "quit", "bye"):
            print("Bye.")
            break

        messages.append({"role": "user", "content": user_input})

        # agentic loop — keep going until Claude stops calling tools
        while True:
            with client.messages.stream(
                model="claude-opus-4-7",
                max_tokens=4096,
                thinking={"type": "adaptive"},
                system=SYSTEM,
                tools=TOOLS,
                messages=messages,
            ) as stream:
                print("Claude: ", end="", flush=True)
                for chunk in stream.text_stream:
                    print(chunk, end="", flush=True)
                response = stream.get_final_message()

            print()  # newline after streamed text

            # preserve full content (including tool_use blocks) in history
            messages.append({"role": "assistant", "content": response.content})

            if response.stop_reason != "tool_use":
                break

            # execute every tool Claude requested
            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                print(f"\n  → {block.name}({json.dumps(block.input, ensure_ascii=False)})")
                result = _call_tool(block.name, block.input)
                print(f"  ← {_fmt_tool_result(result)}\n")
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": result,
                })

            messages.append({"role": "user", "content": tool_results})

        print()


if __name__ == "__main__":
    run()
