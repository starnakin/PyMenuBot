class Grocery():
    def __init__(self, store, grocery):
        self.store=store
        self.grocery=grocery
    
    def add(self, article):
        if self.containe_by_name(article.name):
            self.get_article_by_name(article.name).add_quantity(article.quantity)
        else:
            self.grocery.append(article)
        return self

    def remove(self, article):
        if self.containe_by_name(article.name):
            self.grocery.remove(article)
        return self

    def containe(self, article):
        return article in self.grocery 

    def containe_by_name(self, article_name):
        for article in self.grocery:
            if article.name == article_name:
                return article
        return None
    
    def get_article_by_name(self, article_name):
        for article in self.grocery:
            if article.name == article_name:
                return article
        return None

    def sort(self, sort_rule):
        sorted=[]
        for category in sort_rule:
            for article in self.grocery:
                if article.category == category:
                    sorted.append(article)
        return sorted
    
    def containe_similare(self, similar_article):
        for article in self.grocery:
            if article.similar_article == similar_article:
                return True
        return False
    
    def get_similare(self, similar_article):
        for article in self.grocery:
            if article.similar_article == similar_article:
                return article
        return None
    
    def update(self, article, new_article):
        self.grocery[self.grocery.index(article)] = new_article 
        return self.grocery

    def get_article_by_message_id(self, message_id):
        for article in self.grocery:
            if article.message_id == message_id:
                return article
        return None