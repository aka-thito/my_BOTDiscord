import traceback

import discord
from discord.ext import commands

from config.error_handler import log_exception


class AppCommandErrors(commands.Cog):
    """Global handler for app command errors that logs traceback and notifies user."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: Exception):
        await log_exception(error, interaction, context_text="on_app_command_error")

        # Send ephemeral message if interaction wasn't responded to
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "❌ Ocurrió un error interno. Revisa la consola del bot para más detalles.",
                    ephemeral=True,
                )
            else:
                await interaction.followup.send(
                    "❌ Ocurrió un error interno. Revisa la consola del bot para más detalles.",
                    ephemeral=True,
                )
        except Exception:
            # If even sending fails, just print
            traceback.print_exc()


async def setup(bot):
    await bot.add_cog(AppCommandErrors(bot))
