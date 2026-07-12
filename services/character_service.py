import random
import uuid
from dataclasses import asdict

from config.constants import (
    ALDEAS,
    CLANES,
    ELEMENTOS,
    ESPECIALIZACION_INICIAL,
    RANGO_INICIAL,
    RAREZA_RAZA,
    RAZAS,
)
from models.character import Character
from repositories.character_repository import CharacterRepository


class CharacterService:
    def __init__(self):
        self._repo = CharacterRepository()

    def create(self, nombre: str, edad: int, altura: float, peso: float, aldea: str) -> dict:
        raza = random.choices(RAZAS, weights=RAREZA_RAZA, k=1)[0]
        elemento_principal, elemento_secundario = random.sample(ELEMENTOS, 2)
        personaje = Character(
            id=str(uuid.uuid4()),
            nombre=nombre,
            edad=edad,
            altura=altura,
            peso=peso,
            aldea=aldea,
            rango=RANGO_INICIAL,
            especializacion=ESPECIALIZACION_INICIAL,
            clan=random.choice(CLANES),
            raza=raza,
            elemento_principal=elemento_principal,
            elemento_secundario=elemento_secundario,
        )
        return asdict(personaje)

    def save(self, user_id: str, character: dict) -> None:
        self._repo.create(user_id, character)

    def get(self, user_id: str) -> dict | None:
        return self._repo.get(user_id)

    def has_alive(self, user_id: str) -> bool:
        return self._repo.has_alive(user_id)

    def delete(self, user_id: str) -> None:
        self._repo.delete(user_id)

    def all(self) -> dict[str, dict]:
        return self._repo.load_all()

    def update(self, user_id: str, data: dict) -> None:
        self._repo.update(user_id, data)

    def get_pending(self) -> dict[str, dict]:
        return {
            uid: c for uid, c in self.all().items() if c.get("estado_aprobacion") == "pendiente"
        }

    def get_approved(self) -> dict[str, dict]:
        return {uid: c for uid, c in self.all().items() if c.get("estado_aprobacion") == "aprobado"}

    def approve(self, user_id: str) -> None:
        char = self.get(user_id)
        if char:
            char["estado_aprobacion"] = "aprobado"
            self._repo.update(user_id, char)

    def reject(self, user_id: str) -> None:
        char = self.get(user_id)
        if char:
            char["estado_aprobacion"] = "rechazado"
            self._repo.update(user_id, char)

    @staticmethod
    def validate_name(nombre: str) -> str:
        nombre = nombre.strip()
        if len(nombre) < 1:
            raise ValueError("El nombre debe tener mínimo 1 caracter.")
        if len(nombre) > 20:
            raise ValueError("El nombre no puede superar los 20 Caracteres.")
        return nombre

    @staticmethod
    def validate_age(edad: int) -> int:
        if edad < 10 or edad > 90:
            raise ValueError("La edad debe estar entre 10 y 90 años.")
        return edad

    @staticmethod
    def validate_height(altura: float) -> float:
        if altura < 1.00 or altura > 2.50:
            raise ValueError("La altura debe estar entre 1.00 y 2.50 metros.")
        return altura

    @staticmethod
    def validate_weight(peso: float) -> float:
        if peso < 20 or peso > 250:
            raise ValueError("El peso ingresado no es válido.")
        return peso

    @staticmethod
    def validate_village(aldea: str) -> str:
        if aldea not in ALDEAS:
            raise ValueError("La aldea seleccionada no existe.")
        return aldea
