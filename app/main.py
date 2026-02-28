import os
import discord
from discord.ext import commands

TOKEN = os.getenv("DISCORD_BOT_TOKEN", "").strip()
ALLOWED_CHANNEL_ID = os.getenv("DISCORD_ALLOWED_CHANNEL_ID", "").strip()

intents = discord.Intents.default()
intents.message_content = True  # required for prefix commands
bot = commands.Bot(command_prefix="!", intents=intents)

def channel_allowed(ctx: commands.Context) -> bool:
    return (not ALLOWED_CHANNEL_ID) or (str(ctx.channel.id) == str(ALLOWED_CHANNEL_ID))

@bot.event
async def on_ready():
    print(f"[agent] logged in as {bot.user} ✅")

@bot.command()
async def ping(ctx: commands.Context):
    if not channel_allowed(ctx):
        return
    await ctx.send("pong ✅")

@bot.command()
async def status(ctx: commands.Context):
    if not channel_allowed(ctx):
        return
    await ctx.send("Clawbot agent online ✅")

if __name__ == "__main__":
    if not TOKEN:
        raise SystemExit("[agent] DISCORD_BOT_TOKEN missing")
    bot.run(TOKEN)
