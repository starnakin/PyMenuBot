from discord import Embed
class Article():
    def __init__(self, name, quantity="1", author="", message_id=0, price="0.0",  image="", recurrent=False):
        self.name = name
        self.quantity = quantity
        self.author = author
        self.message_id=message_id
        self.image=image
        self.price=price
        self.recurrent = recurrent
    
    def add_quantity(self, added_quantity):
        self.quantity+=added_quantity
        return self
    
    def toogle_recurrency(self):
        self.recurrent = not self.recurrent
        return self
    
    def to_embed(self):
        embed = Embed(title=self.name)
        embed.set_thumbnail(url=self.image)
        embed.add_field(name="quantité", value=self.quantity)
        if self.price != "0.0":
            embed.add_field(name="prix", value=self.price)
        if self.recurrent:
            embed.add_field(name="recurrent", value=self.recurrent)
        embed.set_footer(text=self.author)
        return embed
