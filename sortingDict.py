import collections
def ordDic(dic):
    od = collections.OrderedDict(sorted(dic.items(), reverse=True))
    return od

if __name__ == "__main__":
    a = {'2':'a','4':'b','1':'r'}
    print(ordDic(a))