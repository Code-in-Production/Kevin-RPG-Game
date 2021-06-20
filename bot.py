import os
import discord
from discord.ext import commands

bot = commands.Bot(command_prefix=';')

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

bot.load_extension("gameplay")
bot.run(os.environ["RPG_BOT_TOKEN"])
