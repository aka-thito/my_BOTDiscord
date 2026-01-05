import discord
from discord.ext import commands

# Define el evento on_ready para el bot
class Ready(commands.Cog):
    
    # Constructor de la clase
    def __init__(self, bot):
        # Asigno el bot a una variable de la clase
        self.bot = bot
    
    # Listener para el evento on_ready
    @commands.Cog.listener()
    # Cuando el bot este listo
    async def on_ready(self):
        # Imprime esto
        print(f"{self.bot.user} Esta online")

# Funcion para agregar el Cog al bot
async def setup(bot):
    # Agrega el Cog Ready al bot
    await bot.add_cog(Ready(bot))
