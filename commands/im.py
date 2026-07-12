import discord
from discord import app_commands
from discord.ext import commands

from services.character_service import CharacterService

char_service = CharacterService()


def _build_character_embed(personaje: dict) -> discord.Embed:
    embed = discord.Embed(
        title=f"🎭 {personaje.get('nombre', 'Desconocido')}", color=discord.Color.blue()
    )
    embed.add_field(
        name="📝 Información",
        value=(
            f"**Edad:** {personaje.get('edad', 'N/A')}\n"
            f"**Altura:** {personaje.get('altura', 'N/A')}m\n"
            f"**Peso:** {personaje.get('peso', 'N/A')}kg"
        ),
        inline=False,
    )
    embed.add_field(
        name="🏘️ Origen",
        value=(
            f"**Aldea:** {personaje.get('aldea', 'N/A')}\n"
            f"**Clan:** {personaje.get('clan', 'N/A')}\n"
            f"**Rango:** {personaje.get('rango', 'N/A')}"
        ),
        inline=False,
    )
    embed.add_field(
        name="⚡ Elementos",
        value=(
            f"**Principal:** {personaje.get('elemento_principal', 'N/A')}\n"
            f"**Secundario:** {personaje.get('elemento_secundario', 'N/A')}"
        ),
        inline=False,
    )
    embed.add_field(name="🏷️ Raza", value=personaje.get("raza", "N/A"), inline=True)
    embed.add_field(
        name="🎯 Especialización", value=personaje.get("especializacion", "N/A"), inline=True
    )
    stats = personaje.get("estadisticas", {})
    embed.add_field(
        name="📊 Estadísticas",
        value=(
            f"**Fuerza:** {stats.get('fuerza', 0)} **Velocidad:** {stats.get('velocidad', 0)}\n"
            f"**Resistencia:** {stats.get('resistencia', 0)} "
            f"**Inteligencia:** {stats.get('inteligencia', 0)}\n"
            f"**Chakra:** {stats.get('chakra', 0)}"
        ),
        inline=False,
    )
    return embed


class MyCharacter(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="im", description="Muestra la ficha de tu personaje")
    async def my_character(self, interaction: discord.Interaction):
        personaje = char_service.get(str(interaction.user.id))
        if not personaje:
            await interaction.response.send_message(
                "❌ No tienes un personaje. Usa `/create-pj` para crear uno.", ephemeral=True
            )
            return

        embed = _build_character_embed(personaje)
        view = CharacterActionsView(str(interaction.user.id))
        await interaction.response.send_message(embed=embed, view=view, ephemeral=True)


class CharacterActionsView(discord.ui.View):
    def __init__(self, user_id: str):
        super().__init__(timeout=120)
        self.user_id = user_id

    @discord.ui.button(label="🎒 Inventario", style=discord.ButtonStyle.primary)
    async def inventory_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        personaje = char_service.get(self.user_id)
        if not personaje:
            await interaction.response.send_message("❌ Personaje no encontrado.", ephemeral=True)
            return

        inventario = personaje.get("inventario", [])
        embed = discord.Embed(title="🎒 Inventario", color=discord.Color.gold())
        if not inventario:
            embed.description = "*No tienes objetos en tu inventario.*"
        else:
            for i, item in enumerate(inventario, 1):
                nombre = item.get("nombre", "Objeto")
                desc = item.get("descripcion", "")
                cantidad = item.get("cantidad", 1)
                valor = f"x{cantidad}"
                embed.add_field(name=f"{i}. {nombre} {valor}", value=desc or "—", inline=False)

        await interaction.response.send_message(embed=embed, ephemeral=True)

    @discord.ui.button(label="⚔️ Habilidades", style=discord.ButtonStyle.success)
    async def abilities_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        personaje = char_service.get(self.user_id)
        if not personaje:
            await interaction.response.send_message("❌ Personaje no encontrado.", ephemeral=True)
            return

        embed = discord.Embed(title="⚔️ Habilidades y Pasivas", color=discord.Color.teal())

        jutsus = personaje.get("jutsus", [])
        habilidades = personaje.get("habilidades", [])
        pasivas = personaje.get("pasivas", [])

        if jutsus:
            embed.add_field(
                name="🌀 Jutsus",
                value="\n".join(
                    f"• {j.get('nombre', j) if isinstance(j, dict) else j}" for j in jutsus
                )
                or "*Ninguno*",
                inline=False,
            )

        if habilidades:
            embed.add_field(
                name="⚡ Habilidades",
                value="\n".join(
                    f"• {h.get('nombre', h) if isinstance(h, dict) else h}" for h in habilidades
                )
                or "*Ninguna*",
                inline=False,
            )

        if pasivas:
            embed.add_field(
                name="🔰 Pasivas",
                value="\n".join(
                    f"• {p.get('nombre', p) if isinstance(p, dict) else p}" for p in pasivas
                )
                or "*Ninguna*",
                inline=False,
            )

        if not jutsus and not habilidades and not pasivas:
            embed.description = "*No tienes habilidades registradas.*"

        await interaction.response.send_message(embed=embed, ephemeral=True)


async def setup(bot):
    await bot.add_cog(MyCharacter(bot))
