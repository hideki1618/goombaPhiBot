import logging
import discord
from discord.ext import commands
import os
import asyncio
from server import run_server 

from config import DISCORD_TOKEN

# Configure logging
logging.basicConfig(
    level=logging.INFO,  # Set to DEBUG for more details
    format="%(asctime)s [%(levelname)s]: %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
)

logger = logging.getLogger(__name__)

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
            logger.info(f"Loaded cog: {cog_name}")

@bot.event
async def on_ready():
    logger.info(f"Logged in as {bot.user.name}")
    await bot.tree.sync()  # Sync slash commands
    logger.info("Bot is ready!")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    if interaction.command:
        """Log whenever a user interacts with a slash command."""
        logger.info(f"Command used: /{interaction.command.name} by {interaction.user} in {interaction.guild}")
    
@bot.event
async def on_command_error(interaction: discord.Interaction, error):
    logger.error(f"Error in command /{interaction.command.name}: {error}")

async def main():
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, run_server)
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

asyncio.run(main())