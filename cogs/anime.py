import discord
from discord.ext import commands
import aiohttp

class AnimeCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name="anime")
    async def random_anime(self, ctx):
        async with aiohttp.ClientSession() as session:
            async with session.get("https://api.jikan.moe/v4/random/anime") as resp:
                data = await resp.json()
                await ctx.send(f"🎌 Аниме: **{data['data']['title']}**\n🔗 {data['data']['url']}")

async def setup(bot):
    await bot.add_cog(AnimeCog(bot))