import discord
from discord.ext import commands

import difflib

def extractInt(text):
    a="0"
    for i in text:
        if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            a+=i
    return int(a)

def removeInt(text):
    return ''.join([i for i in text if not i.isdigit()]) 

def containInt(text):
    for i in text:
        if i in ["0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]:
            return True
    return False

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
                        await message.channel.send(embed=embed)
                        await message.delete()
            else:
                await message.add_reaction("✅")

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        member = self.bot.get_guild(payload.guild_id).get_member(payload.user_id)
        if not member == self.bot.user:
            if channel.name == "liste-de-courses":
                if payload.emoji.name == "✅":
                    await message.delete()

def setup(bot):
    bot.add_cog(Course(bot))