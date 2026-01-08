from config.errors import ErrorType
from config.embeds import error_embed
from config.error_sender import send

# Descripcion: Maneja y envia mensajes de error estandarizados
async def handle_error(ctx, error_type: ErrorType):

    if error_type == ErrorType.USAGE:
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