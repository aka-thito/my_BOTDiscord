from discord.ext import commands
from config.loader import load_commands, load_events

class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Command para recargar los comandos y eventos del bot
    @commands.command(
            # Constantes del comando para su descripcion
            name = "reload",
            help = "Recarga los comandos y eventos del bot"
            )
    # Solo el dueño del bot puede usar este comando
    @commands.is_owner()

    # La funcion del comando
    async def reload(self, ctx):

        # Mensaje de recarga iniciada
        await ctx.send("Recargando comandos y eventos...")

        # 
        for extension in list(self.bot.extensions):
            #
            await self.bot.unload_extension(extension)

        # 
        await load_commands(self.bot)
        await load_events(self.bot)

        await ctx.send("Comandos y eventos recargados.")

# Funcion para agregar el Cog al bot
async def setup(bot):
    await bot.add_cog(Reload(bot))
