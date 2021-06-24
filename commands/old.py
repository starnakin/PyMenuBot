from discord.ext import commands

from main import shopping_channel_id
from utils import create_embed
from utils import removeInt
from utils import extractInt
from utils import get_messages_content
from utils import key_to_message

import  difflib

class Old(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def old(self, ctx):
        await ctx.message.delete()
        shopping_channel = self.bot.get_channel(shopping_channel_id)
        messages = await shopping_channel.history(limit=1000).flatten()
        for message in messages:
            if message.author != self.bot.user:
                for line in message.content.split("\n"):
                    print(line)
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
                        await old_message.clear_reaction("➕")
                        await old_message.add_reaction("➕")
                        await message.delete()
                    else:
                        print(value, key)
                        await message.channel.send(embed=create_embed(key, value, author))
                        await message.delete()
                


def setup(bot):
    bot.add_cog(Old(bot))