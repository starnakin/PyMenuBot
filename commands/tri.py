def setup(bot):
    bot.add_cog(Get(bot))

class Get(commands.Cog):
    def __init__(self, bot):
        self.bot = bot