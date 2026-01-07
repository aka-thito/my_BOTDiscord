import discord
from discord.ext import commands
from config.embeds import success_embed
from config.error_sender import send_error
from config.errors import ErrorType

class ModerationKick(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Descripcion: Comando para expulsar a un miembro del servidor
    @commands.command(
            
        name = "kick",
        help = "Expulsa a un miembro del servidor"

    )

    @commands.has_permissions(kick_members = True)
    
    # Definicion de la funcion kick
    async def kick(self, ctx, member: discord.Member, *, reason = None):

        # Si el usuario se me menciona a si mismo
        if member == ctx.author:
            await send_error(ctx, ErrorType.SELF_ACTION)
            return

        # Asignacion de razon por defecto si no se proporciona
        reason = reason or "No se proporcionó una razón."

        # Intento de expulsar al miembro
        try:

            await member.kick(reason = reason)
            await ctx.send(
                embed = success_embed(
                    "Miembro expulsado",
                    f"**{member.name}** fue expulsado.\n"
                    f"**Razón:** {reason}"
                )

            )

        # Excepcion para el error de permisos del bot
        except discord.Forbidden:
            await send_error(ctx, ErrorType.BOT_PERMISSIONS)

        # Excepcion para otros errores desconocidos
        except discord.HTTPException:
            await send_error(ctx, ErrorType.UNKNOWN)

async def setup(bot):
    # Agrega el Cog ModerationKick al bot
    await bot.add_cog(ModerationKick(bot))

