import discord
from discord import embeds
from discord.ext import commands
from main import shopping_category

from utils import num
from utils import add_number
from utils import emoji_to_number
from utils import get_property

from article import Article
from grocery import Grocery
from groceries_list import GroceriesList
from groceries_lists import GroceriesLists

from main import groceries_lists

from discord.ext.commands import bot


class Course(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):

        if message.content.startswith('!'):
            return

        if message.channel.category.name==shopping_category:

            if message.author != self.bot.user:

                guild = message.guild

                for line in message.content.split("\n"):

                    name, quantity, price, img= get_property(line)
                    
                    article = Article(name, quantity, message.author.name, price=price, image=img)
                    groceries_list = groceries_lists.get_groceries_list_by_id(guild.id)

                    if groceries_list != None:

                        grocery = groceries_list.get_by_id(message.channel.id)

                        if grocery != None:

                            new_message = await message.channel.send(embed=article.to_embed())
                            article.message_id=new_message.id
                            grocery.add(article)
                            
                        else:
                            groceries_list.add(Grocery(message.channel.id, [article]))
                            new_message = await message.channel.send(embed=article.to_embed())
                            article.message_id=new_message.id
                    else:
                        groceries_lists.add(GroceriesList(guild, Grocery(message.channel.id, [article])))
                        new_message = await message.channel.send(embed=article.to_embed())
                        article.message_id=new_message.id
                    await message.delete()
            else:
                await message.add_reaction("✅")
                embed_quantity = int(message.embeds[0].fields[0].value)
                for i in add_number(1, embed_quantity):
                    await message.add_reaction(i)
                await message.add_reaction("➕")
                await message.add_reaction("🕒")

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        if channel.category.name == shopping_category:
            groceries_list=groceries_lists.get_groceries_list_by_id(channel.guild.id)
            groceries_list.add(Grocery(channel.id, []))

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):

        guild = self.bot.get_guild(payload.guild_id)
        member = guild.get_member(payload.user_id)

        if member != self.bot.user:

            channel = self.bot.get_channel(payload.channel_id)

            if channel.category.name == shopping_category:

                message = await channel.fetch_message(payload.message_id)
                emoji=payload.emoji.name

                groceries_list = groceries_lists.get_groceries_list_by_id(guild.id)
                grocery = groceries_list.get_by_id(channel.id)
                article = grocery.get_article_by_message_id(message.id)

                if emoji == "✅":
                    if article.recurrent:
                        await message.delete()
                        new_message = await message.channel.send(embed=article.to_embed())
                        article.message_id=new_message.id
                    else:
                        grocery.remove(article)
                        await message.delete()

                elif emoji in num:

                    number=emoji_to_number(emoji)
                    old_quantity=int(article.quantity)
                    article.add_quantity(-number)
    
                    await message.edit(embed=article.to_embed())

                    for i in add_number(old_quantity, int(article.quantity)):
                        await message.clear_reaction(i)

                    await message.remove_reaction(emoji, member)

                elif emoji == "➕":

                    await message.edit(embed=article.add_quantity(1).to_embed())

                    for i in add_number(int(article.quantity)-1, int(article.quantity)):
                        await message.add_reaction(i)
                        
                    await message.clear_reaction("➕")
                    await message.add_reaction("➕")
                    await message.clear_reaction("🕒")
                    await message.add_reaction("🕒")
                
                elif emoji == "🕒":

                    await message.edit(embed=article.toogle_recurrency().to_embed())

                    await message.clear_reaction("🕒")
                    await message.add_reaction("🕒")


def setup(bot):
    bot.add_cog(Course(bot))