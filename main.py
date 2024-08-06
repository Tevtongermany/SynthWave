
import asyncio
import os
import signal
import sys
from time import sleep
import aiohttp
import disnake
from disnake.ext import tasks, commands
from dotenv import load_dotenv
import utils
import colorama
import globals

load_dotenv(".env")

intents = disnake.Intents.default()
client = disnake.Client(intents=intents)

bot = commands.InteractionBot(intents=intents, reload=True)

async def bot_setup():
    if not os.path.exists("config.json"):
        print(F"Welcome to the setup guide for {colorama.Fore.BLUE}Synth{colorama.Fore.CYAN}Wave{colorama.Fore.RESET}")
        sleep(1)
        print("So first thing do you want to have a DJ role? (Basically only the people with this role can interact with the bot)")
        DJ_Role_Input = input("Y/N: ")
        if DJ_Role_Input == "Y":
            DJ_Role = True
            print("Please Enter a Role ID for the Dj Role! Example: 871735248461897758")
            DJ_Role_ID_Input = input("Role ID: ")
        print(f"""
            For {colorama.Fore.BLUE}Synth{colorama.Fore.CYAN}Wave{colorama.Fore.RESET} To Properly work you will need lavalink! 
            But Don't worry we will automatically download it for you!
            """)
        
        if not os.path.exists("./Lavalink.jar"): 
            await utils.download_lavalink()
        else:
            print("Looks like Lavalink already exists! Skipping download")
        print("You are done with the setup!")
    

    
async def check_if_lavalink_running():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"http://localhost:{os.getenv('SERVER_PORT')}/metrics") as r:
                if r.ok:
                    return
    except aiohttp.ClientConnectionError as e:
        print("Couldnt find any existing Lavalink nodes! making new one")

            
    has_right_java_version = utils.has_major_java_version(17)
    if has_right_java_version:
        lavalink_pid = utils.start_lavalink()
        if isinstance(lavalink_pid,int):
            print(f"lavalink running under pid: {lavalink_pid}")
        else:
            print(F"failed to start lavalink! {lavalink_pid}")
    
            


#asyncio.run(bot_setup())
asyncio.run(check_if_lavalink_running())


@bot.event
async def on_ready():
    print(f'\n'
          f'{colorama.Fore.BLUE}Synth{colorama.Fore.CYAN}Wave{colorama.Fore.RESET} V{globals.VERSION}\n'
          f'Running on Disnake Version {disnake.__version__}'
          )
    
    permissions = disnake.Permissions() 
    permissions.connect = True 
    permissions.speak = True 
    permissions.send_messages = True 
    permissions.send_messages = True 
    permissions.manage_messages = True

    invite_url = disnake.utils.oauth_url(bot.user.id, permissions=permissions)
    print(f"Invite link: {invite_url}")

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(os.getenv("TOKEN"))

