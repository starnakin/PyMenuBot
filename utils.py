import discord
from bs4 import BeautifulSoup
import urllib
import requests
#TODO get the more optimised between delkete message and edit the message
num=["1️⃣", "2️⃣", "3️⃣" , "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

#TODO recreate this function because is suck
def extractInt(text):
    a="0"
    for i in text:
        if i.isdigit():
            a+=i
    return int(a)

#TODO recreate this function because is suck
def removeInt(text):
    a=""
    for i in(text):
        if not i.isdigit():
            a+=i
    return a

def emoji_to_number(emoji):
    for i in range(len(num)):
        if num[i] == emoji:
            return i+1

def get_max(number):
    if number >10:
        return 10
    else:
         return number

def add_number(old_number, new_number):
    futur_emoji=[]
    if new_number==old_number:
        return []
    if new_number>old_number:
        if old_number > 10:
            return []
        if old_number==0:
            old_number=1
        if new_number > 10:
            for i in range(old_number, 10):
                futur_emoji.append(num[i])
        else:
            for i in range(old_number-1, new_number-1):
                futur_emoji.append(num[i])
    else:
        if new_number > 10:
            return []
        else:
            futur_emoji.append(num[new_number-1])
            if old_number >10:
                max=10
            else:
                max=old_number
            for i in range(new_number, max):
                futur_emoji.append(num[i])

    return futur_emoji

def get_property_by_product_name(product_name):
    html_content = urllib.request.urlopen("https://www.carrefour.fr/s?q="+product_name).read()
    soup = BeautifulSoup(html_content, 'html.parser')

    first_result=soup.find_all("li", {"class": "product-grid-item"})[0]

    most_similar=first_result.text.replace("\n", "").replace("  ", "")

    product_url="https://www.carrefour.fr"+first_result.find("a", {"class":"product-card-image"})["href"]
    img="https://www.carrefour.fr"+first_result.find("a", {"class":"product-card-image"}).find("img")["data-src"]

    #quantity=soup.find_all("div", {"class": "ds-format ds-product-card__shimzone--small"}) #TODO make work it

    price=float(first_result.find("div", {"class": "product-card-price__price"}).text.replace("\n", "").replace(" ", "").replace("€", "").replace(",", "."))

    html_content = urllib.request.urlopen(product_url).read()
    soup = BeautifulSoup(html_content, 'html.parser')

    category=soup.find_all("li", {"class":"breadcrumb-trail__item"})[2].text
    
    return {"image": img, "price": price, "category": category, "most_similar": most_similar}
