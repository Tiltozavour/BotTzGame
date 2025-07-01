import discord
from discord.ext import commands
from discord.ui import Button, View
import random

def create_game_embed(game_data):
    if not game_data:
        return discord.Embed(
            title="Ошибка",
            description=random.choice(RESPONSES["error"]),
            color=discord.Color.red()
        )

    embed = discord.Embed(
        title=random.choice(RESPONSES["suggestion"]).format(game=game_data["name"]),
        color=discord.Color.blue()
    )

    if game_data.get("url"):
        embed.url = game_data["url"]

    if game_data.get("tags"):
        embed.add_field(
            name="Теги",
            value=", ".join(game_data["tags"][:5]),
            inline=False
        )

    embed.set_footer(text="Используйте кнопки ниже")
    return embed


# Стили сообщений
RESPONSES = {
    "suggestion": [
        "🎮 **{game}** - вот твой идеальный выбор!",
        "🔥 Готов к чему-то новому? Попробуй **{game}**"
    ],
    "error": [
        "⚠️ Список игр пуст! Сначала используйте !update",
        "❌ Нет доступных игр с текущими фильтрами"
    ]
}

