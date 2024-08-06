import disnake
from disnake.ext import commands
import aiohttp
import os
import globals
import aiofiles
import tqdm.asyncio
import mafic


class Music(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot: commands.InteractionBot = bot
        self.pool = mafic.NodePool(self.bot)

    @commands.Cog.listener()
    async def on_ready(self):
        if self.pool.nodes:
            print("Already Connected to server!")
        else:
            await self.add_nodes()
    
    async def add_nodes(self):
        try:
            await self.pool.create_node(
                host="127.0.0.1",
                port=os.getenv("SERVER_PORT"),
                label="MAIN",
                password=os.getenv("LAVALINK_SERVER_PASSWORD")

            )
        except Exception as e:
            print("Couldn't connect to lavalink instance!")
                    

    @commands.slash_command(name="status")
    async def status(self, inter:disnake.CommandInteraction):
        embed = disnake.Embed
        embed.title = "Status"
        embed.description = ""




def setup(bot):
    bot.add_cog(Music(bot))