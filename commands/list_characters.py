import discord
from discord.ext import commands
from discord import app_commands
import json
import os

ARCHIVO_PERSONAJES = "data/characters.json"


def load_characters():
    if not os.path.exists(ARCHIVO_PERSONAJES):
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


class ListCharacters(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="list-pj",
        description="Lista todos los personajes (Solo administradores)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def list_characters(self, interaction: discord.Interaction):
        personajes = load_characters()
        
        if not personajes:
            await interaction.response.send_message(
                "❌ No hay personajes creados en el sistema.",
                ephemeral=True
            )
            return

        # Crear opciones para el selector
        options = []
        for user_id, personaje_data in personajes.items():
            nombre_personaje = personaje_data.get("nombre", "Desconocido")
            try:
                user = await self.bot.fetch_user(int(user_id))
                nombre_usuario = user.name
            except:
                nombre_usuario = f"Usuario #{user_id}"
            
            label = f"{nombre_personaje} ({nombre_usuario})"
            options.append(
                discord.SelectOption(label=label, value=user_id)
            )

        if not options:
            await interaction.response.send_message(
                "❌ No hay personajes para listar.",
                ephemeral=True
            )
            return

        embed = discord.Embed(
            title="📋 Lista de Personajes",
            description="Selecciona un personaje para ver sus detalles o eliminarlo.",
            color=discord.Color.blue()
        )

        await interaction.response.send_message(
            embed=embed,
            view=CharacterListView(self.bot, options),
            ephemeral=True
        )

    @list_characters.error
    async def list_characters_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ No tienes permisos para usar este comando. Se requieren permisos de administrador.",
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"❌ Error inesperado: {error}",
                ephemeral=True
            )


class CharacterSelect(discord.ui.Select):
    def __init__(self, bot, options):
        self.bot = bot
        super().__init__(placeholder="Selecciona un personaje...", options=options)

    async def callback(self, interaction: discord.Interaction):
        user_id = self.values[0]
        personajes = load_characters()
        personaje_data = personajes.get(user_id)

        if not personaje_data:
            await interaction.response.send_message(
                "❌ El personaje no fue encontrado.",
                ephemeral=True
            )
            return

        try:
            user = await self.bot.fetch_user(int(user_id))
            nombre_usuario = user.name
        except:
            nombre_usuario = f"Usuario #{user_id}"

        embed = discord.Embed(
            title=f"🎭 {personaje_data.get('nombre', 'Desconocido')}",
            description=f"**Propietario:** {nombre_usuario} ({user_id})",
            color=discord.Color.blue()
        )

        embed.add_field(
            name="📝 Información Básica",
            value=f"**Edad:** {personaje_data.get('edad', 'N/A')}\n**Género:** {personaje_data.get('genero', 'N/A')}\n**Altura:** {personaje_data.get('altura', 'N/A')}m\n**Peso:** {personaje_data.get('peso', 'N/A')}kg",
            inline=False
        )
        embed.add_field(
            name="🏘️ Datos del Personaje",
            value=f"**Aldea:** {personaje_data.get('aldea', 'N/A')}\n**Clan:** {personaje_data.get('clan', 'N/A')}\n**Rango:** {personaje_data.get('rango', 'N/A')}\n**Estado Aprobación:** {personaje_data.get('estado_aprobacion', 'N/A')}",
            inline=False
        )
        embed.add_field(
            name="⚡ Elementos",
            value=f"**Cantidad:** {personaje_data.get('cantidad_elementos', 0)}\n**Elementos:** {', '.join(personaje_data.get('elementos', []))}",
            inline=False
        )

        await interaction.response.send_message(
            embed=embed,
            view=ConfirmDeleteView(user_id, personaje_data.get('nombre', 'Desconocido')),
            ephemeral=True
        )


class CharacterListView(discord.ui.View):
    def __init__(self, bot, options):
        super().__init__()
        self.add_item(CharacterSelect(bot, options))


class ConfirmDeleteView(discord.ui.View):
    def __init__(self, user_id, nombre_personaje):
        super().__init__()
        self.user_id = user_id
        self.nombre_personaje = nombre_personaje

    @discord.ui.button(label="❌ Eliminar", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="⚠️ Confirmación de Eliminación",
            description=f"¿Estás seguro de que deseas eliminar el personaje **{self.nombre_personaje}**?\n\nEsta acción **NO se puede deshacer**.",
            color=discord.Color.red()
        )

        await interaction.response.send_message(
            embed=embed,
            view=FinalConfirmDeleteView(self.user_id, self.nombre_personaje),
            ephemeral=True
        )

    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.secondary)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.delete_original_response()


class FinalConfirmDeleteView(discord.ui.View):
    def __init__(self, user_id, nombre_personaje):
        super().__init__()
        self.user_id = user_id
        self.nombre_personaje = nombre_personaje

    @discord.ui.button(label="✅ Confirmar Eliminación", style=discord.ButtonStyle.danger)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        personajes = load_characters()
        
        if self.user_id in personajes:
            del personajes[self.user_id]
            save_characters(personajes)

            embed = discord.Embed(
                title="✅ Personaje Eliminado",
                description=f"El personaje **{self.nombre_personaje}** ha sido eliminado permanentemente del sistema.",
                color=discord.Color.green()
            )

            await interaction.response.send_message(
                embed=embed,
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                "❌ El personaje no fue encontrado.",
                ephemeral=True
            )

    @discord.ui.button(label="❌ Cancelar", style=discord.ButtonStyle.secondary)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.delete_original_response()


async def setup(bot):
    await bot.add_cog(ListCharacters(bot))
