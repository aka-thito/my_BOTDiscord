import discord
from discord.ext import commands
from discord import app_commands


def is_owner_check():
    async def predicate(interaction: discord.Interaction):
        app_info = await interaction.client.application_info()
        return interaction.user.id == app_info.owner.id
    return app_commands.check(predicate)


class Reload(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="reload",
        description="Recarga todas las extensiones y sincroniza los Slash Commands"
    )
    @is_owner_check()
    async def reload(
        self,
        interaction: discord.Interaction
    ):

        await interaction.response.defer(ephemeral=True)

        success = 0
        failed = 0

        # Recorre todas las extensiones cargadas
        for extension in list(self.bot.extensions):

            try:
                await self.bot.reload_extension(extension)

                print(
                    f"[RELOAD] Extensión recargada: "
                    f"{extension}"
                )

                success += 1

            except Exception as error:

                print(
                    f"[RELOAD] Error recargando "
                    f"{extension}: {error}"
                )

                failed += 1

        # Sincroniza nuevamente los Slash Commands
        try:

            synced = await self.bot.tree.sync()

            await interaction.followup.send(
                f"✅ Recarga completada.\n\n"
                f"📦 Extensiones recargadas: {success}\n"
                f"❌ Extensiones con error: {failed}\n"
                f"🌳 Slash Commands sincronizados: {len(synced)}",
                ephemeral=True
            )

        except Exception as error:

            print(
                f"[SLASH] Error al sincronizar: "
                f"{error}"
            )

            await interaction.followup.send(
                f"⚠️ Las extensiones fueron recargadas, "
                f"pero ocurrió un error al sincronizar "
                f"los Slash Commands.\n\n"
                f"Error: {error}",
                ephemeral=True
            )

    @reload.error
    async def reload_error(self, interaction: discord.Interaction, error):
        # Loggear la excepcion completa para poder debuggear desde la terminal
        try:
            from config.error_handler import log_exception
            await log_exception(error, interaction, context_text="reload_error")
        except Exception:
            import traceback
            traceback.print_exc()

        if interaction.response.is_done():
            send = interaction.followup.send
        else:
            send = interaction.response.send_message

        if isinstance(error, app_commands.CheckFailure):
            await send(
                "❌ Este comando solo puede ser usado por el propietario del bot.",
                ephemeral=True
            )
        elif isinstance(error, discord.Forbidden):
            await send(
                "❌ No tengo permisos suficientes para completar la recarga.",
                ephemeral=True
            )
        elif isinstance(error, discord.HTTPException):
            await send(
                "❌ Error de red al ejecutar la recarga. Inténtalo de nuevo.",
                ephemeral=True
            )
        else:
            await send(
                "❌ Error inesperado al ejecutar /reload.",
                ephemeral=True
            )


async def setup(bot):
    await bot.add_cog(Reload(bot))
