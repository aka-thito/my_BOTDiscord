# Importacion de librerias para el INDEX del bot 
import discord
import asyncio
from discord.ext import commands

# Importacion de Variables y Funciones dentro de los modulos
from config.settings import TOKEN, PREFIX
from config.intents import get_intents
from config.loader import load_commands

# Asigno una constante a la funcion para poder ejecutarla
INTENTS = get_intents()

ready = commands.Bot(
    command_prefix = PREFIX, # Asignacion de Prefix
    intents = INTENTS # Asignacion de permisos
    )

# Evento Ready
@ready.event
async def on_ready():
    print(f'{ready.user} Esta Funcionando')

# Arraque del BOT
async def main():
    async with ready:
        # Cargar comandos automátiamente
        await load_commands(ready)

        # Inicia Sesión del bot
        await ready.start(TOKEN)


#Ejecuta el bot y una excepcion para cuando se apaga
try:
    asyncio.run(main())
except KeyboardInterrupt:
    print("El Bot fue apagado manualemnte") 
