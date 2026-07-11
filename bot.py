import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv

from database import setup_database
from cogs.tickets import TicketView, CloseTicketView

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(
    command_prefix="!",
    intents=intents,
    help_command=None
)

COGS = [
    "cogs.tickets",
]


@bot.event
async def setup_hook():
    # Database
    await setup_database()

    # Load cogs
    for cog in COGS:
        try:
            await bot.load_extension(cog)
            print(f"✅ Loaded {cog}")
        except Exception as e:
            print(f"❌ Failed to load {cog}: {e}")

    # Persistent buttons
    bot.add_view(TicketView())
    bot.add_view(CloseTicketView())

    # Sync slash commands
    try:
        synced = await bot.tree.sync()
        print(f"✅ Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Slash command sync failed: {e}")


@bot.event
async def on_ready():
    print("-" * 40)
    print(f"Logged in as: {bot.user}")
    print(f"Bot ID: {bot.user.id}")
    print(f"Servers: {len(bot.guilds)}")
    print("KCRP Manager is ready!")
    print("-" * 40)


@bot.event
async def on_command_error(ctx, error):
    print(f"Command Error: {error}")


async def main():
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
