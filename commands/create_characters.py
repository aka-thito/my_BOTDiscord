import discord
from discord.ext import commands
from discord import app_commands

from config.error_sender import send

from data.characters.manager import CharacterManager
from data.characters.factory import CharacterFactory
from data.characters.validator import CharacterValidator
from data.characters.embeds import CharacterEmbeds
from data.characters.constants import ALDEAS


class CreateCharacter(commands.Cog):

    def __init__(self, bot):

        self.bot = bot

    @app_commands.command(
        name="create-pj",
        description="Crea tu personaje."
    )
    async def create_character(
        self,
        interaction: discord.Interaction
    ):

        # Si ya tiene personaje vivo, avisar y salir
        if CharacterManager.has_alive_character(interaction.user.id):
            await interaction.response.send_message(
                "❌ Ya posees un personaje vivo.",
                ephemeral=True
            )
            return

        # Mostrar selección de aldea antes de abrir el modal
        class AldeaSelect(discord.ui.Select):
            def __init__(self):
                options = [discord.SelectOption(label=a, value=a) for a in ALDEAS]
                super().__init__(placeholder="Selecciona tu aldea...", min_values=1, max_values=1, options=options)

            async def callback(self, select_interaction: discord.Interaction):
                # Abrir modal con la aldea seleccionada prellenada
                aldea = self.values[0]
                await select_interaction.response.send_modal(CreateCharacterModal(aldea_default=aldea))

        class AldeaView(discord.ui.View):
            def __init__(self, timeout: int = 60):
                super().__init__(timeout=timeout)
                self.add_item(AldeaSelect())

            async def on_timeout(self):
                # No hacer nada especial al expirar
                pass

        view = AldeaView()
        await interaction.response.send_message("Selecciona tu aldea para comenzar:", view=view, ephemeral=True)


    @create_character.error
    async def error(
        self,
        interaction,
        error
    ):

        if interaction.response.is_done():
            sender = interaction.followup.send
        else:
            sender = interaction.response.send_message

        if isinstance(error, app_commands.MissingPermissions):

            await sender(
                "❌ No tienes permisos.",
                ephemeral=True
            )

            return

        if isinstance(error, discord.Forbidden):

            await sender(
                "❌ No tengo permisos.",
                ephemeral=True
            )

            return

        print(error)

        await sender(
            "❌ Error inesperado.",
            ephemeral=True
        )


class CreateCharacterModal(discord.ui.Modal):

    def __init__(self, aldea_default: str = None):
        """Modal para crear personaje. Se puede pasar una aldea por defecto desde la selección previa."""
        super().__init__(
            title="Crear personaje"
        )

        # Campos del modal
        self.nombre = discord.ui.TextInput(
            label="Nombre",
            placeholder="Escribe el nombre de tu personaje"
        )

        self.edad = discord.ui.TextInput(
            label="Edad",
            placeholder="Edad (ej. 18)"
        )

        self.altura = discord.ui.TextInput(
            label="Altura",
            placeholder="Altura en metros (ej. 1.75)"
        )

        self.peso = discord.ui.TextInput(
            label="Peso",
            placeholder="Peso en kg (ej. 70)"
        )

        # El campo aldea se pre-llena con la selección realizada
        self.aldea = discord.ui.TextInput(
            label="Aldea",
            default=aldea_default or "",
            placeholder="Si no se seleccionó, escribe la aldea"
        )

        # Añadir campos al modal
        self.add_item(self.nombre)
        self.add_item(self.edad)
        self.add_item(self.altura)
        self.add_item(self.peso)
        self.add_item(self.aldea)

    async def on_submit(
        self,
        interaction: discord.Interaction
    ):

        try:

            nombre = CharacterValidator.validar_nombre(
                self.nombre.value
            )

            edad = CharacterValidator.validar_edad(
                int(self.edad.value)
            )

            altura = CharacterValidator.validar_altura(
                float(self.altura.value)
            )

            peso = CharacterValidator.validar_peso(
                float(self.peso.value)
            )

            aldea = CharacterValidator.validar_aldea(
                self.aldea.value
            )

        except ValueError as e:

            await interaction.response.send_message(

                str(e),

                ephemeral=True

            )

            return

        personaje = CharacterFactory.crear(

            nombre,

            edad,

            altura,

            peso,

            aldea

        )

        CharacterManager.create_character(

            interaction.user.id,

            personaje

        )

        embed = CharacterEmbeds.created(
            personaje
        )

        await interaction.response.send_message(

            embed=embed,

            ephemeral=True

        )

    async def on_error(
        self,
        interaction,
        error
    ):

        print(error)

        await interaction.response.send_message(

            "❌ Ocurrió un error.",

            ephemeral=True
        )


async def setup(bot):

    await bot.add_cog(
        CreateCharacter(bot)
    )