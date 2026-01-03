import discord
from discord.ext import commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="invite")
    async def invite(self, ctx):
        # ID del bot
        client_id = self.bot.user.id

        # Permisos básicos (puedes cambiarlos)
        permissions = discord.Permissions(administrator=False)
        invite_link = discord.utils.oauth_url(
            client_id,
            permissions=permissions
        )

        # Enviar DM
        try:
            await ctx.author.send(
                f"🤖 Aquí tienes el enlace para invitarme a otro servidor:\n{invite_link}"
            )
            await ctx.send("📩 Te envié el enlace por mensaje privado.")
        except discord.Forbidden:
            await ctx.send(
                "❌ No pude enviarte el mensaje privado. ¿Tienes los DMs cerrados?"
            )

async def setup(bot):
    await bot.add_cog(Invite(bot))
