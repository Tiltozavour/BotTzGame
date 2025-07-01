import discord
from discord.ext import commands
from discord.ui import Button, View
import random
import json
import os
from utils.steam_parser import fetch_steam_games
from utils.embeds import create_game_embed

class GameView(View):
  def __init__(self, game_data):
        super().__init__(timeout=120)
        self.game_data = game_data

        # Кнопка "Steam" только если есть URL
        if game_data.get('url'):
            self.add_item(Button(
                label="Steam",
                url=game_data['url'],
                style=discord.ButtonStyle.link,
                emoji="🔗"
            ))

        # Кнопка "Другая игра"
        self.add_item(Button(
            label="Другая игра",
            style=discord.ButtonStyle.blurple,
            emoji="🔄"
        ))
        
@discord.ui.button(label="Другая игра", style=discord.ButtonStyle.blurple, emoji="🔄")
async def reroll_callback(self, interaction, button):
        new_game = GamesCog.get_random_game()
        if new_game:
            embed = create_game_embed(new_game)
            await interaction.response.edit_message(embed=embed, view=GameView(new_game))
        else:
            await interaction.response.edit_message(
                content=random.choice(RESPONSES["error"]),
                view=None
            )

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


class GamesCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.BANNED_TAGS = ["Аниме", "Free to Play", "Симулятор", "MOBA"]

    @commands.command(name='cmrnt_game')
    async def suggest_game(self, ctx):
        game = self.get_random_game()
        if game:
            await ctx.send(embed=create_game_embed(game), view=GameView(game))
        else:
            await ctx.send("❌ Нет доступных игр")


    def get_random_game(self):
        games = load_games()
        return random.choice(games) if games else None
    


def load_games():
    try:
        if os.path.exists('steam_games.json'):
            with open('steam_games.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        return []
    except Exception as e:
        print(f"Ошибка загрузки игр: {e}")
        return []

async def fetch_steam_games():
    try:
        url = "https://store.steampowered.com/search/?filter=topsellers"
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, 'html.parser')

        games = []
        for item in soup.select('.search_result_row'):
            try:
                name = item.select_one('.title').text.strip()
                tags = [tag.text.strip() for tag in item.select('.search_tag')]
                game_url = item['href'].split('?')[0]  # Очищаем URL от параметров

                if not any(banned.lower() in [tag.lower() for tag in tags] for banned in BANNED_TAGS):
                    games.append({
                        "name": name,
                        "tags": tags,
                        "url": game_url
                    })
            except Exception as e:
                print(f"Ошибка обработки игры: {e}")
                continue

        with open('steam_games.json', 'w', encoding='utf-8') as f:
            json.dump(games, f, ensure_ascii=False, indent=2)

        return games
    except Exception as e:
        print(f"Ошибка парсинга Steam: {e}")
        return []


@commands.command(name='update')
@commands.has_permissions(administrator=True)
async def force_update(self, ctx):
        games = await fetch_steam_games(self.BANNED_TAGS)
    
        await ctx.send(f"✅ Обновлено {len(games)} игр")

async def setup(bot):
    await bot.add_cog(GamesCog(bot))