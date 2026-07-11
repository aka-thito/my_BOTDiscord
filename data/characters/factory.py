import random
import uuid

from dataclasses import asdict

from .models import Character

from .constants import (
    CLANES,
    RAZAS,
    RAREZA_RAZA,
    ELEMENTOS,
    RANGO_INICIAL,
    ESPECIALIZACION_INICIAL
)


class CharacterFactory:

    @staticmethod
    def crear(

        nombre,
        edad,
        altura,
        peso,
        aldea

    ):

        raza = random.choices(

            RAZAS,

            weights=PESO_RAZAS,

            k=1

        )[0]

        elemento_principal, elemento_secundario = random.sample(

            ELEMENTOS,

            2

        )

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

            elemento_secundario=elemento_secundario

        )

        return asdict(personaje)