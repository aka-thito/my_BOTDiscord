import json
from pathlib import Path
from typing import Any


class JsonRepository:
    def __init__(self, path: Path):
        self.path = path

    def load(self, default: dict[str, Any] | None = None) -> dict[str, Any]:
        if default is None:
            default = {}
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write(default)
            return default.copy()
        try:
            with self.path.open("r", encoding="utf-8") as f:
                return json.load(f)
        except json.JSONDecodeError:
            self._write(default)
            return default.copy()

    def save(self, data: dict[str, Any]) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._write(data)

    def _write(self, data: dict[str, Any]) -> None:
        with self.path.open("w", encoding="utf-8") as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
