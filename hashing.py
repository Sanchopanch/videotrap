import hashlib
# Получить md5 хеш
def getmd5(word,count=1):
    for x in range(count):
        a = hashlib.md5()
        a.update(word.encode('utf-16'))
        word = a.hexdigest()
    return word

if __name__ == "__main__":
    print('sasha:'+getmd5('2728'))
    #sasha:d7374ed42a9c0d14b9dc38e32ca86009