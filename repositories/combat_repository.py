from datetime import datetime
from pathlib import Path

from repositories.base import JsonRepository

COMBAT_PATH = Path("data/combats.json")


class CombatRepository:
    def __init__(self):
        self._repo = JsonRepository(COMBAT_PATH)

    def load_all(self) -> dict[str, dict]:
        return self._repo.load()

    def save_all(self, data: dict[str, dict]) -> None:
        self._repo.save(data)

    def get(self, combat_id: str) -> dict | None:
        return self.load_all().get(combat_id)

    def get_active_for_user(self, user_id: str) -> tuple[str | None, dict | None]:
        combats = self.load_all()
        for cid, combat in combats.items():
            if combat.get("estado") == "activo":
                if user_id in (combat.get("atacante_id"), combat.get("defensor_id")):
                    return cid, combat
        return None, None

    def create(self, combat_id: str, data: dict) -> None:
        combats = self.load_all()
        combats[combat_id] = data
        self.save_all(combats)

    def update(self, combat_id: str, data: dict) -> None:
        combats = self.load_all()
        combats[combat_id] = data
        self.save_all(combats)

    def generate_id(self) -> str:
        combats = self.load_all()
        today = datetime.now().strftime("%Y%m%d")
        count = sum(1 for cid in combats if cid.startswith(f"CB-{today}"))
        return f"CB-{today}-{count + 1:04d}"
