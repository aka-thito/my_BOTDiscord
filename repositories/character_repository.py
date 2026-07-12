from pathlib import Path

from repositories.base import JsonRepository

CHARACTER_PATH = Path("data/characters.json")


# Clases de clanes y razas
class CharacterRepository:
    # Funciones para manejar los personajes de los usuarios
    def __init__(self):
        self._repo = JsonRepository(CHARACTER_PATH)
        self._cache: dict[str, dict] = {}

    # Funcion para cargar todos los personajes desde el archivo JSON
    def load_all(self) -> dict[str, dict]:
        if self._cache:
            return self._cache
        self._cache = self._repo.load()
        return self._cache

    # Funcion para guardar todos los personajes en el archivo JSON
    def save_all(self) -> None:
        self._repo.save(self._cache)

    # Funciones para manejar personajes individuales
    def get(self, user_id: str) -> dict | None:
        return self.load_all().get(str(user_id))

    # Funcion para verificar si un personaje existe para un usuario dado
    def exists(self, user_id: str) -> bool:
        return str(user_id) in self.load_all()

    # Funcion para verificar si un personaje está vivo para un usuario dado
    def has_alive(self, user_id: str) -> bool:
        char = self.get(user_id)
        if char is None:
            return False
        return char.get("vivo", False)

    # Funciones para crear, eliminar y actualizar personajes
    def create(self, user_id: str, character: dict) -> None:
        chars = self.load_all()
        chars[str(user_id)] = character
        self.save_all()

    def delete(self, user_id: str) -> None:
        chars = self.load_all()
        chars.pop(str(user_id), None)
        self.save_all()

    def update(self, user_id: str, data: dict) -> None:
        chars = self.load_all()
        chars[str(user_id)] = data
        self.save_all()

    # Función para recargar los personajes desde el archivo JSON
    def reload(self) -> dict[str, dict]:
        self._cache = {}
        return self.load_all()
