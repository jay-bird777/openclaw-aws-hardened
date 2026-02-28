import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN", "").strip()
ALLOWED_CHANNEL_ID = os.getenv("DISCORD_ALLOWED_CHANNEL_ID", "").strip()

intents = discord.Intents.default()
intents.message_content = True  # must be enabled in Discord Dev Portal too
bot = commands.Bot(command_prefix="!", intents=intents)

def allowed(ctx):
    return (not ALLOWED_CHANNEL_ID) or (str(ctx.channel.id) == str(ALLOWED_CHANNEL_ID))

@bot.event
async def on_ready():
    print(f"[agent] logged in as {bot.user} ✅")

@bot.command()
async def ping(ctx):
    if not allowed(ctx): return
    await ctx.send("pong ✅")

@bot.command()
async def helpme(ctx):
    if not allowed(ctx): return
    await ctx.send("Commands: !ping, !helpme")

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("[agent] DISCORD_BOT_TOKEN missing")
    bot.run(TOKEN)
