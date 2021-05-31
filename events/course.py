import discord
from discord import channel
from discord import embeds
from discord.ext import commands

import difflib

import json

from discord.ext.commands import bot

course_dict={}
num=["1️⃣", "2️⃣", "3️⃣" , "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

def extractInt(text):
    a="0"
    for i in range(len(text)):
        if text[i].isdigit():
            if i!=0:
                if text[i-1] == " ":
                    a+=text[i]
            else:
                a+=text[i]
    return int(a)

def removeInt(text):
    a=""
    for i in range(len(text)):
        if not text[i].isdigit():
            a+=text[i]
        else:
            if i != 0:
                if text[i-1] != " ":
                    a+=text[i]
    return a

def containInt(text):
    for i in range(len(text)):
        if i!=0:
            if text[i].isdigit() & text[i-1] == " ":
                return True
    return False

def emoji_to_number(emoji):
    for i in range(len(num)):
        if num[i] == emoji:
            return i+1

class Course(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name=="liste-de-courses":
            if message.author != self.bot.user:
                for k in message.content.split("\n"):
                    messages = await message.channel.history(limit=200).flatten()
                    messages_content={}
                    for i in messages:
                        for emb in i.embeds:
                            for field in emb.fields:
                                messages_content.update({field.name.lower(): field.value})
                    
                    l = difflib.get_close_matches(removeInt(k).lower(), messages_content.keys(), 1, 0.8)
                    if len(l) == 1:
                        print(l[0])
                        embed = discord.Embed()
                        embed.add_field(name=l[0], value=(extractInt(k),1)[extractInt(k)==0]+extractInt(messages_content.get(l[0])))
                        embed.set_author(name=message.author.name)
                        await message.channel.send(embed=embed)
                        for i in messages:
                            for emb in i.embeds:
                                for field in emb.fields:
                                    if field.name == l[0]:
                                        await i.delete()
                        await message.delete()
                    else:
                        embed = discord.Embed()
                        embed.add_field(name=removeInt(k), value=(extractInt(k),1)[extractInt(k)==0])
                        embed.set_author(name=message.author.name)
                        await message.channel.send(embed=embed)
                        await message.delete()
            else:
                for embed in message.embeds:
                    for field in embed.fields:
                        for i in range(int(field.value)-1):
                            await message.add_reaction(num[i])
                await message.add_reaction("✅")

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
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
            if channel.name == "liste-de-courses":
                if emoji == "✅":
                    await message.delete()
                elif emoji in num:
                    number=emoji_to_number(emoji)
                    await message.delete()
                    embed = discord.Embed()
                    embed.add_field(name=field_name, value=field_value-number)
                    embed.set_author(name=field_author)
                    await message.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Course(bot))