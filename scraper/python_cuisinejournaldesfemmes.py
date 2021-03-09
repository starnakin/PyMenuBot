from bs4 import BeautifulSoup

import urllib.parse
import urllib.request
import ast
import re

class CuisineJournalDesFemmes(object):
    @staticmethod
    def get(url):
        html_content = urllib.request.urlopen(url).read()
        soup = BeautifulSoup(html_content, 'html.parser')
        
        image_url=soup.find("img", {"class": "bu_cuisine_img_noborder photo"})["src"]
        
        try:
            people_data=int(soup.find("span", {"id": "numberPerson"}).text)
        except:
            people_data=int(soup.find("span", {"class": "bu_cuisine_title_3 bu_cuisine_title_3--subtitle"}).text.split(" ")[2])
        
        ingredients_map={}
        ingredients_data = soup.findAll("h3", {"class": "app_recipe_ing_title"})

        for i in ingredients_data:
            try:
                quantity_data = int(i.find("span")["data-quantity"])/people_data
                ingredients_map.update({i.find("span")["data-mesure-singular"]+" "+i.find('a')["alt"]: quantity_data})
            except IOError:
                quantity_data = float(i.find("span")["data-quantity"])/people_data
                ingredients_map.update({i.find("span")["data-mesure-singular"]+" "+i.find('a')["alt"]: quantity_data})
            except:
                ingredients_map.update({i.find("span")["data-mesure-singular"]+" "+i.find('a')["alt"]: i.find("span")["data-quantity"]})

        list_step=[]
        step_data=soup.findAll("li", {"class": "bu_cuisine_recette_prepa"})
        for i in step_data:
            list_step.append(i.text.replace("  ", "").replace("\n", ""))        
        
        rate=soup.find("span", {"class": "jAverage"}).text.replace("                                    ", "").replace("    ", "")+"/5"

        name=soup.find("h1", {"class": "app_recipe_title_page"}).text

        data = {
            "url": url,
            "image": image_url,
            "name": name,
            "ingredients": ingredients_map,
            "steps": list_step,
            "rate": rate
        }

        return data