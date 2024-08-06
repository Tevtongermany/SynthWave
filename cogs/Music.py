import disnake
from disnake.ext import commands
import aiohttp
import os
import globals
import aiofiles
import tqdm.asyncio
class Music(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        ...
                    

        




def setup(bot):
    bot.add_cog(Music(bot))