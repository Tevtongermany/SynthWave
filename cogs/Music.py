import math
import disnake
from disnake.ext import commands
import aiohttp
import os
import emoji
import globals
import aiofiles
import tqdm.asyncio
from mafic import NodePool, Player, Playlist, Track, TrackEndEvent, SearchType, EndReason


class Music(commands.Cog):
    def __init__(self, bot):
        super().__init__()
        self.bot: commands.InteractionBot = bot
        self.pool = NodePool(self.bot)
        self.loop = False
        self.queue: list[Track] = []


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

        await inter.response.defer()

        if query.startswith("https://"):
            tracks = await player.fetch_tracks(query)
        else:

            tracks = await player.fetch_tracks(query, search_type=SearchType.SOUNDCLOUD)

        if not tracks:
            return await inter.edit_original_response("No tracks found.")

        if isinstance(tracks, Playlist):
            tracks = tracks.tracks
            if len(tracks) > 1:
                self.queue.extend(tracks[1:])

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


        if player.current:
            self.queue.append(track)
            return await inter.edit_original_response(embed=queue_embed)
        elif not player.current:
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

    @commands.slash_command(name="currently_playing")
    async def currently_playing(self,inter:disnake.CommandInteraction):
        player : Player = inter.guild.voice_client
        if player is None:
            await inter.send(embed=disnake.Embed(title="Nothing is currently playing"))  
            return
        if player.current is None:
            await inter.send(embed=disnake.Embed(title="Nothing is currently playing")) 
            return
        
        embed = disnake.Embed()
        embed.title = f"Currently Playing: {player.current.title} {emoji.EMOJI_VIBIN}"
        embed.set_author(name=player.current.author)
        embed.set_thumbnail(player.current.artwork_url)
        song_lenght = await self.format_time(player.current.length)
        Playback = await self.format_time(player.position)
        embed.description = f"{Playback}/{song_lenght}"
        await inter.send(embed=embed)

    @commands.slash_command(name="volume")
    async def volume(self, inter: disnake.CommandInteraction, volume: int):
        if not inter.author.voice:
            return await inter.send("You are not in a voice channel")
        
        await inter.response.defer()

        if not inter.guild.voice_client:
            player = await inter.user.voice.channel.connect(cls=Player)
        else:
            player = inter.guild.voice_client

        if volume > 100:
            await inter.send(embed= disnake.Embed(title="Cannot set volume over 100!"))
            return

        await player.set_volume(volume)
        embed = disnake.Embed(title=f"Volume set to {volume}! :loud_sound:")

        await inter.send(embed=embed)


    @commands.slash_command(name="queue")
    async def queue(self, inter: disnake.CommandInteraction):
        if not inter.author.voice:
            return await inter.send("You are not in a voice channel")

        if not inter.guild.voice_client:
            player = await inter.user.voice.channel.connect(cls=Player)
        else:
            player = inter.guild.voice_client

        if not player.current:
            await inter.send("No song is playing")
            return

        queue_embed = disnake.Embed(
            title=f"Current Playing Song: [1] {player.current.title} - {player.current.author}",
        )
        queue_embed.description = ""

        for index, song in enumerate(self.queue[:30]):
            queue_embed.description += f"[{index + 2}] {song.title} - {song.author}\n"

        if len(self.queue) > 30:
            queue_embed.description += f" {len(self.queue) - 30} more songs"

        await inter.send(embed=queue_embed)

    async def format_time(self,milliseconds: int):
        total_seconds = milliseconds / 1000
        hours = total_seconds // 3600
        total_seconds %= 3600
        minutes = total_seconds // 60
        seconds = total_seconds % 60
        hours = int(hours)
        minutes = int(minutes)
        seconds = int(seconds)

        if hours >= 1:
            return f"{hours}:{minutes}:{seconds}"
        elif minutes >= 1:
            if seconds <= 9:
                return f"{minutes}:0{seconds}"
            return f"{minutes}:{seconds}"
        else:
            return f"{seconds}"
def setup(bot):
    bot.add_cog(Music(bot))
    print("Reloading")