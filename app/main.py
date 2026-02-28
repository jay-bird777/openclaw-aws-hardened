import os
import asyncio
import discord

TOKEN = os.getenv("DISCORD_BOT_TOKEN")
ALLOWED_CHANNEL_ID = os.getenv("DISCORD_ALLOWED_CHANNEL_ID")

if ALLOWED_CHANNEL_ID:
    try:
        ALLOWED_CHANNEL_ID = int(ALLOWED_CHANNEL_ID)
    except ValueError:
        ALLOWED_CHANNEL_ID = None

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

def channel_allowed(message):
    if not ALLOWED_CHANNEL_ID:
        return True
    return message.channel.id == ALLOWED_CHANNEL_ID

@client.event
async def on_ready():
    print(f"[agent] Logged in as {client.user}")
    print("[agent] Ready.")

@client.event
async def on_message(message):
    if message.author.bot:
        return

    if not channel_allowed(message):
        return

    content = message.content.strip()

    if content == "!ping":
        await message.channel.send("🏓 pong")

    elif content == "!status":
        await message.channel.send("🟢 Clawbot is online.")

    elif content.startswith("!echo "):
        await message.channel.send(content[6:])

async def heartbeat():
    while True:
        print("[agent] heartbeat…")
        await asyncio.sleep(60)

async def main():
    asyncio.create_task(heartbeat())
    await client.start(TOKEN)

if __name__ == "__main__":
    asyncio.run(main())
