import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # Bloque de informacion sobre el comando invite
    @commands.command(
            name = "invite",
            help = "Obtén el enlace para invitar al bot a tu servidor"
            )
    
    # Funcion principal del comando invite
    async def invite(self, ctx):

        # ID del bot
        client_id = self.bot.user.id

        # Permisos básicos
        permissions = discord.Permissions(administrator = False)

        # Genera el enlace de invitación
        invite_link = discord.utils.oauth_url(
            client_id,
            permissions = permissions
        )

        # Intenta enviar DM
        try:
            await ctx.author.send(
                f"Aquí tienes el enlace para invitarme a otro servidor:\n{invite_link}"
            )

            # Confirma en el canal que se envió el DM
            await ctx.send("Te envié el enlace por mensaje privado.")
        
        # Si no se puede enviar el mensaje privado
        except discord.Forbidden:
            await ctx.send(
                "❌ No pude enviarte el mensaje privado. ¿Tienes los DMs cerrados?"
            )

async def setup(bot):
    # Agrega el Cog Invite al bot
    await bot.add_cog(Invite(bot))
