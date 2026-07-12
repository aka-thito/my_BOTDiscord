import discord
from discord import app_commands
from discord.ext import commands

from services.character_service import CharacterService

char_service = CharacterService()


def _build_character_embed(
    personaje_data: dict, nombre_usuario: str, user_id: str
) -> discord.Embed:
    embed = discord.Embed(
        title=f"🎭 {personaje_data.get('nombre', 'Desconocido')}",
        description=f"**Propietario:** {nombre_usuario} ({user_id})",
        color=discord.Color.blue(),
    )
    embed.add_field(
        name="📝 Información Básica",
        value=(
            f"**Edad:** {personaje_data.get('edad', 'N/A')}\n"
            f"**Altura:** {personaje_data.get('altura', 'N/A')}m\n"
            f"**Peso:** {personaje_data.get('peso', 'N/A')}kg"
        ),
        inline=False,
    )
    status = personaje_data.get("estado_aprobacion", "pendiente")
    emoji = {"aprobado": "✅", "rechazado": "❌", "pendiente": "⏳"}
    embed.add_field(
        name="🏘️ Datos del Personaje",
        value=(
            f"**Aldea:** {personaje_data.get('aldea', 'N/A')}\n"
            f"**Clan:** {personaje_data.get('clan', 'N/A')}\n"
            f"**Rango:** {personaje_data.get('rango', 'N/A')}\n"
            f"**Estado:** {emoji.get(status, '⏳')} {status.capitalize()}"
        ),
        inline=False,
    )
    embed.add_field(
        name="⚡ Elementos",
        value=(
            f"**Principal:** {personaje_data.get('elemento_principal', 'N/A')}\n"
            f"**Secundario:** {personaje_data.get('elemento_secundario', 'N/A')}"
        ),
        inline=False,
    )
    stats = personaje_data.get("estadisticas", {})
    embed.add_field(
        name="📊 Estadísticas",
        value=(
            f"**Fuerza:** {stats.get('fuerza', 'N/A')}\n"
            f"**Velocidad:** {stats.get('velocidad', 'N/A')}\n"
            f"**Resistencia:** {stats.get('resistencia', 'N/A')}"
        ),
        inline=True,
    )
    return embed


class ListCharacters(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="list-pj", description="Gestiona todos los personajes del sistema (Admin)"
    )
    @app_commands.checks.has_permissions(administrator=True)
    async def list_characters(self, interaction: discord.Interaction):
        all_chars = char_service.all()
        if not all_chars:
            await interaction.response.send_message(
                "❌ No hay personajes en el sistema.", ephemeral=True
            )
            return

        pending = char_service.get_pending()
        approved = char_service.get_approved()
        total = len(all_chars)
        pend_count = len(pending)
        aprob_count = len(approved)
        rej_count = total - pend_count - aprob_count

        embed = discord.Embed(
            title="📋 Gestión de Personajes",
            description=(
                f"**Total:** {total}\n"
                f"⏳ **Pendientes:** {pend_count}\n"
                f"✅ **Aprobados:** {aprob_count}\n"
                f"❌ **Rechazados:** {rej_count}"
            ),
            color=discord.Color.blue(),
        )

        options = []
        for uid, data in all_chars.items():
            nombre = data.get("nombre", "Desconocido")
            try:
                user = await self.bot.fetch_user(int(uid))
                label = f"{nombre} ({user.name})"
            except Exception:
                label = f"{nombre} (#{uid})"
            options.append(
                discord.SelectOption(
                    label=label, value=uid, description=data.get("estado_aprobacion", "?")
                )
            )

        if not options:
            await interaction.response.send_message(
                "❌ No hay personajes para mostrar.", ephemeral=True
            )
            return

        await interaction.response.send_message(
            embed=embed, view=CharacterListView(self.bot, options), ephemeral=True
        )

    @list_characters.error
    async def list_characters_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.MissingPermissions):
            await interaction.response.send_message(
                "❌ Se requieren permisos de administrador.", ephemeral=True
            )
        else:
            await interaction.response.send_message(f"❌ Error: {error}", ephemeral=True)


