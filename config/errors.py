from enum import Enum, auto

# Descripcion: Tipos de errores estandarizados
class ErrorType(Enum):
    
    USAGE = auto()
    PERMISSIONS = auto()
    BOT_PERMISSIONS = auto()
    INVALID_MEMBER = auto()
    SELF_ACTION = auto()
    HIERARCHY = auto()
    UNKNOWN = auto()
