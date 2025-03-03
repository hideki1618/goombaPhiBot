import discord
from discord.ext import commands
from discord import app_commands
from utils.twitch_api import get_twitch_schedule
from utils.data_management import get_default_twitch_channel, get_schedule_message
from config import DISCORD_OWNER_ID, TEST_SERVER_ID

class Sync(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name='sync', description='Owner only')
    @app_commands.guilds(discord.Object(TEST_SERVER_ID))
    @app_commands.describe(install_guild="Guild to install commands to")
    async def sync(self, interaction: discord.Interaction, install_guild: str = None):
        # 🕒 Defer the response immediately
        await interaction.response.defer(ephemeral=True)

        # Check if user is owner
        if interaction.user.id == DISCORD_OWNER_ID:

            # Sync globally
            if install_guild is None:
                try:
                    synced = await self.bot.tree.sync()
                    await interaction.followup.send(f'Command tree synced globally! {len(synced)} commands were synced.', ephemeral=True)
                except Exception as e:
                    await interaction.followup.send(f'Failed to sync commands: {e}', ephemeral=True)

            # Sync to specific guild
            else:
                try:
                    self.bot.tree.copy_global_to(guild=discord.Object(install_guild))
                    synced = await self.bot.tree.sync(guild=discord.Object(install_guild))
                    await interaction.followup.send(f'Command tree synced to guild {install_guild}! {len(synced)} commands were synced.', ephemeral=True)
                except Exception as e:
                    await interaction.followup.send(f'Failed to sync commands: {e}', ephemeral=True)

        else:
            await interaction.followup.send('You must be the owner to use this command!', ephemeral=True)
    
# # Add Cog to bot
async def setup(bot):
    await bot.add_cog(Sync(bot))