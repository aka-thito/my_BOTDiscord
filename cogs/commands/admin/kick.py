import discord
from discord.ext import commands
from config.embeds import success_embed, error_embed

class Moderation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(
            
            name = "kick",
            help = "Expulsa a un miembro del servidor"

            )
    
    @commands.has_permissions(kick_members = True)
    async def kick(self, ctx, member: discord.Member, *, reason = None):

        if member == ctx.author:
            await ctx.send(
                embed = error_embed(
                "Acción no permitida",
                "No puedes expulsarte a ti mismo."
                )
            )
            return
        
        reason = reason or "No se proporcionó una razón."

        try:
            await member.kick(reason = reason)
            await ctx.send(
                embed = success_embed(
                    "Miembro expulsado",
                    f"**{member.name}** fue expulsado.\n"
                    f"**Razón:** {reason}"
                )
            )
        
        except discord.Forbidden:
            await ctx.send(
                embed = error_embed(
                    "Permisos insuficientes",
                    "No tengo permisos para expulsar a este miembro."
                )
            )
        
        except discord.HTTPException:
            await ctx.send(
                embed = error_embed(
                    "Error de expulsión",
                    "Error al intentar expulsar al miembro."
                )
            )


    @kick.error
    async def kick_error(self, ctx, error):

        if isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(
                embed = error_embed(
                    "Uso incorrecto!",
                    "Debes mencionar a un usuario. \n\n"
                    "**Uso correcto:** `!kick @usuario [razón]`"
                )
            )
        elif isinstance(error, commands.BadArgument):
            await ctx.send(
                embed = error_embed(
                    "Usuario Invalido",
                    "No pude encontrar al usuario mencionado."
                )
            )

        elif isinstance(error, commands.MissingPermissions):
            await ctx.send(
                embed = error_embed(
                    "Permisos insuficientes",
                    "No tienes permisos para usar este comando."
                )
            )

async def setup(bot):
    await bot.add_cog(Moderation(bot))