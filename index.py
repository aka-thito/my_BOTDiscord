# Importacion de librerias para el INDEX del bot 
import asyncio
from discord.ext import commands

# Importacion de Variables y Funciones dentro de los modulos
from config.settings import TOKEN, PREFIX
from config.intents import get_intents
from config.loader import load_commands, load_events

# Asigno una constante a la funcion para poder ejecutarla
INTENTS = get_intents()

bot = commands.Bot(
    command_prefix = PREFIX, # Asignacion de Prefix
    intents = INTENTS # Asignacion de permisos
    )


# Arraque del BOT
async def main():
    async with bot:
        # Cargar comandos por medio de la funcion load_commands
        await load_commands(bot)

        # Cargar eventos
        await load_events(bot)

        # Inicia Sesión del bot
        await bot.start(TOKEN)


#Ejecuta el bot y una excepcion para cuando se apaga
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("El Bot fue apagado manualemnte") 
