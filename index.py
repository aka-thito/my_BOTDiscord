"""# Importacion de librerias para el INDEX del bot 
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
    
# Si se presiona Ctrl+C para apagar el bot
except KeyboardInterrupt:
    print("El Bot fue apagado manualemnte") """

import asyncio
import discord
from discord.ext import commands

from config.settings import TOKEN, PREFIX, TEST_GUILD_ID
from config.intents import get_intents
from config.loader import load_commands, load_events

INTENTS = get_intents()

bot = commands.Bot(
    command_prefix=PREFIX,
    intents=INTENTS
)


@bot.event
async def on_ready():

    try:
        if TEST_GUILD_ID:
            guild = discord.Object(id=TEST_GUILD_ID)
            synced = await bot.tree.sync(guild=guild)
            print(
                f"[SLASH] Se sincronizaron {len(synced)} comandos en el servidor de pruebas {TEST_GUILD_ID}."
            )
        else:
            synced = await bot.tree.sync()
            print(
                f"[SLASH] Se sincronizaron {len(synced)} comandos globalmente."
            )

    except Exception as error:
        print(
            f"[SLASH] Error al sincronizar "
            f"comandos: {error}"
        )

    print(
        f"[BOT] Conectado como "
        f"{bot.user}"
    )


async def main():

    async with bot:

        await load_commands(bot)

        await load_events(bot)

        await bot.start(TOKEN)


try:
    asyncio.run(main())

except KeyboardInterrupt:
    print("El Bot fue apagado manualmente")
