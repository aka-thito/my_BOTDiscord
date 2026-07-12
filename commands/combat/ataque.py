import discord
from discord import app_commands
from discord.ext import commands

from config.embeds import error_embed, info_embed
from config.logging_config import setup_logging
from config.settings import COMBAT_LOG_CHANNEL_ID
from services.combat_service import CombatService

logger = setup_logging()
combat_service = CombatService()


def _build_inicio_embed(
    combat_id: str, atacante_id: str, defensor_id: str, accion: str
) -> discord.Embed:
    embed = info_embed(
        f"⚔️ COMBATE INICIADO — {combat_id}", f"<@{atacante_id}> desafía a <@{defensor_id}>"
    )
    embed.add_field(name="Acción", value=f'"{accion}"', inline=False)
    embed.add_field(name="Turno de", value=f"<@{defensor_id}> para responder", inline=False)
    return embed


def _build_ataque_embed(
    combat_id: str, atacante_id: str, defensor_id: str, accion: str
) -> discord.Embed:
    embed = info_embed(f"⚔️ ATAQUE — {combat_id}", f"<@{atacante_id}> ataca a <@{defensor_id}>")
    embed.add_field(name="Acción", value=f'"{accion}"', inline=False)
    embed.add_field(name="Turno de", value=f"<@{defensor_id}> para responder", inline=False)
    return embed


class Ataque(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="ataque", description="Ataca a un oponente o inicia un combate")
    @app_commands.describe(
        accion="Describe tu acción de ataque",
        objetivo="El usuario a atacar (solo al iniciar combate)",
    )
    async def ataque(
        self, interaction: discord.Interaction, accion: str, objetivo: discord.Member = None
    ):
        await interaction.response.defer()

        user_id = str(interaction.user.id)
        combat_id, combat = combat_service.get_active_combat(user_id)

        if combat is None:
            if objetivo is None:
                await interaction.followup.send(
                    embed=error_embed(
                        "Objetivo requerido", "Debes mencionar un usuario para iniciar un combate."
                    ),
                    ephemeral=True,
                )
                return

            if objetivo.id == interaction.user.id:
                await interaction.followup.send(
                    embed=error_embed("Acción inválida", "No puedes atacarte a ti mismo."),
                    ephemeral=True,
                )
                return

            if objetivo.bot:
                await interaction.followup.send(
                    embed=error_embed("Objetivo inválido", "No puedes atacar a un bot."),
                    ephemeral=True,
                )
                return

            defensor_id = str(objetivo.id)

            if not combat_service.get_character(user_id):
                await interaction.followup.send(
                    embed=error_embed("Sin ficha", "Necesitas tener una ficha para combatir."),
                    ephemeral=True,
                )
                return

            defensor_char = combat_service.get_character(defensor_id)
            if not defensor_char:
                await interaction.followup.send(
                    embed=error_embed(
                        "Sin ficha", f"{objetivo.mention} no tiene una ficha de personaje."
                    ),
                    ephemeral=True,
                )
                return

            if combat_service.get_active_combat(defensor_id)[0] is not None:
                await interaction.followup.send(
                    embed=error_embed(
                        "Ya en combate", f"{objetivo.mention} ya está en un combate activo."
                    ),
                    ephemeral=True,
                )
                return

            try:
                combat_id, combat = combat_service.create_combat(
                    str(interaction.guild_id), user_id, defensor_id, accion
                )
            except Exception as e:
                logger.error("Error al crear combate: %s", e)
                await interaction.followup.send(
                    embed=error_embed("Error inesperado", "No se pudo iniciar el combate."),
                    ephemeral=True,
                )
                return

            try:
                log_channel = self.bot.get_channel(COMBAT_LOG_CHANNEL_ID)
                if log_channel:
                    await log_channel.send(
                        embed=_build_inicio_embed(combat_id, user_id, defensor_id, accion)
                    )
            except Exception as e:
                logger.error("Error al enviar log: %s", e)

            await interaction.followup.send(
                embed=info_embed(
                    "Combate iniciado",
                    f"Registro: `{combat_id}`\nEsperando respuesta de {objetivo.mention}.",
                )
            )
            return

        if combat["turno_actual"] != user_id:
            await interaction.followup.send(
                embed=error_embed("No es tu turno", "Espera a que tu oponente responda."),
                ephemeral=True,
            )
            return

        if combat["fase"] != "ataque":
            await interaction.followup.send(
                embed=error_embed(
                    "Fase incorrecta",
                    "Tu oponente ya atacó. Debes responder con `/ataque`, `/defensa` o `/esquiva`.",
                ),
                ephemeral=True,
            )
            return

        oponente_id = (
            combat["defensor_id"] if user_id == combat["atacante_id"] else combat["atacante_id"]
        )

        try:
            combat = combat_service.register_attack(combat_id, user_id, accion)
        except Exception as e:
            logger.error("Error al registrar ataque: %s", e)
            await interaction.followup.send(
                embed=error_embed("Error inesperado", "No se pudo registrar el ataque."),
                ephemeral=True,
            )
            return

        try:
            log_channel = self.bot.get_channel(COMBAT_LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(
                    embed=_build_ataque_embed(combat_id, user_id, oponente_id, accion)
                )
        except Exception as e:
            logger.error("Error al enviar log: %s", e)

        await interaction.followup.send(
            embed=info_embed("Ataque registrado", f"Esperando respuesta de <@{oponente_id}>.")
        )


async def setup(bot):
    await bot.add_cog(Ataque(bot))
