# Importanto dependencias o librerias
import os
import re

from dotenv import load_dotenv

# Carga variables del .env
load_dotenv()

# Configuracion de constantes del bot
TOKEN = os.getenv("TOKEN")
PREFIX = "!"

TEST_GUILD_ID = None
_test_guild_env = os.getenv("TEST_GUILD_ID")
if _test_guild_env:
    # Keep only digits (strip '#' or other non-digit chars)
    digits = re.sub(r"\D", "", _test_guild_env)
    TEST_GUILD_ID = int(digits) if digits else None
else:
    TEST_GUILD_ID = None

COMBAT_LOG_CHANNEL_ID = 1518103186651480224
