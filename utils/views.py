import discord
from utils.data_management import set_default_twitch_channel

class ConfirmView(discord.ui.View):
    def __init__(self, interaction, twitch_id, channel_name, cog):
        super().__init__(timeout=60)
        self.interaction = interaction
        self.twitch_id = twitch_id
        self.channel_name = channel_name
        self.cog = cog

    @discord.ui.button(label="✅ Confirm", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        set_default_twitch_channel(self.interaction.guild.id, self.twitch_id)
        await self.interaction.followup.send(
            f"✅ Default Twitch channel set to **{self.channel_name}**).",
            ephemeral=True
        )
        self.stop()

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.interaction.followup.send("❌ Operation cancelled.", ephemeral=True)
        self.stop()
