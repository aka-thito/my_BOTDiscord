import discord

def get_intents():

    intents = discord.Intents.default()

    # Intents equivalentes a permisos que tiene el bot
    intents.guilds = True
    intents.messages = True
    intents.message_content = True
    intents.members = True

    return intents
