import random
from datetime import datetime

from repositories.character_repository import CharacterRepository
from repositories.combat_repository import CombatRepository


class CombatService:
    def __init__(self):
        self._combat_repo = CombatRepository()
        self._char_repo = CharacterRepository()

    def get_active_combat(self, user_id: str) -> tuple[str | None, dict | None]:
        return self._combat_repo.get_active_for_user(user_id)

    def get_character(self, user_id: str) -> dict | None:
        return self._char_repo.get(user_id)

    def create_combat(
        self, guild_id: str, atacante_id: str, defensor_id: str, accion_texto: str
    ) -> tuple[str, dict]:
        combat_id = self._combat_repo.generate_id()
        entrada = {
            "tipo": "ataque",
            "texto": accion_texto,
            "usuario_id": atacante_id,
            "timestamp": datetime.now().isoformat(),
        }
        combat = {
            "guild_id": guild_id,
            "atacante_id": atacante_id,
            "defensor_id": defensor_id,
            "turno_actual": defensor_id,
            "fase": "respuesta",
            "ultima_accion": entrada,
            "historial": [entrada],
            "estado": "activo",
            "fecha_inicio": datetime.now().isoformat(),
        }
        self._combat_repo.create(combat_id, combat)
        return combat_id, combat

    def register_attack(self, combat_id: str, atacante_id: str, accion_texto: str) -> dict:
        combats = self._combat_repo.load_all()
        combat = combats[combat_id]
        oponente_id = self._get_opponent(combat, atacante_id)
        entrada = {
            "tipo": "ataque",
            "texto": accion_texto,
            "usuario_id": atacante_id,
            "timestamp": datetime.now().isoformat(),
        }
        combat["ultima_accion"] = entrada
        combat["historial"].append(entrada)
        combat["fase"] = "respuesta"
        combat["turno_actual"] = oponente_id
        self._combat_repo.update(combat_id, combat)
        return combat

    def resolve_response(
        self, combat_id: str, respondedor_id: str, respuesta_tipo: str, respuesta_texto: str
    ) -> tuple[str, dict]:
        combats = self._combat_repo.load_all()
        combat = combats[combat_id]
        ultima = combat["ultima_accion"]
        iniciador_id = ultima["usuario_id"]
        chars = self._char_repo.load_all()
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
        else:
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

        entrada = {
            "tipo": respuesta_tipo,
            "texto": respuesta_texto,
            "usuario_id": respondedor_id,
            "resultado": resultado,
            "timestamp": datetime.now().isoformat(),
        }
        combat["ultima_accion"] = entrada
        combat["historial"].append(entrada)
        combat["fase"] = "ataque"
        combat["turno_actual"] = respondedor_id
        self._combat_repo.update(combat_id, combat)
        return resultado, combat

    @staticmethod
    def _get_opponent(combat: dict, user_id: str) -> str:
        return combat["defensor_id"] if user_id == combat["atacante_id"] else combat["atacante_id"]
