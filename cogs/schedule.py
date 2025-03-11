import discord
from discord.ext import commands
from discord import app_commands
from utils.twitch_api import get_twitch_schedule
from utils.data_management import get_default_twitch_channel, get_schedule_message
import nest_asyncio
import asyncio

class Schedule(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="schedule", description="Publish the Twitch schedule for the channel associated with this server.")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(schedule_limit="Number of upcoming streams to fetch")
    async def fetch_schedule(self, interaction: discord.Interaction, schedule_limit: int = 1):
        """
        Fetches and displays the Twitch schedule for a given channel.
        """
        # 🕒 Defer the response immediately
        await interaction.response.defer()  # Prevents "This interaction failed" error

        # Validate schedule limit
        if schedule_limit < 1:
            await interaction.response.send_message(
                "⚠️ The schedule limit must be at least 1.",
                ephemeral=True
            )
            return
        
        # Fetch default Twitch channel for this server
        channel_id = get_default_twitch_channel(interaction.guild.id)
        if channel_id is None:
            await interaction.response.send_message(
                "⚠️ No default Twitch channel set for this server. Please set one using `/setchannel`.",
                ephemeral=True
            )
            return
        
        # Fetch Twitch schedule
        nest_asyncio.apply()
        schedule_string = asyncio.run(get_twitch_schedule(channel_id,schedule_limit))
        if schedule_string is None:
            await interaction.followup.send("⚠️ No upcoming streams found.")
            return
        
        # Fetch schedule message
        schedule_message = get_schedule_message(interaction.guild.id)
        if schedule_message is None:
            schedule_message = f"🎶 This Week's Streams🎶"

        # Send the schedule message
        await interaction.followup.send(f"{schedule_message}\n{schedule_string}",
                                        allowed_mentions=discord.AllowedMentions(everyone=True, roles=True))

# Add Cog to bot
async def setup(bot):
    await bot.add_cog(Schedule(bot))