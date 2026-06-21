import json
import os
import random
from datetime import datetime

COMBATS_FILE = "data/combats.json"
CHARACTERS_FILE = "data/characters.json"


def load_combats() -> dict:
    os.makedirs("data", exist_ok=True)
    if not os.path.exists(COMBATS_FILE):
        with open(COMBATS_FILE, "w", encoding="utf-8") as f:
            json.dump({}, f)
        return {}
    with open(COMBATS_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else {}


def save_combats(data: dict):
    with open(COMBATS_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)


def load_characters() -> dict:
    if not os.path.exists(CHARACTERS_FILE):
        return {}
    with open(CHARACTERS_FILE, "r", encoding="utf-8") as f:
        content = f.read().strip()
        return json.loads(content) if content else {}


def get_character(user_id: str) -> dict | None:
    return load_characters().get(user_id)


def get_active_combat(user_id: str) -> tuple[str | None, dict | None]:
    """Retorna (combat_id, combat) si el usuario está en un combate activo."""
    combats = load_combats()
    for combat_id, combat in combats.items():
        if combat["estado"] == "activo":
            if user_id in (combat["atacante_id"], combat["defensor_id"]):
                return combat_id, combat
    return None, None


def _generate_combat_id() -> str:
    combats = load_combats()
    today = datetime.now().strftime("%Y%m%d")
    count = sum(1 for cid in combats if cid.startswith(f"CB-{today}"))
    return f"CB-{today}-{count + 1:04d}"


def create_combat(guild_id: str, atacante_id: str, defensor_id: str, accion_texto: str) -> tuple[str, dict]:
    """Crea un nuevo combate. Retorna (combat_id, combat)."""
    combats = load_combats()
    combat_id = _generate_combat_id()
    entrada = {
        "tipo": "ataque",
        "texto": accion_texto,
        "usuario_id": atacante_id,
        "timestamp": datetime.now().isoformat()
    }
    combats[combat_id] = {
        "guild_id": guild_id,
        "atacante_id": atacante_id,
        "defensor_id": defensor_id,
        "turno_actual": defensor_id,
        "fase": "respuesta",
        "ultima_accion": entrada,
        "historial": [entrada],
        "estado": "activo",
        "fecha_inicio": datetime.now().isoformat()
    }
    save_combats(combats)
    return combat_id, combats[combat_id]


def register_attack(combat_id: str, atacante_id: str, accion_texto: str) -> dict:
    """Registra un /ataque en fase 'ataque'. Pasa a fase 'respuesta'."""
    combats = load_combats()
    combat = combats[combat_id]
    oponente_id = _get_opponent(combat, atacante_id)

    entrada = {
        "tipo": "ataque",
        "texto": accion_texto,
        "usuario_id": atacante_id,
        "timestamp": datetime.now().isoformat()
    }
    combat["ultima_accion"] = entrada
    combat["historial"].append(entrada)
    combat["fase"] = "respuesta"
    combat["turno_actual"] = oponente_id
    save_combats(combats)
    return combat


def _get_opponent(combat: dict, user_id: str) -> str:
    return combat["defensor_id"] if user_id == combat["atacante_id"] else combat["atacante_id"]


def resolve_response(combat_id: str, respondedor_id: str, respuesta_tipo: str, respuesta_texto: str) -> tuple[str, dict]:
    """
    Resuelve la respuesta del defensor.
    respuesta_tipo: "ataque" | "defensa" | "esquiva"
    Retorna (texto_resultado, combat_actualizado)
    """
    combats = load_combats()
    combat = combats[combat_id]
    ultima = combat["ultima_accion"]
    iniciador_id = ultima["usuario_id"]

    chars = load_characters()
    stats_i = chars[iniciador_id]["estadisticas"]
    stats_r = chars[respondedor_id]["estadisticas"]

    roll_i = random.randint(0, 20)
    roll_r = random.randint(0, 20)

    if respuesta_tipo == "ataque":
        score_i = stats_i["fuerza"] + roll_i
        score_r = stats_r["fuerza"] + roll_r
        if score_i > score_r:
            resultado = (
                f"⚔️ **Contraataque** — El ataque de <@{iniciador_id}> fue más poderoso "
                f"(`{score_i}` vs `{score_r}`). <@{respondedor_id}> recibe el golpe."
            )
        elif score_r > score_i:
            resultado = (
                f"⚔️ **Contraataque** — <@{respondedor_id}> contraatacó con éxito "
                f"(`{score_r}` vs `{score_i}`). <@{iniciador_id}> recibe el golpe."
            )
        else:
            resultado = (
                f"⚔️ **Contraataque** — ¡Impacto mutuo! "
                f"(`{score_i}` vs `{score_r}`). Ambos reciben el golpe."
            )

    elif respuesta_tipo == "defensa":
        score_i = stats_i["fuerza"] + roll_i
        score_r = stats_r["resistencia"] + roll_r
        if score_i > score_r:
            resultado = (
                f"🛡️ **Ataque vs Defensa** — El ataque atravesó la defensa "
                f"(`{score_i}` vs `{score_r}`). <@{respondedor_id}> recibe el golpe."
            )
        else:
            resultado = (
                f"🛡️ **Ataque vs Defensa** — La defensa resistió el impacto "
                f"(`{score_r}` vs `{score_i}`). <@{iniciador_id}> es bloqueado."
            )

    else:  # esquiva
        score_i = stats_i["fuerza"] + roll_i
        score_r = stats_r["velocidad"] + roll_r
        if score_i > score_r:
            resultado = (
                f"💨 **Ataque vs Esquiva** — El ataque fue demasiado rápido "
                f"(`{score_i}` vs `{score_r}`). <@{respondedor_id}> no pudo esquivar."
            )
        else:
            resultado = (
                f"💨 **Ataque vs Esquiva** — ¡Esquiva exitosa! "
                f"(`{score_r}` vs `{score_i}`). <@{respondedor_id}> se mueve a tiempo."
            )

    # Tras la resolución: el respondedor pasa a atacar en el siguiente turno
    entrada = {
        "tipo": respuesta_tipo,
        "texto": respuesta_texto,
        "usuario_id": respondedor_id,
        "resultado": resultado,
        "timestamp": datetime.now().isoformat()
    }
    combat["ultima_accion"] = entrada
    combat["historial"].append(entrada)
    combat["fase"] = "ataque"
    combat["turno_actual"] = respondedor_id
    save_combats(combats)

    return resultado, combat
