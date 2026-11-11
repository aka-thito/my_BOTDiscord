import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Registro de constantes para la configuración del logging
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "bot.log"
LOG_MAX_BYTES = 5 * 1024 * 1024
LOG_BACKUP_COUNT = 3

# Funcion setup_logging
def setup_logging() -> logging.Logger:

    # Crear el directorio de logs si no existe
    LOG_DIR.mkdir(exist_ok = True)

    # Configuración del logger
    logger = logging.getLogger("bot")
    logger.setLevel(logging.DEBUG)

    # Evitar que los mensajes se propaguen a otros loggers
    if logger.handlers:
        return logger

    # Configuración del formateador y los manejadores de logging
    formatter = logging.Formatter(
        # Formato de log: [Fecha y hora] Nivel de log Nombre del logger — Mensaje
        "[%(asctime)s] %(levelname)-8s %(name)s — %(message)s",
        datefmt = "%Y-%m-%d %H:%M:%S",
    )

    # Configuración del manejador de archivos con rotación
    file_handler = RotatingFileHandler(
        # Archivo de log
        LOG_FILE,
        # Tamaño máximo del archivo de log antes de rotar
        maxBytes = LOG_MAX_BYTES,
        # Número de archivos de respaldo a mantener
        backupCount = LOG_BACKUP_COUNT,
        # Codificación del archivo de log
        encoding = "utf-8"
    )

    # Configuración del nivel de log
    file_handler.setLevel(logging.DEBUG)
    # Configuración del formateador para el manejador de archivos
    file_handler.setFormatter(formatter)
    # Configuración del manejador de consola
    console_handler = logging.StreamHandler(sys.stdout)
    # Configuración del nivel de log para la consola
    console_handler.setLevel(logging.INFO)
    # Configuración del formateador para el manejador de consola
    console_handler.setFormatter(formatter)
    # Agregar los manejadores al logger
    logger.addHandler(file_handler)
    # Agregar el manejador de consola al logger
    logger.addHandler(console_handler)

    return logger
