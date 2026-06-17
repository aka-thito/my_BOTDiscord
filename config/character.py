# Este módulo se encarga de manejar los personajes del Rol, incluyendo su carga y almacenamiento en un archivo JSON.

import json
import os

RUTA = "data/personajes.json"

def cargar_personajes():
    if not os.path.exists(RUTA):
        with open(RUTA, "w", encoding="utf-8") as f:
            json.dump({}, f)

    with open(RUTA, "r", encoding="utf-8") as f:
        return json.load(f)


def guardar_personajes(datos):
    with open(RUTA, "w", encoding="utf-8") as f:
        json.dump(datos, f, indent=4, ensure_ascii=False)