import os
import time
import json
import urllib.request

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID", "")
HEARTBEAT_SECONDS = int(os.getenv("HEARTBEAT_SECONDS", "60"))

def send_telegram(text: str) -> None:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        print("[agent] Telegram not configured; skipping message:", text)
        return

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = json.dumps({"chat_id": TELEGRAM_CHAT_ID, "text": text}).encode("utf-8")

    req = urllib.request.Request(
        url,
        data=payload,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    with urllib.request.urlopen(req, timeout=15) as resp:
        body = resp.read().decode("utf-8")
        print("[agent] Telegram response:", body)

def main():
    print("[agent] starting up…")
    send_telegram("✅ OpenClaw agent is online (AWS EC2 + SSM + CloudWatch logs).")

    while True:
        print("[agent] heartbeat…")
        time.sleep(HEARTBEAT_SECONDS)

if __name__ == "__main__":
    main()
