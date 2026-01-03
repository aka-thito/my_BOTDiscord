# Importacion de librerias para el INDEX del bot 
import os
import discord

# Importacion de Variables y Funciones dentro de los modulos
from dotenv import load_dotenv
from config.settings import TOKEN
from config.intents import get_intents

# asigno una constante a la funcion para poder ejecutarla
INTENTS = get_intents()

client = discord.Client(intents = INTENTS)

@client.event
async def on_ready():
    print(f'{client.user} Esta Funcionando')


client.run(TOKEN)
