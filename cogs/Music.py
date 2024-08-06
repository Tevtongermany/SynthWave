import math
import disnake
from disnake.ext import commands
import aiohttp
import os
import globals
import aiofiles
import tqdm.asyncio
from mafic import NodePool, Player, Playlist, Track, TrackEndEvent, SearchType, EndReason


class Music(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot: commands.InteractionBot = bot
        self.pool = NodePool(self.bot)

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
                port=int(os.getenv("SERVER_PORT")),
                label="MAIN",
                password=os.getenv("LAVALINK_SERVER_PASSWORD")

            )
        except Exception as e:
            print("Couldn't connect to lavalink instance!" + str(e))
                    

    @commands.slash_command(name="status")
    async def status(self, inter:disnake.CommandInteraction):
        embeds:list[disnake.Embed] = []
        for node in self.pool.nodes:
            embed = disnake.Embed()
            embed.title = f"Node: {node.label}"
            if node.get_player(inter.author.guild.id) is None:
                embed.description = "No Players Connected"
            else:
                embed.description = f"{node.get_player(inter.author.guild.id)}"
            embeds.append(embed)
        await inter.send(embeds=embeds)


    @commands.slash_command(name="play")
    async def play(self, inter:disnake.CommandInteraction,query:str):
        if not inter.author.voice:
            return await inter.send("You are not in a voice channel")
        
        if not inter.guild.voice_client:
            player = await inter.user.voice.channel.connect(cls=Player)
        else:
            player = inter.guild.voice_client

        if query.startswith("https://"):
            tracks = await player.fetch_tracks(query)
        else:
            tracks = await player.fetch_tracks(query, search_type=SearchType.YOUTUBE)

        if not tracks:
            return await inter.edit_original_response("No tracks found.")
        
def setup(bot):
    bot.add_cog(Music(bot))