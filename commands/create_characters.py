import discord
from discord import app_commands
from discord.ext import commands

from config.constants import ALDEAS
from services.character_service import CharacterService

char_service = CharacterService()


class CreateCharacter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="create-pj", description="Crea tu personaje.")
    async def create_character(self, interaction: discord.Interaction):
        if char_service.has_alive(str(interaction.user.id)):
            await interaction.response.send_message(
                "❌ Ya posees un personaje vivo.", ephemeral=True
            )
            return

        class AldeaSelect(discord.ui.Select):
            def __init__(self):
                options = [discord.SelectOption(label=a, value=a) for a in ALDEAS]
                super().__init__(
                    placeholder="Selecciona tu aldea...",
                    min_values=1,
                    max_values=1,
                    options=options,
                )

            async def callback(self, select_interaction: discord.Interaction):
                aldea = self.values[0]
                await select_interaction.response.send_modal(
                    CreateCharacterModal(aldea_default=aldea)
                )

        class AldeaView(discord.ui.View):
            def __init__(self, timeout: int = 60):
                super().__init__(timeout=timeout)
                self.add_item(AldeaSelect())

            async def on_timeout(self):
                pass

        view = AldeaView()
        await interaction.response.send_message(
            "Selecciona tu aldea para comenzar:", view=view, ephemeral=True
        )

    @create_character.error
    async def error(self, interaction, error):
        if interaction.response.is_done():
            sender = interaction.followup.send
        else:
            sender = interaction.response.send_message

        if isinstance(error, app_commands.MissingPermissions):
            await sender("❌ No tienes permisos.", ephemeral=True)
            return

        if isinstance(error, discord.Forbidden):
            await sender("❌ No tengo permisos.", ephemeral=True)
            return

        print(error)
        await sender("❌ Error inesperado.", ephemeral=True)


class CreateCharacterModal(discord.ui.Modal):
    def __init__(self, aldea_default: str | None = None):
        super().__init__(title="Crear personaje")
        self.nombre: discord.ui.TextInput = discord.ui.TextInput(
            label="Nombre", placeholder="Escribe el nombre de tu personaje"
        )
        self.edad: discord.ui.TextInput = discord.ui.TextInput(
            label="Edad", placeholder="Edad (ej. 18)"
        )
        self.altura: discord.ui.TextInput = discord.ui.TextInput(
            label="Altura", placeholder="Altura en metros (ej. 1.75)"
        )
        self.peso: discord.ui.TextInput = discord.ui.TextInput(
            label="Peso", placeholder="Peso en kg (ej. 70)"
        )
        self.aldea: discord.ui.TextInput = discord.ui.TextInput(
            label="Aldea",
            default=aldea_default or "",
            placeholder="Si no se seleccionó, escribe la aldea",
        )
        self.add_item(self.nombre)
        self.add_item(self.edad)
        self.add_item(self.altura)
        self.add_item(self.peso)
        self.add_item(self.aldea)

    async def on_submit(self, interaction: discord.Interaction):
        try:
            nombre = char_service.validate_name(self.nombre.value)
            edad = char_service.validate_age(int(self.edad.value))
            altura = char_service.validate_height(float(self.altura.value))
            peso = char_service.validate_weight(float(self.peso.value))
            aldea = char_service.validate_village(self.aldea.value)
        except ValueError as e:
            await interaction.response.send_message(str(e), ephemeral=True)
            return

        personaje = char_service.create(nombre, edad, altura, peso, aldea)
        char_service.save(str(interaction.user.id), personaje)

        embed = discord.Embed(
            title="Personaje creado",
            description=(
                "✅ Tu personaje fue creado correctamente.\n⏳ Está pendiente de aprobación."
            ),
            color=discord.Color.blue(),
        )
        embed.add_field(
            name="Información",
            value=(
                f"**Nombre:** {personaje['nombre']}\n"
                f"**Edad:** {personaje['edad']}\n"
                f"**Altura:** {personaje['altura']}\n"
                f"**Peso:** {personaje['peso']}"
            ),
            inline=False,
        )
        embed.add_field(
            name="Datos",
            value=(
                f"**Clan:** {personaje['clan']}\n"
                f"**Raza:** {personaje['raza']}\n"
                f"**Aldea:** {personaje['aldea']}"
            ),
            inline=False,
        )
        embed.add_field(
            name="Elementos",
            value=(
                f"Principal: {personaje['elemento_principal']}\n"
                f"Secundario: {personaje['elemento_secundario']}"
            ),
            inline=False,
        )
        stats = personaje["estadisticas"]
        embed.add_field(
            name="Estadísticas",
            value=(
                f"Fuerza: {stats['fuerza']}\n"
                f"Velocidad: {stats['velocidad']}\n"
                f"Resistencia: {stats['resistencia']}\n"
                f"Inteligencia: {stats['inteligencia']}\n"
                f"Chakra: {stats['chakra']}"
            ),
            inline=False,
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

    async def on_error(self, interaction, error):
        print(error)
        await interaction.response.send_message("❌ Ocurrió un error.", ephemeral=True)


async def setup(bot):
    await bot.add_cog(CreateCharacter(bot))
