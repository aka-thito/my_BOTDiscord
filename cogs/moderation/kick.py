import discord
from discord.ext import commands
from config.embeds import success_embed
from config.error_sender import send_error
from config.errors import ErrorType

class ModerationKick(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(
        name = "kick",
        help = "Expulsa a un miembro del servidor"
    )
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):

        if member == ctx.author:
            await send_error(ctx, ErrorType.SELF_ACTION)
            return

        reason = reason or "No se proporcionó una razón."

        try:
            await member.kick(reason = reason)
            await ctx.send(
                embed=success_embed(
                    "Miembro expulsado",
                    f"**{member.name}** fue expulsado.\n"
                    f"**Razón:** {reason}"
                )
            )

        except discord.Forbidden:
            await send_error(ctx, ErrorType.BOT_PERMISSIONS)

        except discord.HTTPException:
            await send_error(ctx, ErrorType.UNKNOWN)

async def setup(bot):
    await bot.add_cog(ModerationKick(bot))

