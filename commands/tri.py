from discord.ext import commands

class Tri(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def tri(self, ctx):
        pass
def setup(bot):
    bot.add_cog(Tri(bot))