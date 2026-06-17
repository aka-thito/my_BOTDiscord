import traceback
import discord
from discord.ext import commands
from config.error_handler import log_exception
from discord import app_commands

class AppCommandErrors(commands.Cog):
    """Global handler for app command errors that logs traceback and notifies user."""

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error: Exception):
        # Log full exception and context
        await log_exception(error, interaction, context_text="on_app_command_error")

        # If the interaction wasn't responded to, send an ephemeral message to avoid "The application did not respond"
        try:
            if not interaction.response.is_done():
                # Provide concise message to user and point to logs
                await interaction.response.send_message(
                    "❌ Ocurrió un error interno al ejecutar el comando. Revisa la consola del bot para más detalles.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "❌ Ocurrió un error interno al ejecutar el comando. Revisa la consola del bot para más detalles.",
                    ephemeral=True
                )
        except Exception:
            # If even sending fails, just print
            traceback.print_exc()


async def setup(bot):
    await bot.add_cog(AppCommandErrors(bot))
