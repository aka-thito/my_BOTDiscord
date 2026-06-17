import discord
from discord.ext import commands
from discord import app_commands
from config.embeds import success_embed
from config.errors import ErrorType
from config.error_handler import handle_error

class ModerationKick(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name = "kick",
        description = "Expulsa a un miembro del servidor"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, interaction: discord.Interaction, member: discord.Member, reason: str = None):

        # Si el usuario se menciona a si mismo
        if member == interaction.user:
            await handle_error(interaction, ErrorType.SELF_ACTION)
            return
        
        # Si el miembro tiene un rol superior o igual al del autor
        if member.top_role >= interaction.user.top_role:
            await handle_error(interaction, ErrorType.HIERARCHY)
            return

        # Asignacion de razon por defecto si no se proporciona
        reason = reason or "No se proporcionó una razón."

        # Intento de expulsar al miembro
        try:
            await interaction.response.defer()
            await member.kick(reason = reason)
            await interaction.followup.send(
                embed = success_embed(
                    "Miembro expulsado",
                    f"**{member.name}** fue expulsado.\n"
                    f"**Razón:** {reason}"
                )
            )

        # Excepcion para el error de permisos del bot
        except discord.Forbidden:
            await handle_error(interaction, ErrorType.BOT_PERMISSIONS)

        # Excepcion para otros errores desconocidos
        except discord.HTTPException:
            await handle_error(interaction, ErrorType.UNKNOWN)

    @commands.Cog.listener()
    async def on_app_command_error(self, interaction: discord.Interaction, error):
        if not interaction.command:
            return
        if interaction.command.name != "kick":
            return

        from discord import app_commands as _ac
        if isinstance(error, _ac.MissingPermissions) or isinstance(error, commands.MissingPermissions):
            await handle_error(interaction, ErrorType.PERMISSIONS)
        else:
            await handle_error(interaction, ErrorType.UNKNOWN)

async def setup(bot):
    # Agrega el Cog ModerationKick al bot
    await bot.add_cog(ModerationKick(bot))
