class GroceriesList():
    def __init__(self, guild, groceries):
        self.id = guild
        self.groceries = groceries
    
    def add(self, grocery):
        self.groceries.append(grocery)

    def containe(self, grocery):
        return grocery in self.groceries 

    def get_by_id(self, grocery_id):
        for grocery in self.groceries:
            if grocery.store == grocery_id:
                return grocery
        return None