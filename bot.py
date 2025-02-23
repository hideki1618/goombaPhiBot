import discord
from discord.ext import commands
import os
import asyncio

from config import DISCORD_TOKEN

# Define bot with command prefix "/"
intents = discord.Intents.default()
bot = commands.Bot(command_prefix="/", intents=intents)

# Load all cogs dynamically
COG_DIRECTORY = "cogs"

async def load_cogs():
    for filename in os.listdir(COG_DIRECTORY):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            await bot.load_extension(cog_name)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user.name}")
    await bot.tree.sync()  # Sync slash commands
    print("Bot is ready!")

async def main():
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())