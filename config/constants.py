from pathlib import Path

CHARACTER_PATH = Path("data/characters.json")

CLANES = [
    "Uchiha",
    "Senju",
    "Hyuga",
    "Akimichi",
    "Yamanaka",
    "Nara",
    "Aburame",
    "Inuzuka",
    "Uzumaki",
]

RAZAS = ["Humano", "Fabricado", "Humano Sintético", "Ser Celestial"]
RAREZA_RAZA = [90, 5, 4, 1]

ELEMENTOS = ["Fuego", "Agua", "Tierra", "Aire", "Rayo"]

ALDEAS = [
    "Aldea de la Hoja",
    "Aldea de la Arena",
    "Aldea del Sonido",
    "Aldea de la Niebla",
    "Aldea del Rayo",
]

RANGO_INICIAL = "Genin"
RANGOS = ["Estudiante", "Genin", "Chunin", "Jonin", "Anbu", "Kage"]

ESPECIALIZACION_INICIAL = "Taijutsu"
ESPECIALIZACIONES = [
    "Taijutsu",
    "Ninjutsu",
    "Genjutsu",
    "Kenjutsu",
    "Ninjutsu Médico",
    "Fuinjutsu",
]

ESTADISTICAS_BASE = {
    "fuerza": 10,
    "velocidad": 10,
    "resistencia": 10,
    "inteligencia": 10,
    "chakra": 100,
}
