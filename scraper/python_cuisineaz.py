from bs4 import BeautifulSoup

import urllib.parse
import urllib.request
import ast
import re


class CuisineAZ(object):
    @staticmethod
    def get(url):

        html_content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        image_url=soup.find("img", {"id": "ContentPlaceHolder_recipeImg"})["data-src"]
        
        people_data=int(soup.find("span", {"id": "ContentPlaceHolder_LblRecetteNombre"}).text.split(" ")[0])

        ingredients_map={}
        ingredients_data = soup.find("ul", {"class": "txt-dark-gray"}).findAll("li")
        for i in ingredients_data:
            try:
                quantity_data = int(i.text.split(" ")[0])/people_data
                ingredients_map.update({i.text.replace(i.text.split(" ")[0], ""): quantity_data})
            except IOError:
                quantity_data = float(i.text.split(" ")[0].replace(",", "."))/people_data
                ingredients_map.update({i.text.replace(i.text.split(" ")[0], ""): quantity_data})
            except:
                ingredients_map.update({i.text: ""})
        list_step=[]
        step_data=soup.find("section", {"class": "borderSection instructions"}).findAll("ul", {"data-onscroll": ""})[1].findAll("p")
        for i in step_data:
            list_step.append(i.text)        
        
        rate=5

        name=soup.find("h1", {"class":"recipe-title"}).text

        data = {
            "url": url,
            "image": image_url,
            "name": name,
            "ingredients": ingredients_map,
            "steps": list_step,
            "rate": rate
        }

        return data