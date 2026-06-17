import discord
from discord.ext import commands
from discord import app_commands

from config.embeds import success_embed
from config.error_handler import handle_error
from config.errors import ErrorType


class Moderation_Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Descripcion de los parametros del comando
    @app_commands.describe(
        member = "El miembro a banear",
        reason = "La razón del baneo"
    )

    # Descripcion: Comando para banear a un miembro del servidor (slash)
    @app_commands.command(
        name = "ban",
        description = "Banea a un miembro del servidor"
    )
    @app_commands.checks.has_permissions(ban_members = True)
    async def ban(self, 
                  interaction: discord.Interaction, 
                  member: discord.Member, 
                  reason: str = None):

        # Si el usuario se menciona a si mismo
        if member == interaction.user:
            await handle_error(interaction, ErrorType.SELF_ACTION)
            return
        
        # Si
        bot_member = interaction.guild.get_member(self.bot.user.id)
        
        # Si el miembro a banear es el bot
        if member == interaction.guild.me:
            await handle_error(interaction, ErrorType.INVALID_TARGET)
            return
        
        # Si el miembro tiene un rol superior o igual al del autor
        if member.top_role >= interaction.user.top_role:
            await handle_error(interaction, ErrorType.HIERARCHY)
            return
    
        # Asignacion de razon por defecto si no se proporciona
        reason = reason or "No se proporcionó una razón."

        # Intento de banear al miembro
        try:
            # Defer in case operation takes time
            await interaction.response.defer()
            await member.ban(reason=reason)
            await interaction.followup.send(
                embed = success_embed(
                    "Miembro baneado",
                    f"**{member.name}** fue baneado.\n"
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
        # Manejo general de errores para comandos de moderación
        if not interaction.command:
            return
        if interaction.command.name != "ban":
            return

        # Mapeo basico de errores a ErrorType
        from discord import app_commands as _ac
        if isinstance(error, _ac.MissingPermissions) or isinstance(error, commands.MissingPermissions):
            await handle_error(interaction, ErrorType.PERMISSIONS)
        else:
            await handle_error(interaction, ErrorType.UNKNOWN)

async def setup(bot):
    # Agrega el Cog Moderation_Ban al bot
    await bot.add_cog(Moderation_Ban(bot))
