"""
Quick test — sends the PRC_UPDATE_ATTACHMENT_SUMMARY payload through the full
db-agent chain (registry check → dispatch → Oracle callproc).
Run: python test_update_summary.py
"""
import asyncio, json, os, sys

sys.path.insert(0, ".")
sys.path.insert(0, "..")

# load .env
with open(".env") as f:
    for line in f:
        line = line.strip()
        if line and not line.startswith("#") and "=" in line:
            k, v = line.split("=", 1)
            os.environ[k.strip()] = v.strip()


async def main():
    from agent.db_agent import db_agent

    payload = {
        "claim_id":        "A0000001",
        "attachment_name": "9999999_test_insert.pdf",
        "version":         1,
        "summary_json":    json.dumps({
            "document_type": "Test File",
            "status":        "Verified",
            "short_summary": "This is a generated summary of the test document to verify the CLOB update logic.",
        }),
    }

    print("Route  : pkg_procedure:PKG_AGENT_INSERT_CLAIM.PRC_UPDATE_ATTACHMENT_SUMMARY")
    print("Payload:", json.dumps(payload, indent=2))
    print()

    result = await db_agent.handle(
        route="pkg_procedure:PKG_AGENT_INSERT_CLAIM.PRC_UPDATE_ATTACHMENT_SUMMARY",
        payload=payload,
        token=os.environ["INTERNAL_SERVICE_TOKEN"],
        service_name="test-cli",
    )

    print("Result:", result)


asyncio.run(main())
