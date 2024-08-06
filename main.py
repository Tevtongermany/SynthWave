
import asyncio
import os
from time import sleep
import disnake
from disnake.ext import tasks, commands
from dotenv import load_dotenv
import utils
import colorama

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
        
        if not os.path.exists("/Lavalink/Lavalink.jar"): 
            await utils.download_lavalink()
        else:
            print("Looks like Lavalink already exists! Skipping download")





asyncio.run(bot_setup())


@bot.event
async def on_ready():
    print(f'Bot Started!')

for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f'cogs.{filename[:-3]}')


bot.run(os.getenv("TOKEN"))

