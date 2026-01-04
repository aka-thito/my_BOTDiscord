import discord

#Colores estandar para los embeds
SUCCESS_COLOR = discord.Color.green() # Verde para exito
ERROR_COLOR = discord.Color.red() # Rojo para errores
INFO_COLOR = discord.Color.blurple() # Azul para informacion
WARNING_COLOR = discord.Color.orange() # Naranja para advertencias

def success_embed(title, description = None):

    embed = discord.Embed(
        title = title,
        description = description,
        color = SUCCESS_COLOR       
    )
    
    return embed

def error_embed(title, description = None):

    embed = discord.Embed(
        title = title,
        description = description,
        color = ERROR_COLOR       
    )
    
    return embed

def info_embed(title, description = None):

    embed = discord.Embed(
        title = title,
        description = description,
        color = INFO_COLOR       
    )
    
    return embed

def warning_embed(title, description = None):

    embed = discord.Embed(
        title = title,
        description = description,
        color = WARNING_COLOR       
    )
    
    return embed

