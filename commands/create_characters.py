import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random
from datetime import datetime

from config.error_sender import send

# Archivo donde se guardarán los personajes
ARCHIVO_PERSONAJES = "data/characters.json"
ARCHIVO_CLANES = "data/clans.json"

# Lista de valores aleatorios disponibles
ELEMENTOS = ["Fuego", "Agua", "Tierra", "Aire", "Rayo"]
RAZAS = ["Humano", "Fabricado", "Humano Sintético", "Ser Celestial"]
ALDEAS = ["Aldea de la Hoja", "Aldea de la Arena", "Aldea del Sonido", "Aldea de la Niebla", "Aldea del Rayo"]
RANGOS = ["Genin", "Chunin", "Jonin", "Anbu", "Kage"]
ESPECIALIZACIONES = ["Taijutsu", "Ninjutsu", "Genjutsu", "Kenjutsu", "Medico Ninja", "Sellador"]

# funciones para cargar y guardar personajes en un archivo JSON
def load_characters():
    if not os.path.exists(ARCHIVO_PERSONAJES):
        with open(ARCHIVO_PERSONAJES, "w", encoding="utf-8") as archivo:
            json.dump({}, archivo, indent=4)
        return {}

    try:
        with open(ARCHIVO_PERSONAJES, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return {}
            return json.loads(contenido)
    except json.JSONDecodeError:
        print(f"[ERROR] El archivo {ARCHIVO_PERSONAJES} no está bien formado.")
        return {}


def save_characters(datos):
    with open(ARCHIVO_PERSONAJES, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


def load_clans():
    """Carga los clanes disponibles desde clans.json"""
    if not os.path.exists(ARCHIVO_CLANES):
        return {}
    
    try:
        with open(ARCHIVO_CLANES, "r", encoding="utf-8") as archivo:
            contenido = archivo.read().strip()
            if not contenido:
                return {}
            return json.loads(contenido)
    except json.JSONDecodeError:
        print(f"[ERROR] El archivo {ARCHIVO_CLANES} no está bien formado.")
        return {}


def get_available_clans():
    """Retorna una lista de clanes disponibles"""
    clanes = load_clans()
    return list(clanes.keys())


# Función para asignar valores aleatorios con validación de clanes
def assign_random_values(clan_nombre):
    """
    Asigna valores aleatorios al personaje basándose en el clan elegido.
    - Si cantidad_elementos = 1: asigna solo el elemento natural del clan
    - Si cantidad_elementos > 1: asigna el elemento del clan + otros elementos aleatorios
    """
    clanes = load_clans()
    clan_data = clanes.get(clan_nombre, {})
    elemento_natural = clan_data.get("elemento_natural", random.choice(ELEMENTOS))
    
    # Selección de raza con pesos/probabilidades
    raza = random.choices(RAZAS, weights=[90, 5, 4, 1], k=1)[0]
    
    # Cantidad de elementos con distribución: 3 es más común
    cantidad_elementos = random.choices([1, 2, 3, 4, 5], weights=[15, 20, 30, 20, 15], k=1)[0]
    
    # Lógica de asignación de elementos
    if cantidad_elementos == 1:
        # Solo el elemento del clan
        elementos = [elemento_natural]
    else:
        # Elemento del clan + otros aleatorios
        elementos_adicionales = [e for e in ELEMENTOS if e != elemento_natural]
        elementos_random = random.sample(elementos_adicionales, min(cantidad_elementos - 1, len(elementos_adicionales)))
        elementos = [elemento_natural] + elementos_random

    return {
        "clan": clan_nombre,
        "elementos": elementos,
        "cantidad_elementos": cantidad_elementos,
        "raza": raza
    }


# Función para crear la estructura base del personaje
def create_character_structure(nombre, edad, altura, peso, aldea, genero, random_values):
    """
    Crea la estructura completa del personaje.
    Esta estructura es expandible para futuras funcionalidades.
    """
    return {
        # Información básica (CU-01: Creación de ficha)
        "nombre": nombre,
        "edad": edad,
        "altura": altura,
        "peso": peso,
        "genero": genero,
        "vivo": True,
        "aldea": aldea,
        "rango": "Civil",
        "especializacion": None,
        "fecha_creacion": datetime.now().isoformat(),
        "estado_aprobacion": "pendiente",  # CU-12: Validar/aprobar ficha inicial
        
        # Valores asignados
        "clan": random_values["clan"],
        "elementos": random_values["elementos"],
        "cantidad_elementos": random_values["cantidad_elementos"],
        "raza": random_values["raza"],
        
        # Información del personaje
        "jutsus": [],  # CU-06: Revisar Jutsus
        "inventario": [],  # CU-04: Revisar inventario
        
        # Estadísticas (CU-05: Revisar estadísticas)
        "estadisticas": {
            "fuerza": 10,
            "velocidad": 10,
            "resistencia": 10,
            "inteligencia": 10,
            "chakra": 100
        },
        
        # Historial de cambios (CU-11: Historial de cambios de la ficha)
        "historial_cambios": []
    }


# Este comando permite a los usuarios crear un personaje para el rol, solicitando información básica como nombre, edad, altura y peso.
# La información se guarda en un archivo JSON para su posterior uso en el juego de rol.
class CreateCharacter(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="create-pj",
        description="Crea tu personaje mediante un formulario privado en el servidor"
    )
    async def create_character(self, interaction: discord.Interaction):
        personajes = load_characters()
        user_id = str(interaction.user.id)

        if user_id in personajes and personajes[user_id]["vivo"]:
            await interaction.response.send_message(
                f"❌ {interaction.user.mention}, ya posees un personaje vivo.\n"
                f"No puedes crear otro hasta que el actual muera.",
                ephemeral=True
            )
            return

        await interaction.response.send_modal(CreateCharacterModal(self.bot))

    @create_character.error
    async def create_character_error(self, interaction: discord.Interaction, error):
        if interaction.response.is_done():
            send = interaction.followup.send
        else:
            send = interaction.response.send_message

        if isinstance(error, app_commands.MissingPermissions):
            await send("❌ No tienes permisos para ejecutar este comando.", ephemeral=True)
        elif isinstance(error, discord.Forbidden):
            await send("❌ No tengo permisos para completar esta acción.", ephemeral=True)
        elif isinstance(error, discord.HTTPException):
            await send("❌ Error en la comunicación con Discord. Inténtalo más tarde.", ephemeral=True)
        else:
            print(error)

            await send(
                f"❌ Error inesperado:\n{error}",
                ephemeral=True
            )


class CreateCharacterModal(discord.ui.Modal):
    def __init__(self, bot):
        super().__init__(title="Crear personaje")
        self.bot = bot

        self.nombre = discord.ui.TextInput(
            label="Nombre del personaje",
            placeholder="Escribe el nombre de tu personaje",
            required=True,
            max_length=50
        )
        self.add_item(self.nombre)

        self.edad = discord.ui.TextInput(
            label="Edad",
            placeholder="Ejemplo: 18",
            required=True,
            max_length=3
        )
        self.add_item(self.edad)

        self.altura = discord.ui.TextInput(
            label="Altura (m)",
            placeholder="Ejemplo: 1.75",
            required=True,
            max_length=5
        )
        self.add_item(self.altura)

        self.peso = discord.ui.TextInput(
            label="Peso (kg)",
            placeholder="Ejemplo: 70",
            required=True,
            max_length=5
        )
        self.add_item(self.peso)

        self.aldea = discord.ui.TextInput(
            label="Aldea",
            placeholder="Ejemplo: Aldea de la Hoja",
            required=True,
            max_length=30
        )
        self.add_item(self.aldea)

    async def on_submit(self, interaction: discord.Interaction):
        personajes = load_characters()
        user_id = str(interaction.user.id)

        if user_id in personajes and personajes[user_id]["vivo"]:
            await interaction.response.send_message(
                f"❌ {interaction.user.mention}, ya posees un personaje vivo.",
                ephemeral=True
            )
            return

        try:
            edad = int(self.edad.value)
        except ValueError:
            await interaction.response.send_message(
                "❌ La edad debe ser un número válido.",
                ephemeral=True
            )
            return

        try:
            altura = float(self.altura.value)
        except ValueError:
            await interaction.response.send_message(
                "❌ La altura debe ser un número válido (ej: 1.75).",
                ephemeral=True
            )
            return

        try:
            peso = float(self.peso.value)
        except ValueError:
            await interaction.response.send_message(
                "❌ El peso debe ser un número válido.",
                ephemeral=True
            )
            return

        await interaction.response.defer()
        await interaction.followup.send(view=GenderSelectView(self.bot, self.nombre.value, edad, altura, peso, self.aldea.value), ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        print(f"[CREATE-PJ] Error en modal: {error}")
        await interaction.response.send_message(
            "❌ Ocurrió un error inesperado al crear tu personaje.",
            ephemeral=True
        )


class GenderSelect(discord.ui.Select):
    def __init__(self, bot, nombre, edad, altura, peso, aldea):
        self.bot = bot
        self.nombre = nombre
        self.edad = edad
        self.altura = altura
        self.peso = peso
        self.aldea = aldea
        
        options = [
            discord.SelectOption(label="Mujer", value="Mujer", emoji="👩"),
            discord.SelectOption(label="Hombre", value="Hombre", emoji="👨"),
        ]
        super().__init__(placeholder="Selecciona tu género...", options=options)

    async def callback(self, interaction: discord.Interaction):
        genero = self.values[0]
        
        clanes = load_clans()
        
        if not clanes:
            await interaction.response.defer()
            await interaction.followup.send(
                "❌ Error: No se encontraron clanes disponibles. Contacta al administrador.",
                ephemeral=True
            )
            return
        
        clanes_list = list(clanes.keys())
        
        await interaction.response.defer()
        embed = discord.Embed(
            title="Selecciona tu clan",
            description="Elige el clan al que pertenecerá tu personaje. Cada clan tiene su propio elemento natural.",
            color=discord.Color.blue()
        )
        
        clan_options = [
            discord.SelectOption(
                label=clan,
                value=clan,
                description=clanes[clan].get("descripcion", "")[:50] + "..."
            )
            for clan in clanes_list
        ]
        
        await interaction.followup.send(
            embed=embed,
            view=ClanSelectView(self.bot, self.nombre, self.edad, self.altura, self.peso, self.aldea, genero, clan_options),
            ephemeral=True
        )


class GenderSelectView(discord.ui.View):
    def __init__(self, bot, nombre, edad, altura, peso, aldea):
        super().__init__()
        self.add_item(GenderSelect(bot, nombre, edad, altura, peso, aldea))


class ClanSelect(discord.ui.Select):
    def __init__(self, bot, nombre, edad, altura, peso, aldea, genero, clan_options):
        self.bot = bot
        self.nombre = nombre
        self.edad = edad
        self.altura = altura
        self.peso = peso
        self.aldea = aldea
        self.genero = genero
        
        super().__init__(placeholder="Selecciona tu clan...", options=clan_options)

    async def callback(self, interaction: discord.Interaction):
        clan_nombre = self.values[0]
        
        random_values = assign_random_values(clan_nombre)
        personaje_data = create_character_structure(
            self.nombre,
            self.edad,
            self.altura,
            self.peso,
            self.aldea,
            self.genero,
            random_values
        )

        personajes = load_characters()
        user_id = str(interaction.user.id)
        personajes[user_id] = personaje_data
        save_characters(personajes)

        elementos_str = ", ".join(personaje_data['elementos'])
        clanes = load_clans()
        clan_data = clanes.get(clan_nombre, {})

        embed = discord.Embed(
            title="Personaje creado - En espera de aprobación",
            description="✅ Tu personaje fue creado correctamente.\n⏳ Tu ficha está pendiente de aprobación por un Administrador.",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📝 Información Básica",
            value=f"**Nombre:** {self.nombre}\n**Género:** {self.genero}\n**Edad:** {self.edad}\n**Altura:** {self.altura}m\n**Peso:** {self.peso}kg",
            inline=False
        )
        embed.add_field(
            name="🏘️ Datos del Personaje",
            value=f"**Aldea:** {self.aldea}\n**Rango:** Civil\n**Especialización:** Por definir",
            inline=False
        )
        embed.add_field(
            name="⚡ Elementos y Atributos",
            value=f"**Clan:** {clan_nombre}\n**Elemento Natural del Clan:** {clan_data.get('elemento_natural', 'Desconocido')}\n**Cantidad de Elementos:** {personaje_data['cantidad_elementos']}\n**Elementos:** {elementos_str}\n**Raza:** {personaje_data['raza']}",
            inline=False
        )
        embed.add_field(
            name="💪 Estadísticas Iniciales",
            value=f"**Fuerza:** {personaje_data['estadisticas']['fuerza']}\n**Velocidad:** {personaje_data['estadisticas']['velocidad']}\n**Resistencia:** {personaje_data['estadisticas']['resistencia']}\n**Inteligencia:** {personaje_data['estadisticas']['inteligencia']}\n**Chakra:** {personaje_data['estadisticas']['chakra']}",
            inline=False
        )
        embed.set_footer(text="Estado: Pendiente de aprobación | CU-12: Validar/aprobar ficha inicial")

        await interaction.response.edit_message(view=None, embed=embed)


class ClanSelectView(discord.ui.View):
    def __init__(self, bot, nombre, edad, altura, peso, aldea, genero, clan_options):
        super().__init__()
        self.add_item(ClanSelect(bot, nombre, edad, altura, peso, aldea, genero, clan_options))


async def setup(bot):

    await bot.add_cog(CreateCharacter(bot))

