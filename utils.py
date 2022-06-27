import discord
import GoogleImageScraper

#TODO get the more optimised between delkete message and edit the message
num=["1️⃣", "2️⃣", "3️⃣" , "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]

def get_property(text:str):
    price:str = "0.0"
    name:str = ""
    quantity:str = 1

    text.replace(",", ".")
    args = text.split(" ")
    str_quantity=""
    for arg in args:
        if arg.endswith("€"):
            str_price=""
            for letter in arg[:-1][::-1]:
                if letter.isdigit() or letter == ".":
                    str_price+=letter
            price = str_price[::-1]
        else:
            for letter in arg:
                if letter.isdigit():
                    str_quantity+=letter
                else:
                    name+=arg+" "
                    break
                    break
            if str_quantity == "":
                quantity="1"
            else:
                quantity=str_quantity                    
    try:
        urls=GoogleImageScraper.urls(name)
    except:
        urls=["https://camo.githubusercontent.com/b77f040cd201f7d1555cdd6f6f6eb9eff215d4e94a9c42a3e310f6a69cf51bbb/68747470733a2f2f3430342d706167656e6f74666f756e642e66697265626173656170702e636f6d2f696d672f6c6f676f2e706e67"]
    if len(urls) > 0:
        img = urls[0]
    else:
        img = "https://camo.githubusercontent.com/b77f040cd201f7d1555cdd6f6f6eb9eff215d4e94a9c42a3e310f6a69cf51bbb/68747470733a2f2f3430342d706167656e6f74666f756e642e66697265626173656170702e636f6d2f696d672f6c6f676f2e706e67"

    return name, quantity, price, img

def emoji_to_number(emoji):
    for i in range(len(num)):
        if num[i] == emoji:
            return i+1

def get_max(number):
    if number >10:
        return 10
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