import discord
from discord.ext import commands

import asyncio

import cogs

import os 
import time
import threading
import json
import mysql.connector

prefix=json.load(open("/home/starnakin/Documents/home-helper-discord.py/settings/config.json", "r"))["prefix"]
token=json.load(open("/home/starnakin/Documents/home-helper-discord.py/settings/config.json", "r"))["token"]

bot=commands.Bot(command_prefix=prefix, description="Bot of group !")

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

for i in ["commands", "events"]:
    for file in os.listdir("/home/starnakin/Documents/home-helper-discord.py/{}".format(i)):
        if file.endswith(".py"):
            bot.load_extension('{}.{}'.format(i, file[:-3]))
            print(file, "has been loaded")
bot.load_extension("repa")

bot.run(token)