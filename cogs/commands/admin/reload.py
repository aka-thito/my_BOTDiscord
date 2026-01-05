from discord.ext import commands
from config.loader import load_commands, load_events

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bloque de informacion sobre el comando reload
    @commands.command(

            name = "reload",
            help = "Recarga los comandos y eventos del bot"

            )
    
    # Solo el dueño del bot puede usar este comando
    @commands.is_owner()

    # La funcion del comando
    async def reload(self, ctx):

        # Mensaje de recarga iniciada
        await ctx.send("Recargando comandos y eventos...")

        # Descargo todas las extensiones cargadas actualmente
        for extension in list(self.bot.extensions):
            # Descargo la extension
            await self.bot.unload_extension(extension)

        # Vuelve a cargar los comandos y eventos
        await load_commands(self.bot)
        # Vuelve a cargar los eventos
        await load_events(self.bot)
        # Mensaje de recarga completada
        await ctx.send("Comandos y eventos recargados.")

async def setup(bot):
    # Agrega el Cog Reload al bot
    await bot.add_cog(Reload(bot))
