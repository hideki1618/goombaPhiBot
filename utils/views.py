import discord
from utils.data_management import set_default_twitch_channel
from google.cloud.exceptions import GoogleCloudError

class ConfirmView(discord.ui.View):
    def __init__(self, interaction, twitch_id, channel_name, cog):
        super().__init__(timeout=60)
        self.interaction = interaction
        self.twitch_id = twitch_id
        self.channel_name = channel_name
        self.cog = cog
        self.original_message = None  # Store original message

    async def on_timeout(self):
        """This method will be triggered when the view times out."""
        for btn in self.children:
            btn.disabled = True
        if self.original_message:
            await self.original_message.edit(view=self)

    @discord.ui.button(label="✅ Confirm", style=discord.ButtonStyle.success)
    async def confirm(self, interaction: discord.Interaction, button: discord.ui.Button):
        try:
            await interaction.response.defer(ephemeral=True)

            set_default_twitch_channel(self.interaction.guild.id, self.twitch_id)

            await self.interaction.followup.send(
                f"✅ Default Twitch channel set to **{self.channel_name}**.",
                ephemeral=True
            )

            # Disable the buttons after confirmation
            for btn in self.children:
                btn.disabled = True

            # Edit the original message to reflect the disabled buttons
            if self.original_message:
                await self.original_message.edit(view=self)

        except GoogleCloudError as e:
            # Catch general Firestore errors
            await interaction.response.send_message(f"❌ Error updating database: {e}", ephemeral=True)
            return
        
        self.stop()

    @discord.ui.button(label="❌ Cancel", style=discord.ButtonStyle.danger)
    async def cancel(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer(ephemeral=True)

        await self.interaction.followup.send("❌ Operation cancelled.", ephemeral=True)

        # Disable the buttons after confirmation
        for btn in self.children:
            btn.disabled = True

        # Edit the original message to reflect the disabled buttons
        if self.original_message:
            await self.original_message.edit(view=self)

        self.stop()

    async def interaction_check(self, interaction: discord.Interaction) -> bool:
        """Ensure that only the user who initiated the interaction can respond."""
        if interaction.user != self.interaction.user:
            await interaction.response.send_message("You cannot interact with this message.", ephemeral=True)
            return False
        return True

    async def start(self, message):
        """Set the original message reference."""
        self.original_message = message

