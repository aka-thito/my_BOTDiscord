import discord

# Funcion para obtener los intents del bot
def get_intents():

    # Obtengo los intents por defecto
    intents = discord.Intents.default()

    # Intents equivalentes a permisos que tiene el bot
    intents.guilds = True
    intents.messages = True
    intents.message_content = True
    intents.members = True

    # Devuelvo los intents
    return intents