class CharacterSelect(discord.ui.Select):
    def __init__(self, bot, options):
        self.bot = bot
        super().__init__(placeholder="Selecciona un personaje...", options=options)

    async def callback(self, interaction: discord.Interaction):
        user_id = self.values[0]
        personaje_data = char_service.get(user_id)
        if not personaje_data:
            await interaction.response.send_message("❌ Personaje no encontrado.", ephemeral=True)
            return

        try:
            user = await self.bot.fetch_user(int(user_id))
            nombre_usuario = user.name
        except Exception:
            nombre_usuario = f"Usuario #{user_id}"

        embed = _build_character_embed(personaje_data, nombre_usuario, user_id)
        status = personaje_data.get("estado_aprobacion", "pendiente")

        if status == "pendiente":
            view: discord.ui.View = PendingActionsView(user_id, personaje_data.get("nombre", "?"))
        else:
            view = ConfirmDeleteView(user_id, personaje_data.get("nombre", "?"))

        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class CharacterListView(discord.ui.View):
    def __init__(self, bot, options):
        super().__init__()
        self.add_item(CharacterSelect(bot, options))


class PendingActionsView(discord.ui.View):
    def __init__(self, user_id: str, nombre: str):
        super().__init__()
        self.user_id = user_id
        self.nombre = nombre

    @discord.ui.button(label="✅ Aprobar", style=discord.ButtonStyle.success)
    async def approve_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        char_service.approve(self.user_id)
        embed = discord.Embed(
            title="✅ Personaje Aprobado",
            description=f"**{self.nombre}** ha sido aprobado.",
            color=discord.Color.green(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="❌ Rechazar", style=discord.ButtonStyle.danger)
    async def reject_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        char_service.reject(self.user_id)
        embed = discord.Embed(
            title="❌ Personaje Rechazado",
            description=f"**{self.nombre}** ha sido rechazado.",
            color=discord.Color.red(),
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)


class ConfirmDeleteView(discord.ui.View):
    def __init__(self, user_id: str, nombre_personaje: str):
        super().__init__()
        self.user_id = user_id
        self.nombre_personaje = nombre_personaje

    @discord.ui.button(label="🗑️ Eliminar", style=discord.ButtonStyle.danger)
    async def delete_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        embed = discord.Embed(
            title="⚠️ Confirmación",
            description=(
                f"¿Eliminar **{self.nombre_personaje}**"
                " permanentemente?\n\n"
                "Esta acción **NO se puede deshacer**."
            ),
            color=discord.Color.red(),
        )
        await interaction.response.send_message(
            embed=embed,
            view=FinalConfirmDeleteView(self.user_id, self.nombre_personaje),
            ephemeral=True,
        )

    @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.secondary)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.delete_original_response()


class FinalConfirmDeleteView(discord.ui.View):
    def __init__(self, user_id: str, nombre_personaje: str):
        super().__init__()
        self.user_id = user_id
        self.nombre_personaje = nombre_personaje

    @discord.ui.button(label="✅ Confirmar Eliminación", style=discord.ButtonStyle.danger)
    async def confirm_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        if char_service.get(self.user_id):
            char_service.delete(self.user_id)
            embed = discord.Embed(
                title="✅ Personaje Eliminado",
                description=f"**{self.nombre_personaje}** ha sido eliminado permanentemente.",
                color=discord.Color.green(),
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message("❌ Personaje no encontrado.", ephemeral=True)

    @discord.ui.button(label="Cancelar", style=discord.ButtonStyle.secondary)
    async def cancel_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await interaction.response.defer()
        await interaction.delete_original_response()


async def setup(bot):
    await bot.add_cog(ListCharacters(bot))
