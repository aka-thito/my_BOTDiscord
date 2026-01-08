import discord
from discord.ext import commands
from config.embeds import success_embed
from config.errors import ErrorType
from config.error_handler import handle_error

class ModerationKick(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Descripcion: Comando para expulsar a un miembro del servidor
    @commands.command(
            
        name = "kick",
        help = "Expulsa a un miembro del servidor",
        signature = "<miembro> [razón]"

    )

    # Requiere permisos de expulsión
    @commands.has_permissions(kick_members = True)
    
    # Definicion de la funcion kick
    async def kick(self, ctx, member: discord.Member, *, reason = None):

        # Si el usuario se me menciona a si mismo
        if member == ctx.author:
            await handle_error(ctx, ErrorType.SELF_ACTION)
            return
        
        # Si el miembro tiene un rol superior o igual al del autor
        if member.top_role >= ctx.author.top_role:
            await handle_error(ctx, ErrorType.HIERARCHY)
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
            await handle_error(ctx, ErrorType.BOT_PERMISSIONS)

        # Excepcion para otros errores desconocidos
        except discord.HTTPException:
            await handle_error(ctx, ErrorType.UNKNOWN)

    # Manejo de errores para el comando kick
    @kick.error
    async def kick_error(self, ctx, error):

        # Si el usuario genera un error de argumento faltante
        if isinstance(error, commands.MissingRequiredArgument):
            await handle_error(ctx, ErrorType.USAGE)

        # Si el usuario proporciona un miembro inválido
        elif isinstance(error, commands.BadArgument):
            await handle_error(ctx, ErrorType.INVALID_MEMBER)

        # Si el usuario no tiene permisos suficientes
        elif isinstance(error, commands.MissingPermissions):
            await handle_error(ctx, ErrorType.PERMISSIONS)
        
        # Si el bot no tiene permisos suficientes
        elif isinstance(error, commands.BotMissingPermissions):
            await handle_error(ctx, ErrorType.BOT_PERMISSIONS)
        
        # Para otros errores desconocidos
        else:
            await handle_error(ctx, ErrorType.UNKNOWN)

async def setup(bot):
    # Agrega el Cog ModerationKick al bot
    await bot.add_cog(ModerationKick(bot))

