import os
import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def setup_hook():
    await bot.load_extension("cogs.tickets")
    await bot.tree.sync()

@bot.event
async def on_ready():
    print(f"✅ {bot.user} is online!")

bot.run(TOKEN)
