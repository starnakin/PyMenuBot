# -*- coding: utf-8 -*-

from bs4 import BeautifulSoup

import urllib.parse
import urllib.request

import re

class Marmiton(object):

    @staticmethod
    def get(url):

        html_content = urllib.request.urlopen(url).read()

        soup = BeautifulSoup(html_content, 'html.parser')

        name= soup.find("h1", {"class": "main-title show-more"}).text

        ingredients = {}

        for i in soup.find("ul", {"class": "item-list"}).findAll("div", {"class": "item-list__item item"}):
            ingredients.update({i.find("span", {"class":"ingredient-name show-icon"}).text.replace(" ", "").replace("\n", "") : {i.find("span", {"class": "quantity"}).text.replace(" ", "").replace("\n", "") : i.find("span", {"class": "unit"}).text.replace(" ", "").replace("\n", "")}})

        image = soup.find("div", {"class": "recipe-media-viewer-thumbnail-container"}).find("img")['data-src']

        data ={
            "ingredients": ingredients,
            "name": name,
            "image": image,
            "url": url
        }

        return data