import os

from config.logging_config import setup_logging

logger = setup_logging()


async def load_events(bot):
    base_path = "events"
    loaded_events = 0

    for file in os.listdir(base_path):
        if file.endswith(".py") and file != "__init__.py":
            module = f"{base_path}.{file[:-3]}"
            await bot.load_extension(module)
            loaded_events += 1

    if loaded_events == 0:
        logger.warning("No se han encontrado Eventos")
    else:
        logger.info("%d eventos cargados correctamente", loaded_events)


async def load_commands(bot, base_path="commands"):
    loaded_commands = 0
    failed_commands = 0

    for root, _, files in os.walk(base_path):
        for file in files:
            if file.endswith(".py") and file != "__init__.py":
                path = os.path.join(root, file)
                module = path.replace("\\", ".").replace("/", ".")[:-3]

                try:
                    await bot.load_extension(module)
                    loaded_commands += 1
                except Exception as error:
                    logger.error("Error al cargar %s: %s", module, error)
                    failed_commands += 1

    if loaded_commands == 0 and failed_commands == 0:
        logger.warning("No se han encontrado comandos")
        return

    logger.info("Comandos cargados correctamente: %d", loaded_commands)
    if failed_commands:
        logger.warning("Comandos con error: %d", failed_commands)
