import discord
from discord.ext import commands
from config.embeds import success_embed, error_embed
from config.error_sender import send_error
from config.errors import ErrorType


class Moderation_Ban(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
    name = "ban",
    help = "Banea a un miembro del servidor"
)
    @commands.has_permissions(ban_members = True)
    async def ban(self, ctx, member: discord.Member, *, reason = None):

        if member == ctx.author:
            await send_error(ctx, ErrorType.SELF_ACTION)
            return
    
        reason = reason or "No se proporcionó una razón."

        try:
            await member.ban(reason=reason)
            await ctx.send(
                embed=success_embed(
                    "Miembro baneado",
                    f"**{member.name}** fue baneado.\n"
                    f"**Razón:** {reason}"
                )
        )

        except discord.Forbidden:
            await send_error(ctx, ErrorType.BOT_PERMISSIONS)


        except discord.HTTPException:
            await send_error(ctx, ErrorType.UNKNOWN)
        

async def setup(bot):
    # Agrega el Cog Moderation_Ban al bot
    await bot.add_cog(Moderation_Ban(bot))