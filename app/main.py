import os
import time
import json
import urllib.request

DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL", "")
HEARTBEAT_SECONDS = int(os.getenv("HEARTBEAT_SECONDS", "60"))

def send_discord(message: str):
    if not DISCORD_WEBHOOK_URL:
        print("[agent] Discord not configured.")
        return

    data = json.dumps({"content": message}).encode("utf-8")

    req = urllib.request.Request(
        DISCORD_WEBHOOK_URL,
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        print("[agent] Discord response:", resp.read().decode())

def main():
    print("[agent] starting up…")
    send_discord("✅ OpenClaw AWS agent is online.")

    while True:
        print("[agent] heartbeat…")
        time.sleep(HEARTBEAT_SECONDS)

if __name__ == "__main__":
    main()
