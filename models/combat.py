from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CombatAction:
    tipo: str
    texto: str
    usuario_id: str
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())
    resultado: str | None = None


@dataclass
class Combat:
    id: str
    guild_id: str
    atacante_id: str
    defensor_id: str
    turno_actual: str
    fase: str
    ultima_accion: CombatAction
    historial: list = field(default_factory=list)
    estado: str = "activo"
    fecha_inicio: str = field(default_factory=lambda: datetime.now().isoformat())
