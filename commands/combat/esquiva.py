import discord
from discord.ext import commands
from discord import app_commands

from config.combat_manager import get_active_combat, resolve_response
from config.embeds import error_embed, info_embed
from config.settings import COMBAT_LOG_CHANNEL_ID


def _build_resolucion_embed(combat_id: str, accion: str, respondedor_id: str, resultado: str, siguiente_id: str) -> discord.Embed:
    embed = info_embed(
        f"💨 ESQUIVA — {combat_id}",
        f"<@{respondedor_id}>: \"{accion}\""
    )
    embed.add_field(name="Resultado", value=resultado, inline=False)
    embed.add_field(name="Siguiente turno", value=f"<@{siguiente_id}> para atacar", inline=False)
    return embed


class Esquiva(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="esquiva", description="Esquiva el ataque de tu oponente")
    @app_commands.describe(accion="Describe cómo esquivas")
    async def esquiva(self, interaction: discord.Interaction, accion: str):
        await interaction.response.defer()

        user_id = str(interaction.user.id)
        combat_id, combat = get_active_combat(user_id)

        if combat is None:
            await interaction.followup.send(
                embed=error_embed("Sin combate", "No estás en ningún combate activo."),
                ephemeral=True
            )
            return

        if combat["turno_actual"] != user_id:
            await interaction.followup.send(
                embed=error_embed("No es tu turno", "Espera a que tu oponente realice su acción."),
                ephemeral=True
            )
            return

        if combat["fase"] != "respuesta":
            await interaction.followup.send(
                embed=error_embed("Fase incorrecta", "No hay un ataque pendiente al que responder."),
                ephemeral=True
            )
            return

        try:
            resultado, combat_actualizado = resolve_response(combat_id, user_id, "esquiva", accion)
        except KeyError:
            await interaction.followup.send(
                embed=error_embed("Error", "No se encontraron las estadísticas de uno de los combatientes."),
                ephemeral=True
            )
            return
        except Exception as e:
            print(f"[ESQUIVA] Error al resolver: {e}")
            await interaction.followup.send(
                embed=error_embed("Error inesperado", "Ocurrió un error al procesar la esquiva."),
                ephemeral=True
            )
            return

        try:
            log_channel = self.bot.get_channel(COMBAT_LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(
                    embed=_build_resolucion_embed(
                        combat_id, accion, user_id, resultado, combat_actualizado["turno_actual"]
                    )
                )
        except Exception as e:
            print(f"[ESQUIVA] Error al enviar log: {e}")

        await interaction.followup.send(
            embed=info_embed("Esquiva registrada", resultado)
        )


async def setup(bot):
    await bot.add_cog(Esquiva(bot))
