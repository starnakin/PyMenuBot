from bs4 import BeautifulSoup

import urllib.parse
import urllib.request
import ast
import re

class CuisineActuelle(object):    
    @staticmethod
    def get(url):
        html_content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        name=soup.find("h1", {"class": "articleTitle recipe-title"}).text
        
        image_url=soup.find("div", {"class": "leadImage-image"}).find("img")["src"]
        
        steps_list=[]
        steps_data=soup.find("div", {"class": "recipe-instructionContent"}).findAll("li")
        for i in steps_data:
            steps_list.append(i.text)
        
        people_data=soup.find("input", {"class": "recipeIngredients-yieldInput"})["values"]
        quantity_data=soup.findAll()
        
        data={
            "url": url,
            "name": name,
            "image": image_url,
            "steps": steps_list,
            "ingredients": ""
        }
        
        return data
        
print(CuisineActuelle.get("https://www.cuisineactuelle.fr/recettes/far-breton-nature-278381#"))