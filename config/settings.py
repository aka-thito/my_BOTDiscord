# Importanto el sistema operativo
import os
from dotenv import load_dotenv 

# Carga variables del .env
load_dotenv()

# Configuracion de constantes del bot
TOKEN = os.getenv("TOKEN")
PREFIX = "!"