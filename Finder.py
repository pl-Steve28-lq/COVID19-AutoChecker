with open("./schoolCode.txt",'rt',encoding='UTF8') as code:
    a = list(map(lambda x:x.split(","), code.readlines()))

def schoolFinder(name,region):
    for i in a:
        if i[0] == name and i[3] == region: return i[2]
    return None
