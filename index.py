import asyncio
import discord
from discord.ext import commands
from config.intents import get_intents
from config.loader import load_commands, load_events
from config.logging_config import setup_logging
from config.settings import PREFIX, TEST_GUILD_ID, TOKEN

# Ejecucion y guardado de logs
logger = setup_logging()
# Constante de intents para el bot
INTENTS = get_intents()
# Creacion del bot con el prefijo y los intents definidos
bot = commands.Bot(command_prefix = PREFIX, intents = INTENTS)

# Evento que se ejecuta cuando el bot se conecta a Discord
@bot.event
async def on_ready():
    try:
        # Si se define un ID de servidor de pruebas
        if TEST_GUILD_ID:
            # 
            guild = discord.Object(id = TEST_GUILD_ID)
            synced = await bot.tree.sync(guild = guild)
            logger.info(
                "Se sincronizaron %d comandos en el servidor de pruebas %s",
                len(synced),
                TEST_GUILD_ID,
            )
        else:
            synced = await bot.tree.sync()
            logger.info("Se sincronizaron %d comandos globalmente", len(synced))
    except Exception as error:
        logger.error("Error al sincronizar comandos: %s", error)

    logger.info("Conectado como %s", bot.user)


async def main():
    async with bot:
        await load_commands(bot)
        await load_events(bot)
        await bot.start(TOKEN)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    logger.info("Bot apagado manualmente")
