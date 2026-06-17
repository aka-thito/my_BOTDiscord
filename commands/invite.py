import discord
from discord.ext import commands
from discord import app_commands

class Invite(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="invite",
        description="Obtén el enlace para invitar al bot a tu servidor"
    )
    async def invite(self, interaction: discord.Interaction):

        client_id = self.bot.user.id
        permissions = discord.Permissions(administrator=False)

        invite_link = discord.utils.oauth_url(
            client_id,
            permissions=permissions
        )

        try:
            await interaction.user.send(
                f"Aquí tienes el enlace para invitarme a otro servidor:\n{invite_link}"
            )

            await interaction.response.send_message("Te envié el enlace por mensaje privado.", ephemeral=True)

        except discord.Forbidden:
            if interaction.response.is_done():
                await interaction.followup.send(
                    "❌ No pude enviarte el mensaje privado. ¿Tienes los DMs cerrados?",
                    ephemeral=True
                )
            else:
                await interaction.response.send_message(
                    "❌ No pude enviarte el mensaje privado. ¿Tienes los DMs cerrados?",
                    ephemeral=True
                )

    @invite.error
    async def invite_error(self, interaction: discord.Interaction, error):
        if interaction.response.is_done():
            send = interaction.followup.send
        else:
            send = interaction.response.send_message

        if isinstance(error, app_commands.MissingPermissions):
            await send("❌ No tienes permisos para usar este comando.", ephemeral=True)
        elif isinstance(error, discord.Forbidden):
            await send("❌ No tengo permisos para enviar mensajes.", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await send("❌ Error al enviar el mensaje. Inténtalo de nuevo más tarde.", ephemeral=True)
        else:
            await send("❌ Error inesperado al ejecutar /invite.", ephemeral=True)

async def setup(bot):
    # Agrega el Cog Invite al bot
    await bot.add_cog(Invite(bot))
