# form字符串转字典
def dictform(s):
    res = {}
    for line in s.split('&'):
        k, v = line.split('=')
        res[k] = str(v)
    return res


a = 'RsNum=3&Id=11527&Tx=33_1&canTj=1&isNeedAns=0&UTp=Xs&ObjId=3200607035&th_1=21648&wtOR_1=N%5C%7C%2F%5C%7C%2FN%5C%7C%2F%5C%7C%2FN%5C%7C%2F&sF21648_1=N&sF21648_2=&sF21648_3=N&sF21648_4=&sF21648_5=N&sF21648_6=&sF21648_N=6&th_2=21649&wtOR_2=%5C%7C%2F%5C%7C%2F%5C%7C%2F&sF21649_1=&sF21649_2=&sF21649_3=&sF21649_4=&sF21649_N=4&th_3=21650&wtOR_3=1%5C%7C%2F%5C%7C%2F%5C%7C%2F%5C%7C%2F1%5C%7C%2F%5C%7C%2F%5C%7C%2F%5C%7C%2F%5C%7C%2F&sF21650_1=1&sF21650_2=&sF21650_3=&sF21650_4=&sF21650_5=1&sF21650_6=1&sF21650_7=1&sF21650_8=1&sF21650_9=1&sF21650_10=&sF21650_N=10&zw1=&cxStYt=A&zw2=&B2=%CC%E1%BD%BB%B4%F2%BF%A8'
print(dictform(a))
