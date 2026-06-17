import logging
import traceback
import discord
from config.errors import ErrorType
from config.embeds import error_embed
from config.error_sender import send

# Configura logger simple si no hay configuracion
logger = logging.getLogger("bot")
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter("[%(asctime)s] %(levelname)s: %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    logger.setLevel(logging.INFO)


async def log_exception(error: Exception, interaction: discord.Interaction = None, context_text: str = None):
    """
    Loggea la excepción con traceback y datos relevantes de la interacción.
    """
    tb = traceback.format_exc()
    info_parts = []
    if context_text:
        info_parts.append(f"context={context_text}")
    if interaction is not None:
        try:
            user = f"user={interaction.user} id={getattr(interaction.user, 'id', None)}"
        except Exception:
            user = f"user=<unknown>"
        guild_id = getattr(interaction.guild, 'id', None) if getattr(interaction, 'guild', None) else None
        cmd = getattr(interaction, 'command', None)
        cmd_name = cmd.name if cmd else None
        info_parts.append(user)
        info_parts.append(f"guild_id={guild_id}")
        info_parts.append(f"command={cmd_name}")
    info = " ".join(info_parts)

    logger.error("Exception: %s\n%s\n%s", error, info, tb)


# Descripcion: Maneja y envia mensajes de error estandarizados
async def handle_error(ctx, error_type: ErrorType):

    is_interaction = isinstance(ctx, discord.Interaction)

    if error_type == ErrorType.USAGE:
        if is_interaction:
            cmd_name = ctx.command.name if getattr(ctx, 'command', None) else ''
            embed = error_embed(
                "Uso incorrecto",
                f"Verifica los argumentos: /{cmd_name}"
            )
        else:
            embed = error_embed(
                "Uso incorrecto",
                f"Verifica los argumentos: {ctx.prefix}{ctx.command} {ctx.command.signature}"
            )

    elif error_type == ErrorType.PERMISSIONS:
        embed = error_embed(
            "Permisos insuficientes",
            "No tienes los permisos necesarios para ejecutar este comando."
        )

    elif error_type == ErrorType.BOT_PERMISSIONS:
        embed = error_embed(
            "Permisos insuficientes del bot",
            "El bot no tiene los permisos necesarios para ejecutar este comando."
        )

    elif error_type == ErrorType.INVALID_MEMBER:
        embed = error_embed(
            "Miembro inválido",
            "El miembro especificado no es válido o no se encuentra en el servidor."
        )

    elif error_type == ErrorType.SELF_ACTION:
        embed = error_embed(
            "Acción inválida",
            "No puedes realizar esta acción sobre ti mismo."
        )

    elif error_type == ErrorType.HIERARCHY:
        embed = error_embed(
            "Error de jerarquía",
            "No puedes realizar esta acción sobre un miembro con un rol superior o igual al tuyo."
        )

    else:  # ErrorType.UNKNOWN
        embed = error_embed(
            "Error desconocido",
            "Ocurrió un error inesperado."
        )

    await send(ctx, embed)
