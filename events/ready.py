from discord.ext import commands

from config.logging_config import setup_logging

logger = setup_logging()


class Ready(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        logger.info("%s Está online", self.bot.user)


async def setup(bot):
    await bot.add_cog(Ready(bot))
