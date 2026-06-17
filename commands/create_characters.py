import discord
from discord.ext import commands
from discord import app_commands
import json
import os
import random

# Archivo donde se guardarán los personajes
ARCHIVO_PERSONAJES = "data/characters.json"

# Lista de valores aleatorios disponibles
CLANES = ["Uchiha", "Senju", "Hyuga", "Akimichi", "Yamanaka", "Nara", "Aburame", "Inuzuka", "Uzumaki"]
ELEMENTOS = ["Fuego", "Agua", "Tierra", "Aire", "Rayo"]
RAZAS = ["Humano", "Fabricado", "Humano Sintético", "Ser Celestial"]

# funciones para cargar y guardar personajes en un archivo JSON
def load_characters():

    # si el archivo no existe, lo crea con un diccionario vacío
    if not os.path.exists(ARCHIVO_PERSONAJES):

        # con abrir el archivo en modo escritura, crea un nuevo archivo con un diccionario vacío
        with open(ARCHIVO_PERSONAJES, "w", encoding="utf-8") as archivo:
            json.dump({}, archivo, indent=4)

    #con abrir el archivo en modo lectura, devuelve el contenido como un diccionario
    with open(ARCHIVO_PERSONAJES, "r", encoding="utf-8") as archivo:
        return json.load(archivo)


# función para guardar personajes en el archivo JSON
def save_characters(datos):

    with open(ARCHIVO_PERSONAJES, "w", encoding="utf-8") as archivo:
        json.dump(datos, archivo, indent=4, ensure_ascii=False)


# Función para asignar valores aleatorios
def assign_random_values():
    """
    Asigna valores aleatorios al personaje.
    Retorna un diccionario con clan, elemento y raza.
    Probabilidades de raza: Humano 90%, Fabricado 5%, Humano Sintético 4%, Ser Celestial 1%.
    """
    # Selección de raza con pesos/probabilidades
    raza = random.choices(RAZAS, weights=[90, 5, 4, 1], k=1)[0]

    return {
        "clan": random.choice(CLANES),
        "elemento_principal": random.choice(ELEMENTOS),
        "elemento_secundario": random.choice(ELEMENTOS),
        "raza": raza
    }


# Función para crear la estructura base del personaje
def create_character_structure(nombre, edad, altura, peso, random_values):
    """
    Crea la estructura completa del personaje.
    Esta estructura es expandible para futuras funcionalidades.
    """
    return {
        # Información básica
        "nombre": nombre,
        "edad": edad,
        "altura": altura,
        "peso": peso,
        "vivo": True,
        
        # Valores aleatorios asignados
        "clan": random_values["clan"],
        "elemento_principal": random_values["elemento_principal"],
        "elemento_secundario": random_values["elemento_secundario"],
        "raza": random_values["raza"],
        
        # Habilidades (expandible en el futuro)
        "habilidades": [],
        
        # Inventario (expandible en el futuro)
        "inventario": [],
        
        # Estadísticas base (para futuras mecánicas de combate)
        "estadisticas": {
            "fuerza": 10,
            "velocidad": 10,
            "resistencia": 10,
            "inteligencia": 10,
            "chakra": 100
        }
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
            await send("❌ Error inesperado al ejecutar /create-pj.", ephemeral=True)


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

        random_values = assign_random_values()
        personaje_data = create_character_structure(self.nombre.value, edad, altura, peso, random_values)

        personajes[user_id] = personaje_data
        save_characters(personajes)

        embed = discord.Embed(
            title="Personaje creado",
            description="✅ Tu personaje fue creado correctamente.",
            color=discord.Color.green()
        )

        embed.add_field(
            name="📝 Nombre",
            value=self.nombre.value,
            inline=False
        )
        embed.add_field(
            name="⚡ Atributos",
            value=f"**Clan:** {personaje_data['clan']}\n**Raza:** {personaje_data['raza']}\n**Elemento Principal:** {personaje_data['elemento_principal']}\n**Elemento Secundario:** {personaje_data['elemento_secundario']}",
            inline=False
        )
        embed.add_field(
            name="💪 Estadísticas Iniciales",
            value=f"**Fuerza:** {personaje_data['estadisticas']['fuerza']}\n**Velocidad:** {personaje_data['estadisticas']['velocidad']}\n**Resistencia:** {personaje_data['estadisticas']['resistencia']}\n**Inteligencia:** {personaje_data['estadisticas']['inteligencia']}\n**Chakra:** {personaje_data['estadisticas']['chakra']}",
            inline=False
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_error(self, interaction: discord.Interaction, error: Exception) -> None:
        # Loggear la excepcion completa en consola para debug
        try:
            from config.error_handler import log_exception
            await log_exception(error, interaction, context_text="CreateCharacterModal.on_error")
        except Exception:
            print("[CREATE-PJ] Error al loguear la excepcion:")
            import traceback
            traceback.print_exc()

        # Notificar al usuario de forma ephemera
        try:
            if not interaction.response.is_done():
                await interaction.response.send_message(
                    "❌ Ocurrió un error inesperado al crear tu personaje.",
                    ephemeral=True
                )
            else:
                await interaction.followup.send(
                    "❌ Ocurrió un error inesperado al crear tu personaje.",
                    ephemeral=True
                )
        except Exception:
            # Si tampoco se puede notificar, imprimir en consola
            print("[CREATE-PJ] No se pudo notificar al usuario del error.")


async def setup(bot):

    await bot.add_cog(CreateCharacter(bot))

