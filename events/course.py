import discord
from discord.ext import commands

class Course(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.channel.name=="liste-de-courses":
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