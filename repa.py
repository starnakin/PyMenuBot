import discord
from discord.ext import commands

from scraper.python_cuisineaz import CuisineAZ
from scraper.python_cuisinejournaldesfemmes import CuisineJournalDesFemmes
from scraper.python_marmiton import Marmiton, RecipeNotFound

from googlesearch import search

class Repa(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name=="repas":
            recette_list=[]

            for i in search("recette "+message.content, lang='fr', num=10, start=0, stop=10, pause=0):
                if(len(recette_list)>3):
                    break
                
                elif str(i).startswith("https://www.cuisineaz.com/recettes/"):
                    recette_list.append(CuisineAZ.get(str(i)))

                elif str(i).startswith("https://cuisine.journaldesfemmes.fr/recette/"):
                    recette_list.append(CuisineJournalDesFemmes.get(str(i)))
                
                elif str(i).startswith("https://www.marmiton.org/recettes/"):
                    if not str(i).startswith("https://www.marmiton.org/recettes/recherche"):
                        recette_list.append(Marmiton.get(str(i)))
            for i in recette_list:
                embed = discord.Embed(title=i.get("name"))
                print(i.get('url'))
                embed.set_image(url=i.get('url'))
                await message.channel.send(embed=embed)

    

def setup(bot):
    bot.add_cog(Repa(bot))