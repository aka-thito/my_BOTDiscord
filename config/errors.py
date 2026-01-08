from enum import Enum

# Descripcion: Tipos de errores estandarizados
class ErrorType(Enum):
    USAGE = "usage"
    PERMISSIONS = "permissions"
    BOT_PERMISSIONS = "bot_permissions"
    INVALID_MEMBER = "invalid_member"
    SELF_ACTION = "self_action"
    INVALID_TARGET = "invalid_target"
    HIERARCHY = "hierarchy"
    UNKNOWN = "unknown"
