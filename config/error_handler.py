import traceback

import discord

from config.embeds import error_embed
from config.error_sender import send
from config.errors import ErrorType
from config.logging_config import setup_logging

logger = setup_logging()


async def log_exception(
    error: Exception,
    interaction: discord.Interaction | None = None,
    context_text: str | None = None,
):
    tb = traceback.format_exc()
    info_parts = []
    if context_text:
        info_parts.append(f"context={context_text}")
    if interaction is not None:
        try:
            user = f"user={interaction.user} id={getattr(interaction.user, 'id', None)}"
        except Exception:
            user = "user=<unknown>"
        guild_id = (
            getattr(interaction.guild, "id", None) if getattr(interaction, "guild", None) else None
        )
        cmd = getattr(interaction, "command", None)
        cmd_name = cmd.name if cmd else None
        info_parts.append(user)
        info_parts.append(f"guild_id={guild_id}")
        info_parts.append(f"command={cmd_name}")
    info = " ".join(info_parts)
    logger.error("Exception: %s\n%s\n%s", error, info, tb)


async def handle_error(ctx, error_type: ErrorType):
    is_interaction = isinstance(ctx, discord.Interaction)

    if error_type == ErrorType.USAGE:
        if is_interaction:
            cmd_name = ctx.command.name if getattr(ctx, "command", None) else ""
            embed = error_embed("Uso incorrecto", f"Verifica los argumentos: /{cmd_name}")
        else:
            embed = error_embed(
                "Uso incorrecto",
                f"Verifica los argumentos: {ctx.prefix}{ctx.command} {ctx.command.signature}",
            )

    elif error_type == ErrorType.PERMISSIONS:
        embed = error_embed(
            "Permisos insuficientes",
            "No tienes los permisos necesarios para ejecutar este comando.",
        )

    elif error_type == ErrorType.BOT_PERMISSIONS:
        embed = error_embed(
            "Permisos insuficientes del bot",
            "El bot no tiene los permisos necesarios para ejecutar este comando.",
        )

    elif error_type == ErrorType.INVALID_MEMBER:
        embed = error_embed(
            "Miembro inválido",
            "El miembro especificado no es válido o no se encuentra en el servidor.",
        )

    elif error_type == ErrorType.SELF_ACTION:
        embed = error_embed("Acción inválida", "No puedes realizar esta acción sobre ti mismo.")

    elif error_type == ErrorType.HIERARCHY:
        embed = error_embed(
            "Error de jerarquía",
            "No puedes realizar esta acción sobre un miembro con un rol superior o igual al tuyo.",
        )

    else:
        embed = error_embed("Error desconocido", "Ocurrió un error inesperado.")

    await send(ctx, embed)
