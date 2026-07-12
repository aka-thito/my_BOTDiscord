from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class Stats:
    fuerza: int = 10
    velocidad: int = 10
    resistencia: int = 10
    inteligencia: int = 10
    chakra: int = 100


@dataclass
class CombatData:
    en_combate: bool = False
    oponente: int | None = None
    turno: int | None = None
    ultimo_movimiento: str | None = None


@dataclass
class Character:
    id: str
    nombre: str
    edad: int
    altura: float
    peso: float
    vivo: bool = True
    aldea: str = ""
    rango: str = ""
    especializacion: str = ""
    clan: str = ""
    raza: str = ""
    elemento_principal: str = ""
    elemento_secundario: str = ""
    fecha_creacion: str = field(default_factory=lambda: datetime.now().isoformat())
    estado_aprobacion: str = "pendiente"
    jutsus: list = field(default_factory=list)
    habilidades: list = field(default_factory=list)
    pasivas: list = field(default_factory=list)
    inventario: list = field(default_factory=list)
    historial_cambios: list = field(default_factory=list)
    estadisticas: dict = field(default_factory=lambda: Stats().__dict__)
    combate: dict = field(default_factory=lambda: CombatData().__dict__)
