import discord
from utils.twitch_api import get_twitch_schedule
from discord.ext import commands
from discord import app_commands
import nest_asyncio
import asyncio

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="schedule", description="Fetch the Twitch schedule for a channel.")
    @app_commands.describe(channel_name="Twitch channel name", schedule_limit="Number of upcoming streams to fetch")
    async def fetch_schedule(self, interaction: discord.Interaction, channel_name: str, schedule_limit: int = 1):
        """
        Fetches and displays the Twitch schedule for a given channel.
        """
        await interaction.response.defer()  # Prevents "This interaction failed" error
        nest_asyncio.apply()
        schedule_message = asyncio.run(get_twitch_schedule(channel_name,schedule_limit))
        await interaction.followup.send(f"🎶 This Week's {channel_name} Streams🎶\n{schedule_message}")

# Add Cog to bot
async def setup(bot):
    await bot.add_cog(Schedule(bot))