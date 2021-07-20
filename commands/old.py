import discord
from discord import embeds
from discord.ext import commands
from discord.ext.commands import bot

from main import groceries_lists
from main import shopping_category

from utils import num
from utils import removeInt
from utils import extractInt
from utils import add_number

from article import Article
from grocery import Grocery
from groceries_list import GroceriesList
from groceries_lists import GroceriesLists

class Old(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def old(self, ctx):

        if ctx.channel.category.name==shopping_category:

            guild = ctx.guild
            messages = await ctx.channel.history(limit=1000).flatten()
            for message in messages:
                if message.content.startswith('!'):
                    await message.delete()
                else:
                    if message.author != self.bot.user:

                        for line in message.content.split("\n"):

                            quantity = extractInt(line)

                            if quantity == 0:
                                quantity=1
                            
                            article = Article(removeInt(line), quantity, message.author.name)
                            groceries_list = groceries_lists.get_groceries_list_by_id(guild.id)

                            if groceries_list != None:

                                grocery = groceries_list.get_by_id(message.channel.id)

                                if grocery != None:

                                    similar_article = grocery.get_similare(article.similar_article)

                                    if similar_article != None:

                                        old_message = await message.channel.fetch_message(similar_article.message_id)
                                        similar_article.add_quantity(article.quantity)
                                        await old_message.edit(embed=similar_article.to_embed())

                                        for i in add_number(similar_article.quantity-article.quantity, similar_article.quantity):
                                            await old_message.add_reaction(i)

                                        await old_message.clear_reaction("➕")
                                        await old_message.add_reaction("➕")

                                    else:
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

def setup(bot):
    bot.add_cog(Old(bot))