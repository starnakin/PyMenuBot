import discord
from discord.ext import commands

from scraper.python_cuisineaz import CuisineAZ
from scraper.python_cuisinejournaldesfemmes import CuisineJournalDesFemmes
from scraper.python_marmiton import Marmiton

from googlesearch import search

import time
class Repa(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name=="repas":
            if not message.author == self.bot.user:
                recette_list=[]
                z=list(search("recette "+message.content, lang='fr', num=10, start=0, stop=10, pause=0))
                for i in z:
                    if str(i).startswith("https://www.marmiton.org/recettes/"):
                        if not str(i).startswith("https://www.marmiton.org/recettes/recherche"):
                            if not str(i).endswith('https://www.marmiton.org/recettes/'):
                                recette_list.append(Marmiton.get(str(i)))

                for recette in recette_list:
                    embed = discord.Embed(title=recette.get("name"))
                    embed.set_image(url=recette.get('image'))
                    embed.set_author(name=recette.get("site"))
                    embed.set_footer(text=recette.get("url"))
                    for ingredient_data in recette.get("ingredients"):
                        for quantity in recette.get("ingredients").get(ingredient_data):
                            embed.add_field(name=ingredient_data, value=(quantity+recette.get("ingredients").get(ingredient_data).get(quantity), 1)[quantity==""])
                    await message.channel.send(embed=embed)
            else:
                await message.add_reaction("✅")

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
        if not member == self.bot.user:
            if channel.name == "repas":
                if payload.emoji.name == "✅":
                    await message.delete()
def setup(bot):
    bot.add_cog(Repa(bot))