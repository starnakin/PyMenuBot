import discord
from bs4 import BeautifulSoup
import requests
import uuid

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


    html_content = requests.get("https://www.auchan.fr/recherche?text="+product_name).text
    soup = BeautifulSoup(html_content, 'html.parser')

    detail = soup.findAll("a", {"class": "product-thumbnail__details-wrapper"})
    if detail != None:
        img= detail[0].find("figure").find("img")["src"]
        most_similar=detail[0].find("p", {"class":"product-thumbnail__description"}).text.replace("  ","").replace("\n", "")
    else:
        img="https://www.torkartingowy.eu/wp-content/uploads/2021/03/mobile_404.png"
        most_similar=str(product_name)

    price=0
    category=str(uuid.uuid4())

    return {"image": img, "price": price, "category": category, "most_similar": most_similar}
