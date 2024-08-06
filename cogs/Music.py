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
        
        await inter.response.defer()
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
        

        track = tracks[0]
        music_embed = disnake.Embed(
            title=f"Playing Now {track.title}",
            description=f"From {track.source}"
        )
        music_embed.set_thumbnail(track.artwork_url)
        music_embed.set_author(name=track.author)

        queue_embed = disnake.Embed(
            title=f"Queueing {track.title}",
            description=f"From {track.source}"
        )
        queue_embed.set_thumbnail(track.artwork_url)
        queue_embed.set_author(name=track.author)


        await player.play(track)
        return await inter.edit_original_response(embed=music_embed)
    
    @commands.slash_command(name="stop")
    async def stop(self,inter:disnake.CommandInteraction):
        if not inter.author.voice:
            return await inter.send("You are not in a voice channel")
        
        await inter.response.defer()
        if not inter.guild.voice_client:
            player = await inter.user.voice.channel.connect(cls=Player)
        else:
            player = inter.guild.voice_client

        embed = disnake.Embed()
        embed.title = f"Stopping {player.current.title}"
        embed.set_author(name=f"{player.current.author}")
        embed.set_thumbnail(player.current.artwork_url)
        await inter.send(embed=embed)
        await player.stop()

    
def setup(bot):
    bot.add_cog(Music(bot))