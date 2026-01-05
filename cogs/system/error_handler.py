import discord
from discord.ext import commands
from config.error_sender import send_error
from config.errors import ErrorType

class ErrorHandler(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):

        # Ignorar errores manejados manualmente
        if hasattr(ctx.command, 'on_error'):
            return

        # Error de permisos del usuario
        if isinstance(error, commands.MissingPermissions):
            await send_error(ctx, ErrorType.PERMISSIONS)

        # Error de permisos del bot
        elif isinstance(error, commands.BotMissingPermissions):
            await send_error(ctx, ErrorType.BOT_PERMISSIONS)

        # Falta un argumento obligatorio
        elif isinstance(error, commands.MissingRequiredArgument):
            await send_error(ctx, ErrorType.USAGE)

        # Argumento inválido (miembro no existe, etc.)
        elif isinstance(error, commands.BadArgument):
            await send_error(ctx, ErrorType.INVALID_MEMBER)

        # Error desconocido
        else:
            await send_error(ctx, ErrorType.UNKNOWN)
            raise error  # 👈 útil en desarrollo

async def setup(bot):
    await bot.add_cog(ErrorHandler(bot))
