import discord
from discord.ext import commands
from config.embeds import success_embed
from config.error_sender import send
from config.errors import ErrorType


class Moderation_Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Descripcion: Comando para banear a un miembro del servidor
    @commands.command(
            
    name = "ban",
    help = "Banea a un miembro del servidor"

    )

    # Requiere permisos de banear miembros
    @commands.has_permissions(ban_members = True)

    # Definicion de la funcion ban
    async def ban(self, ctx, member: discord.Member, *, reason = None):

        # Si el usuario no proporciona un miembro
        if member is None:
            await send(ctx, ErrorType.USAGE)
            return

        # Si el usuario se me menciona a si mismo
        if member == ctx.author:
            await send(ctx, ErrorType.SELF_ACTION)
            return
        
        # Si el usuario intenta banear al bot
        if member == ctx.guild.me:
            await send(ctx, ErrorType.INVALID_TARGET  )
            return
        
        # Si el miembro tiene un rol superior o igual al del autor
        if member.top_role >= ctx.author.top_role:
            await send(ctx, ErrorType.HIERARCHY)
            return
    
        # Asignacion de razon por defecto si no se proporciona
        reason = reason or "No se proporcionó una razón."

        # Intento de banear al miembro
        try:

            await member.ban(reason=reason)
            await ctx.send(
                embed = success_embed(
                    "Miembro baneado",
                    f"**{member.name}** fue baneado.\n"
                    f"**Razón:** {reason}"
                )

        )

        # Excepcion para el error de permisos del bot
        except discord.Forbidden:
            await send(ctx, ErrorType.BOT_PERMISSIONS)

        # Excepcion para otros errores desconocidos
        except discord.HTTPException:
            await send(ctx, ErrorType.UNKNOWN)
        

async def setup(bot):
    # Agrega el Cog Moderation_Ban al bot
    await bot.add_cog(Moderation_Ban(bot))