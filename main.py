import discord
from discord.ext import commands
from discord.utils import get

from groceries_lists import GroceriesLists
from groceries_list import GroceriesList
from grocery import Grocery
from article import Article

import os 
import json

prefix=json.load(open("./settings/config.json", "r"))["prefix"]
token=json.load(open("./settings/config.json", "r"))["token"]
shopping_category=json.load(open("./settings/config.json", "r"))["shopping_category_name"]

groceries_lists = GroceriesLists([])

intents = discord.Intents().all()
bot=commands.Bot(command_prefix=prefix, description="Bot of group !", intents=intents)

@bot.event
async def on_ready():
    for guild in bot.guilds:
        groceries_list = GroceriesList(guild.id, [])
        categories = get(guild.categories, name = shopping_category)
        if categories == None:
            categories =await guild.create_category(shopping_category)
        for text_channel in categories.text_channels:
            grocery=Grocery(text_channel.id, [])
            messages = await text_channel.history(limit=1000).flatten()
            for message in messages:
                if message.author == bot.user:
                    for embed in message.embeds:
                        for field in embed.fields:
                            footer=embed.footer.text.split(" | ")
                            groceries_list.add(grocery.add(Article(field.name, int(field.value), footer[2], message_id=int(message.id), most_similar=footer[0])))
        groceries_lists.add(groceries_list)
    print("Bot Started !")

@bot.command()
async def load(ctx, name=None):
    if name:
        bot.load_extension(name)
        print(name, "has been loaded")
        await ctx.send(str(name + " has been loaded"))
    
@bot.command()
async def unload(ctx, name=None):
    if name:
        bot.unload_extension(name)
        print(name, "has been unloaded")
        await ctx.send(str(name + " has been unloaded"))

@bot.command()
async def reload(ctx, name=None):
    if name:
        try:
            bot.reload_extension(name)
            print(name, "has been reloaded")
            await ctx.send(str(name + " has been reloaded"))
        except:
            bot.load_extension(name)
            print(name, "has been loaded")
            await ctx.send(str(name + " has been loaded"))

for folder in ["commands", "events"]:
    for file in os.listdir("./{}".format(folder)):
        if file.endswith(".py"):
            bot.load_extension('{}.{}'.format(folder, file[:-3]))
            print(file, "has been loaded")

bot.run(token)