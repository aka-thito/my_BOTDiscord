from dataclasses import dataclass, field


@dataclass
class Item:
    id: str
    nombre: str
    descripcion: str = ""
    tipo: str = "consumible"
    cantidad: int = 1
    stats: dict = field(default_factory=dict)


@dataclass
class Inventory:
    items: list = field(default_factory=list)
    capacidad_max: int = 20
