import requests
from bs4 import BeautifulSoup
import json

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