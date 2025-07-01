
from keep_alive import keep_alive
from dotenv import load_dotenv
import os
import requests
from bs4 import BeautifulSoup
import random
import json
import os
from dotenv import load_dotenv
from apscheduler.schedulers.asyncio import AsyncIOScheduler
import asyncio
import aiohttp
from keep_alive import keep_alive
from dotenv import load_dotenv
import os
import discord
from discord.ext import commands
from discord.ui import Button, View
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Загрузка конфига
load_dotenv()
TOKEN = os.getenv('DISCORD_BOT_TOKEN')

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

# Загрузка модулей (cogs)
async def load_cogs():
    await bot.load_extension('cogs.games')
    await bot.load_extension('cogs.anime')

@bot.event
async def on_ready():
    print(f"Бот {bot.user.name} готов!")
    await load_cogs()

    # Планировщик для автообновления
    scheduler = AsyncIOScheduler()
    scheduler.add_job(auto_update, 'interval', hours=24)
    scheduler.start()

async def auto_update():
    from cogs.games import update_steam_games
    await update_steam_games()
    print("Автообновление выполнено")

keep_alive()
bot.run(TOKEN)
