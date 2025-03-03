import logging
import discord
from discord.ext import commands
import os
import asyncio
from server import run_server
from config import DISCORD_TOKEN, TEST_SERVER_ID

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
GUILD_ID = discord.Object(TEST_SERVER_ID)

# Directory containing all cogs
COG_DIRECTORY = "cogs"

async def load_cogs():
    """Load all cogs dynamically from the specified directory."""
    for filename in os.listdir(COG_DIRECTORY):
        if filename.endswith(".py"):
            cog_name = f"cogs.{filename[:-3]}"
            await bot.load_extension(cog_name)
            logger.info(f"Loaded cog: {cog_name}")

@bot.event
async def on_ready():
    """Event handler for when the bot is ready."""
    logger.info(f"Logged in as {bot.user.name}")
    try:
        guild = GUILD_ID
        synced = await bot.tree.sync(guild=guild)
        print(f"Synced {len(synced)} commands in {bot.get_guild(guild.id).name}")
    except Exception as e:
        print("Failed to sync commands:", e)
    logger.info("Bot is ready!")

@bot.event
async def on_interaction(interaction: discord.Interaction):
    """Event handler for when a user interacts with a slash command."""
    if interaction.command:
        logger.info(f"Command used: /{interaction.command.name} by {interaction.user} in {interaction.guild}")

@bot.event
async def on_command_error(interaction: discord.Interaction, error):
    """Event handler for when a command error occurs."""
    logger.error(f"Error in command /{interaction.command.name}: {error}")

async def main():
    """Main function to start the bot and run the server."""
    loop = asyncio.get_running_loop()
    loop.run_in_executor(None, run_server)
    async with bot:
        await load_cogs()
        await bot.start(DISCORD_TOKEN)

# Run the main function
asyncio.run(main())