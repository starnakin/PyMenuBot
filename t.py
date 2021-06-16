num=["1️⃣", "2️⃣", "3️⃣" , "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
def add_number(old_number, new_number):
    futur_emoji=[]
    if new_number >= 10:
        return []
    if new_number==old_number:
        return []
    if new_number>old_number:
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
                print(i)
                futur_emoji.append(num[i])

    return futur_emoji

print(add_number(0, 15))