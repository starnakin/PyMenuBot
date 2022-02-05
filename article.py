from discord import Embed
from utils import get_property_by_product_name
class Article():
    def __init__(self, name, quantity, author, message_id=0, price=0.0,  image="", category="", most_similar=""):
        self.name = name
        self.quantity = quantity
        self.author = author
        property = get_property_by_product_name(name)
        try:
            self.price = property.get("price")
            self.image=property.get("image")
            self.similar_article=property.get("most_similar")
            self.category=property.get("category")
        except:
            self.price = 0.0
            self.image=""
            self.similar_article=name
            self.category="autre"
        self.message_id=message_id
    
    def add_quantity(self, added_quantity):
        self.quantity+=added_quantity
        return self
    
    def to_embed(self):
        embed = Embed()
        embed.set_thumbnail(url=self.image)
        embed.add_field(name=self.name, value=self.quantity)
        embed.set_footer(text=self.similar_article + " | "+str(self.price)+"€"+" | "+self.author)
        return embed
