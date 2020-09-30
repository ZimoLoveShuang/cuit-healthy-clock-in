# 请求头转字典
def dictheaders(header_raw):
    return dict(line.split(": ", 1) for line in header_raw.split("\n") if line != '')


s = '''
Host: jszx-jxpt.cuit.edu.cn
Connection: keep-alive
Content-Length: 557
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
Origin: http://jszx-jxpt.cuit.edu.cn
Content-Type: application/x-www-form-urlencoded
User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Referer: http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/editSj.asp?UTp=Xs&Tx=33_1&ObjId=3200607035&Id=11527
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9
Cookie: ASPSESSIONIDSSTCDQQA=NJJMFEABKABAACLPHCGMFAGH


'''
print(dictheaders(s))
