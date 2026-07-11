from dataclasses import asdict

from .cache import CharacterCache
from .constants import CHARACTER_PATH

# JsonManager para carga/guardado JSON. Se encuentra en data/utils
from data.utils.json_manager import JsonManager


class CharacterManager:

    @classmethod
    def load(cls):
        """
        Carga todos los personajes.
        Solo lee el JSON una vez.
        """

        cache = CharacterCache.get()

        if cache:
            return cache

        data = JsonManager.load(CHARACTER_PATH)

        CharacterCache.set(data)

        return data

    @classmethod
    def save(cls):

        JsonManager.save(
            CHARACTER_PATH,
            CharacterCache.get()
        )

    @classmethod
    def get_character(cls, user_id):

        personajes = cls.load()

        return personajes.get(str(user_id))

    @classmethod
    def exists(cls, user_id):

        return str(user_id) in cls.load()

    @classmethod
    def has_alive_character(cls, user_id):

        personaje = cls.get_character(user_id)

        if personaje is None:
            return False

        return personaje.get("vivo", False)

    @classmethod
    def create_character(cls, user_id, character):

        personajes = cls.load()

        personajes[str(user_id)] = character

        cls.save()

    @classmethod
    def delete_character(cls, user_id):

        personajes = cls.load()

        personajes.pop(str(user_id), None)

        cls.save()

    @classmethod
    def update_character(cls, user_id, data):

        personajes = cls.load()

        personajes[str(user_id)] = data

        cls.save()

    @classmethod
    def reload(cls):
        """
        Fuerza una recarga desde el JSON.
        """

        CharacterCache.clear()

        return cls.load()