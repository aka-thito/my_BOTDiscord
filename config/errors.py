from enum import Enum

# Descripcion: Tipos de errores estandarizados
class ErrorType(Enum):
    
    USAGE = 1
    PERMISSIONS = 2
    BOT_PERMISSIONS = 3
    INVALID_MEMBER = 4
    SELF_ACTION = 5
    UNKNOWN = 99
