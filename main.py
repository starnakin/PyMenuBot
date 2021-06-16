import discord
from discord.ext import commands

import os 
import pickle
import json

prefix=json.load(open("./settings/config.json", "r"))["prefix"]
token=json.load(open("./settings/config.json", "r"))["token"]
shopping_channel_id=json.load(open("./settings/config.json", "r"))["shopping_channel_id"]

groceries = pickle.load(open('./settings/courses_fr.pickle', "rb"))

intents = discord.Intents().all()
bot=commands.Bot(command_prefix=prefix, description="Bot of group !", intents=intents)

@bot.event
async def on_ready():
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