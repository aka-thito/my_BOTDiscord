from config.embeds import error_embed
from config.errors import ErrorType

# Descripcion: Envia mensajes de error estandarizados
async def send_error(ctx, error_type: ErrorType):

    if error_type == ErrorType.USAGE:
        embed = error_embed(
            "Uso incorrecto",
            "No usaste correctamente el comando.\n"
            "Verifica los argumentos."
        )

    elif error_type == ErrorType.PERMISSIONS:
        embed = error_embed(
            "Permisos insuficientes",
            "No tienes permisos para ejecutar este comando."
        )

    elif error_type == ErrorType.BOT_PERMISSIONS:
        embed = error_embed(
            "Permisos insuficientes",
            "No tengo permisos suficientes para realizar esta acción."
        )

    elif error_type == ErrorType.INVALID_MEMBER:
        embed = error_embed(
            "Miembro inválido",
            "No se pudo encontrar al miembro mencionado."
        )

    elif error_type == ErrorType.SELF_ACTION:
        embed = error_embed(
            "Acción no permitida",
            "No puedes realizar esta acción sobre ti mismo."
        )

    else:
        embed = error_embed(
            "Error desconocido",
            "Ocurrió un error inesperado."
        )

    # Enviar el mensaje de error al contexto
    await ctx.send(embed = embed)
