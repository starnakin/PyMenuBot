from os import replace
import discord
from discord import channel
from discord import embeds
from discord.ext import commands
from main import shopping_channel_id

import asyncio

import difflib

import json

from discord.ext.commands import bot

#TODO get the more optimised between delkete message and edit the message
course_dict={}
num=["1️⃣", "2️⃣", "3️⃣" , "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

#TODO recreate this function because is suck
def extractInt(text):
    a="0"
    for i in range(len(text)):
        if text[i].isdigit():
            if i!=0:
                if text[i-1] == " " or text[i-1].isdigit():
                    a+=text[i]
            else:
                a+=text[i]
    return int(a)

#TODO recreate this function because is suck
def removeInt(text):
    a=""
    for i in range(len(text)):
        if text[i].isdigit():
            if i != 0:
                if text[i-1] != " ":
                    a+=text[i]
                elif text[i+1].isdigit():
                    return a

        else:
            a+=text[i]
    return a

def emoji_to_number(emoji):
    for i in range(len(num)):
        if num[i] == emoji:
            return i+1

def message_to_field(message):
    for emb in message.embeds:
        for field in emb.fields:
            return field

def create_embed(key, value, author):
    embed = discord.Embed()
    embed.add_field(name=key, value=value)
    embed.set_footer(text=author)
    return embed

def key_to_message(messages, key):
    for message in messages:
        field = message_to_field(message)
        try:
            if field.name == key:
                return message
        except:
            pass

def get_messages_content(messages, bot):
    messages_content={}
    for message in messages:
        if message.author == bot.user:
            field = message_to_field(message)
            messages_content.update({field.name.lower(): field.value})
    return messages_content

def add_number(old_number, new_number):
    futur_emoji=[]
    if old_number >= 10:
        return []
    if new_number==old_number:
        return []
    if new_number>old_number:
        if new_number > 10:
            for i in range(old_number, 10):
                futur_emoji.append(num[i])
        else:
            for i in range(old_number-1, new_number-1):
                futur_emoji.append(num[i])
    else:
        if new_number > 10:
            return []
        else:
            futur_emoji.append(num[new_number-1])
            for i in range(new_number, old_number):
                futur_emoji.append(num[i])

    return futur_emoji

class Course(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.id==shopping_channel_id:
            if message.author != self.bot.user:
                for line in message.content.split("\n"):

                    messages = await message.channel.history(limit=200).flatten()

                    messages_content=get_messages_content(messages, self.bot)
                    
                    key=removeInt(line)

                    most_similare = difflib.get_close_matches(key.lower(), messages_content.keys(), 1, 0.8)

                    if (extractInt(line)==0):
                        value=1
                    else:
                        value=extractInt(line)
                    
                    author=message.author.name
                    
                    if len(most_similare) == 1:
                        old_message=key_to_message(messages, most_similare[0])
                        await old_message.edit(embed=create_embed(most_similare[0], value+int(messages_content.get(most_similare[0])), author))
                        for i in add_number(value, value+int(messages_content.get(most_similare[0]))):
                            await old_message.add_reaction(i)
                        await old_message.clear_reaction("➕")
                        await old_message.add_reaction("➕")
                        await message.delete()
                    else:
                        await message.channel.send(embed=create_embed(key, value, author))
                        await message.delete()
            else:
                await message.add_reaction("✅")
                field=message_to_field(message)
                if int(field.value)>11:
                    max=10
                else:
                    max=int(field.value)-1
                for i in range(0,max):
                    await message.add_reaction(num[i])
                await message.add_reaction("➕")

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        print(member)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        emoji=payload.emoji.name
        field_value=0
        field_name=""
        field_author=""
        for embed in message.embeds:
            for field in embed.fields:
                field_value=int(field.value)
                field_name=field.name
                field_author=field.author

        if not member == self.bot.user:
            if channel.id == shopping_channel_id:
                if emoji == "✅":
                    await message.delete()
                elif emoji in num:
                    number=emoji_to_number(emoji)
                    await message.edit(embed=create_embed(field_name, field_value-number, field_author))
                    for i in add_number(field_value, field_value-number):
                        await message.clear_reaction(i)
                    if field_value-number>=number:
                        await message.remove_reaction(emoji, member)
                elif emoji == "➕":
                    await message.clear_reaction("➕")
                    if field_value < 11:
                        await message.add_reaction(num[field_value-1])
                    await message.add_reaction("➕")
                    await message.edit(embed=create_embed(field_name, field_value+1, field_author))   

def setup(bot):
    bot.add_cog(Course(bot))