import os
import time
import json
import urllib.request
import urllib.error

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
HEARTBEAT_SECONDS = int(os.getenv("HEARTBEAT_SECONDS", "60"))

def send_discord(message: str) -> None:
    if not DISCORD_WEBHOOK_URL:
        print("[agent] DISCORD_WEBHOOK_URL not set; skipping.")
        return

    data = json.dumps({"content": message}).encode("utf-8")
    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=data,
        headers={"Content-Type": "application/json", "User-Agent": "openclaw-agent/1.0"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            body = resp.read().decode("utf-8", errors="replace")
            print("[agent] Discord OK:", resp.status, body[:200])
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace") if hasattr(e, "read") else ""
        print(f"[agent] Discord HTTPError: {e.code} {e.reason} body={body[:300]}")
    except Exception as e:
        print("[agent] Discord error:", repr(e))

def main():
    print("[agent] starting up…")
    send_discord("✅ OpenClaw AWS agent is online.")

    while True:
        print("[agent] heartbeat…")
        send_discord("💓 OpenClaw heartbeat")
        time.sleep(HEARTBEAT_SECONDS)

if __name__ == "__main__":
    main()
