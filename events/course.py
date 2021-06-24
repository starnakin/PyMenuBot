from os import replace
import discord
from discord import channel
from discord import embeds
from discord.ext import commands
from main import shopping_channel_id

import asyncio

import difflib

from utils import num
from utils import get_messages_content
from utils import removeInt
from utils import extractInt
from utils import key_to_message
from utils import create_embed
from utils import get_messages_content
from utils import message_to_property
from utils import add_number
from utils import emoji_to_number
from utils import get_property_by_product_name

from discord.ext.commands import bot


class Course(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.content.startswith('!'):
            return
        if message.channel.id==shopping_channel_id:
            if message.author != self.bot.user:
                for line in message.content.split("\n"):

                    messages = await message.channel.history(limit=1000).flatten()

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
                        content = messages_content.get(most_similare[0])
                        await old_message.edit(embed=create_embed(most_similare[0], value+content.get("value"), author, content.get("image"), content.get("price"), content.get("rayon")))
                        await old_message.clear_reaction("➕")
                        await old_message.add_reaction("➕")
                        await message.delete()
                    else:
                        semiproperty = get_property_by_product_name(key)
                        await message.channel.send(embed=create_embed(key, value, author, semiproperty.get("image"), semiproperty.get("price"), semiproperty.get("rayon")))
                        await message.delete()
            else:
                await message.add_reaction("✅")
                property=message_to_property(message)
                for i in add_number(1, property.get("quantity")):
                    await message.add_reaction(i)
                await message.add_reaction("➕")

    
    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)
        channel = self.bot.get_channel(payload.channel_id)
        message = await channel.fetch_message(payload.message_id)
        emoji=payload.emoji.name
        property = message_to_property(message)
        product=property.get("product")
        quantity=property.get("quantity")
        image=property.get("image")
        author=property.get("author")
        price=property.get("price")
        rayon=property.get("rayon")
        if not member == self.bot.user:
            if channel.id == shopping_channel_id:
                if emoji == "✅":
                    await message.delete()
                elif emoji in num:
                    number=emoji_to_number(emoji)
                    await message.edit(embed=create_embed(product, quantity-number, author, image, price, rayon))
                    for i in add_number(quantity, quantity-number):
                        await message.clear_reaction(i)
                    if quantity-number>=number:
                        await message.remove_reaction(emoji, member)
                elif emoji == "➕":
                    await message.edit(embed=create_embed(product, quantity+1, author, image, price, rayon))

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.channel.id == shopping_channel_id:
            old_number=int(message_to_property(before).get("quantity"))
            new_number=int(message_to_property(after).get("quantity"))
            if new_number>old_number:
                for i in add_number(old_number, new_number):
                    await after.add_reaction(i)
                await before.clear_reaction("➕")
                await before.add_reaction("➕")

    @commands.Cog.listener()
    async def on_raw_message_edit (self, payload):
        try:
            before=payload.cached_message
            channel = bot.get_channel(payload.channel_id)
        except:
            return
        message_id = payload.message_id
        after = await channel.fetch_message(message_id)
        if before.channel.id == shopping_channel_id:
            old_number=int(message_to_property(before).get("quantity"))
            new_number=int(message_to_property(after).get("quantity"))
            if new_number>old_number:
                for i in add_number(old_number, new_number):
                    await after.add_reaction(i)
                await before.clear_reaction("➕")
                await before.add_reaction("➕")

def setup(bot):
    bot.add_cog(Course(bot))