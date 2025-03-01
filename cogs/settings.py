import discord
from discord import app_commands
from discord.ext import commands
from utils.data_management import set_schedule_message
from utils.twitch_api import get_twitch_user_id
from utils.views import ConfirmView
from google.cloud.exceptions import GoogleCloudError

class Settings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="setchannel", description="Set a default Twitch channel for this server")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(channel_name="The Twitch channel name to set")
    async def set_channel(self, interaction: discord.Interaction, channel_name: str):
        """Command to set the default Twitch channel, storing the Twitch ID instead of the name."""
        # 🕒 Defer the response immediately
        await interaction.response.defer(ephemeral=True)
    
        # Step 1: Fetch Twitch ID based on channel name
        twitch_id, fetched_name = await get_twitch_user_id(channel_name)  # Function should return (ID, display_name)

        if not twitch_id:
            await interaction.followup.send(
                f"⚠️ Could not find a Twitch channel named **{channel_name}**. Please check the name and try again.",
                ephemeral=True
            )
            return
        
        # Step 2: Ask user for confirmation (ephemeral message)
        view = ConfirmView(interaction, twitch_id, fetched_name, self)
        await interaction.followup.send( 
            f"Is **{fetched_name}** the correct Twitch channel?", 
            view=view, 
            ephemeral=True 
        )
        view.original_message = await interaction.original_response()  # Store the message reference

    @app_commands.command(name="setschedulemessage", description="Set a message for the schedule message in this server")
    @app_commands.default_permissions(manage_messages=True)
    @app_commands.describe(schedule_message="The message to set")
    async def set_schedule_message(self, interaction: discord.Interaction, schedule_message: str):
        """Command to set the schedule message for this server."""

        # 🕒 Defer the response immediately
        await interaction.response.defer(ephemeral=True)

        try:
            set_schedule_message(interaction.guild.id, schedule_message)
        except GoogleCloudError as e:
            # Catch general Firestore errors
            await interaction.followup.send(f"❌ Error updating database: {e}", ephemeral=True)
            return
        
        await interaction.followup.send(
            f"✅ Schedule message set to **{schedule_message}**.",
            ephemeral=True
        )
    
async def setup(bot):
    await bot.add_cog(Settings(bot))
