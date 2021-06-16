from discord.ext import commands

import pickle
import requests
from fuzzywuzzy import fuzz
import statistics

from main import shopping_channel_id
from main import groceries

def classify(requete):
    words=requete.split(" ")
    L=[0 for i in range(len(list(groceries.keys())))]
    dic=requests.get('http://api.conceptnet.io/c/fr/'+words[0]).json()
    related=[dic["edges"][i]["end"]["label"] for i in range(1,len(dic["edges"]))]+[dic["edges"][i]["start"]["label"] for i in range(1,len(dic["edges"]))]
    for j in list(groceries.keys()):
        score = []
        for l in range(len(related)):
            for i in range(len(groceries[j])):
                score.append(fuzz.partial_ratio(groceries[j][i], related[l]))
        
        score=statistics.mean(score)
        if L[list(groceries.keys()).index(j)]<score:
            L[list(groceries.keys()).index(j)]=score
        
    return(list(groceries.keys())[L.index(max(L))])

class Tri(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tri(self, ctx):
        await ctx.message.delete()
        channel = self.bot.get_channel(shopping_channel_id)
        messages = await channel.history(limit=200).flatten()
        sorted={}
        for message in messages:
            if message.author == self.bot.user:
                for embeds in message.embeds:
                    for fields in embeds.fields:
                        a=classify(fields.name)
                        try:
                            b=sorted.get(a)
                            b.append(fields.name)
                            sorted.update({a:b})
                        except:
                            sorted.update({a:[fields.name]})
        print(sorted)

    
def setup(bot):
    bot.add_cog(Tri(bot))