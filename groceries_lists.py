class GroceriesLists():
    def __init__(self, groceries_lists):
        self.groceries_lists = groceries_lists
    
    def add(self, groceries_list):
        self.groceries_lists.append(groceries_list)

    def containe_by_id(self, id):
        return groceries_list_id in self.groceries_lists 

    def get_groceries_list_by_id(self, id):
        for groceries_list in self.groceries_lists:
            if groceries_list.id == id:
                return groceries_list
        return None