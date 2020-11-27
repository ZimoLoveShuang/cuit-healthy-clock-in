import re
import requests
import calendar
import datetime

# 学号
username = ''
# 密码
password = ''
# server酱key，官方地址http://sc.ftqq.com/3.version，不写不会推送通知
key = ''

# 是否开启请假，此项设置为True前，必须填写目的地和请假理由，否则不生效
isLeave = False
# 目的地
destination = ''
# 请假理由
reason = ''

# 是否开启周五自动请假，默认请三天，此项设置为True前，必须填写目的地和请假理由，否则无效
isFridayAutoLeave = False


def cookieJarToStr(cookieJar):
    cookieDict = requests.utils.dict_from_cookiejar(cookieJar)
    res = ''
    cnt = 0
    for k in cookieDict.keys():
        cnt += 1
        res += k + '=' + cookieDict[k]
        if cnt < len(cookieDict.keys()):
            res += ';'
    return res


def strToCookieJar(str):
    cookieDict = {}
    for line in str.split(';'):
        name, value = line.strip().split('=', 1)
        cookieDict[name] = value
    return requests.utils.cookiejar_from_dict(cookieDict)


# 登陆
def login():
    # 获取codeKey和后续需要的cookie
    headers = {
        'Host': 'login.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9'
    }
    res = requests.get(url='http://login.cuit.edu.cn/Login/xLogin/Login.asp', headers=headers, allow_redirects=False)
    firstCookies = cookieJarToStr(res.cookies)
    res.encoding = 'gbk'
    codeKey = re.search('<input type="hidden" name="codeKey" value="\d+">', res.text)[0][43:-2]

    # 发送模拟登陆请求包
    data = {
        'WinW': '1536',
        'WinH': '824',
        'txtId': username,
        'txtMM': password,
        'verifycode': '',
        'codeKey': codeKey,
        'Login': 'Check',
        'IbtnEnter.x': '0',
        'IbtnEnter.y': '0',
    }
    headers = {
        'Host': 'login.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': str(len(data)),
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://login.cuit.edu.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://login.cuit.edu.cn/Login/xLogin/Login.asp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': firstCookies
    }
    requests.post(url='http://login.cuit.edu.cn/Login/xLogin/Login.asp', headers=headers, data=data,
                  allow_redirects=False)

    # 重定向到qqLogin
    headers = {
        'Host': 'login.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://login.cuit.edu.cn/Login/xLogin/Login.asp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': firstCookies
    }
    requests.get(url='http://login.cuit.edu.cn/Login/qqLogin.asp', headers=headers, allow_redirects=False)

    # 重定向到jkjd
    headers = {
        'Host': 'jxgl.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://login.cuit.edu.cn/Login/xLogin/Login.asp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    requests.get(url='http://jxgl.cuit.edu.cn/jkdk', headers=headers, allow_redirects=False)

    # 请求jkdk/
    headers = {
        'Host': 'jxgl.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://login.cuit.edu.cn/Login/xLogin/Login.asp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6'
    }
    requests.get(url='http://jxgl.cuit.edu.cn/jkdk/', headers=headers)

    # 重定向到http://jszx-jxpt.cuit.edu.cn/jxgl/xs/netks/sj.asp?jkdk=Y
    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jxgl.cuit.edu.cn/jkdk/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    }
    res = requests.get(url='http://jszx-jxpt.cuit.edu.cn/jxgl/xs/netks/sj.asp?jkdk=Y', headers=headers,
                       allow_redirects=False)
    # 获取到新的cookies
    cookies = cookieJarToStr(res.cookies)

    # 用新的cookies请求http://jszx-jxpt.cuit.edu.cn/Jxgl/UserPub/Login.asp?UTp=Xs
    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jxgl.cuit.edu.cn/jkdk/', 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookies
    }
    requests.get(url='http://jszx-jxpt.cuit.edu.cn/Jxgl/UserPub/Login.asp?UTp=Xs', headers=headers,
                 allow_redirects=False)

    # 用新的cookies请求http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp
    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jxgl.cuit.edu.cn/jkdk/', 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookies
    }
    res = requests.get(url='http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp', headers=headers,
                       allow_redirects=False)
    res.encoding = 'gbk'
    url = re.search('URL=(.*?)">', res.text)[1]

    # 用老的cookies，重定向到url = http://login.cuit.edu.cn/Login/qqLogin.asp?Oid=jszx%2Djxpt%2Ecuit%2Eedu%2Ecn&OSid=96129967
    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jxgl.cuit.edu.cn/jkdk/', 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': firstCookies
    }
    res = requests.get(url=url, headers=headers, allow_redirects=False)
    res.encoding = 'gbk'

    # 新的cookies请求http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp
    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp', 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookies
    }
    requests.get(url='http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp', headers=headers, allow_redirects=False)

    # 新cookies请求http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/syLogin.asp
    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp', 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookies
    }
    requests.get(url='http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/syLogin.asp', headers=headers, allow_redirects=False)

    # 新cookies重定向到http://jszx-jxpt.cuit.edu.cn/Jxgl/UserPub/Login.asp?UTp=Xs&Func=Login
    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp', 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookies
    }
    requests.get(url='http://jszx-jxpt.cuit.edu.cn/Jxgl/UserPub/Login.asp?UTp=Xs&Func=Login', headers=headers,
                 allow_redirects=False)

    # 新cookies重定向到http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/MainMenu.asp
    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp', 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookies
    }
    requests.get(url=url, headers=headers, allow_redirects=False)

    # 新cookies重定向到http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/sj.asp
    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36 Edg/85.0.564.63',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jszx-jxpt.cuit.edu.cn/Jxgl/Login/tyLogin.asp', 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Cookie': cookies
    }
    res = requests.get(url='http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/sj.asp', headers=headers, allow_redirects=False)
    res.encoding = 'gbk'

    id = re.search('&Id=(.*?)target=_self>'.format(username=username),
                   res.text)[0][len('&Id='):-len(' target=_self>')]
    return cookies, id


# 打卡
def clockIn(cookies, id):
    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/sj.asp', 'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookies
    }

    res = requests.get(
        url='http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/sjDb.asp?UTp=Xs&jkdk=Y&ObjId={username}&Id={id}'.format(
            username=username, id=id), headers=headers, allow_redirects=False)
    res.encoding = 'gbk'

    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/sj.asp',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookies
    }
    requests.get(url='http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/' + res.headers['location'], headers=headers,
                 allow_redirects=False)

    if isLeave and len(destination) > 1 and len(reason) > 1:
        data = {
            'RsNum': '4',
            'Id': id,
            'Tx': '33_1',
            'canTj': '1',
            'isNeedAns': '0',
            'UTp': 'Xs',
            'ObjId': username,
            'th_1': '21650',
            'wtOR_1': '1%5C%7C%2F%5C%7C%2F%5C%7C%2F%5C%7C%2F1%5C%7C%2F1%5C%7C%2F1%5C%7C%2F1%5C%7C%2F1%5C%7C%2F',
            'sF21650_1': '1',
            'sF21650_2': '',
            'sF21650_3': '',
            'sF21650_4': '',
            'sF21650_5': '1',
            'sF21650_6': '1',
            'sF21650_7': '1',
            'sF21650_8': '1',
            'sF21650_9': '1',
            'sF21650_10': '',
            'sF21650_N': '10',
            'th_2': '21912',
            'wtOR_2': '',
            'sF21912_1': destination.encode('gbk'),
            'sF21912_2': reason.encode('gbk'),
            'sF21912_3': '1',
            'sF21912_4': '06',
            'sF21912_5': '1',
            'sF21912_6': '23',
            'sF21912_N': '6',
            'th_3': '21648',
            'wtOR_3': 'N%5C%7C%2F%5C%7C%2FN%5C%7C%2F%5C%7C%2FN%5C%7C%2F',
            'sF21648_1': 'N',
            'sF21648_2': '',
            'sF21648_3': 'N',
            'sF21648_4': '',
            'sF21648_5': 'N',
            'sF21648_6': '',
            'sF21648_N': '6',
            'th_4': '21649',
            'wtOR_4': '%5C%7C%2F%5C%7C%2F%5C%7C%2F',
            'sF21649_1': '',
            'sF21649_2': '',
            'sF21649_3': '',
            'sF21649_4': '',
            'sF21649_N': '4',
            'zw1': '',
            'cxStYt': 'A',
            'zw2': '',
            'B2': '%CC%E1%BD%BB%B4%F2%BF%A8'
        }
    else:
        data = {
            'RsNum': '3',
            'Id': id,
            'Tx': '33_1',
            'canTj': '1',
            'isNeedAns': '0',
            'UTp': 'Xs',
            'ObjId': username,
            'th_1': '21648',
            'wtOR_1': 'N%5C%7C%2F%5C%7C%2FN%5C%7C%2F%5C%7C%2FN%5C%7C%2F',
            'sF21648_1': 'N',
            'sF21648_2': '',
            'sF21648_3': 'N',
            'sF21648_4': '',
            'sF21648_5': 'N',
            'sF21648_6': '',
            'sF21648_N': '6',
            'th_2': '21649',
            'wtOR_2': '%5C%7C%2F%5C%7C%2F%5C%7C%2F',
            'sF21649_1': '',
            'sF21649_2': '',
            'sF21649_3': '',
            'sF21649_4': '',
            'sF21649_N': '4',
            'th_3': '21650',
            'wtOR_3': '1%5C%7C%2F%5C%7C%2F%5C%7C%2F%5C%7C%2F1%5C%7C%2F%5C%7C%2F%5C%7C%2F%5C%7C%2F%5C%7C%2F',
            'sF21650_1': '1',
            'sF21650_2': '',
            'sF21650_3': '',
            'sF21650_4': '',
            'sF21650_5': '1',
            'sF21650_6': '1',
            'sF21650_7': '1',
            'sF21650_8': '1',
            'sF21650_9': '1',
            'sF21650_10': '',
            'sF21650_N': '10',
            'zw1': '',
            'cxStYt': 'A',
            'zw2': '',
            'B2': '%CC%E1%BD%BB%B4%F2%BF%A8'
        }
    if isFridayAutoLeave:
        today = datetime.datetime.today()
        if calendar.weekday(today.year, today.month, today.day) == 4:
            data = {
                'RsNum': '4',
                'Id': id,
                'Tx': '33_1',
                'canTj': '1',
                'isNeedAns': '0',
                'UTp': 'Xs',
                'ObjId': username,
                'th_1': '21650',
                'wtOR_1': '1%5C%7C%2F%5C%7C%2F%5C%7C%2F%5C%7C%2F1%5C%7C%2F1%5C%7C%2F1%5C%7C%2F1%5C%7C%2F1%5C%7C%2F',
                'sF21650_1': '1',
                'sF21650_2': '',
                'sF21650_3': '',
                'sF21650_4': '',
                'sF21650_5': '1',
                'sF21650_6': '1',
                'sF21650_7': '1',
                'sF21650_8': '1',
                'sF21650_9': '1',
                'sF21650_10': '',
                'sF21650_N': '10',
                'th_2': '21912',
                'wtOR_2': '',
                'sF21912_1': destination.encode('gbk'),
                'sF21912_2': reason.encode('gbk'),
                'sF21912_3': '1',
                'sF21912_4': '06',
                'sF21912_5': '3',
                'sF21912_6': '23',
                'sF21912_N': '6',
                'th_3': '21648',
                'wtOR_3': 'N%5C%7C%2F%5C%7C%2FN%5C%7C%2F%5C%7C%2FN%5C%7C%2F',
                'sF21648_1': 'N',
                'sF21648_2': '',
                'sF21648_3': 'N',
                'sF21648_4': '',
                'sF21648_5': 'N',
                'sF21648_6': '',
                'sF21648_N': '6',
                'th_4': '21649',
                'wtOR_4': '%5C%7C%2F%5C%7C%2F%5C%7C%2F',
                'sF21649_1': '',
                'sF21649_2': '',
                'sF21649_3': '',
                'sF21649_4': '',
                'sF21649_N': '4',
                'zw1': '',
                'cxStYt': 'A',
                'zw2': '',
                'B2': '%CC%E1%BD%BB%B4%F2%BF%A8'
            }
    print(data)
    headers = {
        'Host': 'jszx-jxpt.cuit.edu.cn',
        'Connection': 'keep-alive',
        'Content-Length': str(len(data)),
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'Origin': 'http://jszx-jxpt.cuit.edu.cn',
        'Content-Type': 'application/x-www-form-urlencoded',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Referer': 'http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/editSj.asp?UTp=Xs&Tx=33_1&ObjId={username}&Id={id}'.format(
            username=username, id=id),
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        'Cookie': cookies
    }
    res = requests.post(url='http://jszx-jxpt.cuit.edu.cn/Jxgl/Xs/netks/editSjRs.asp', headers=headers, data=data,
                        allow_redirects=False)
    res.encoding = 'gbk'
    # print(res.headers)
    # print(res.text)
    msg = re.search('alert(.*?);', res.text)[0][7:-3]
    return msg


# 推送微信消息
def sendMessage(msg):
    if len(key) < 1:
        return
    url = 'https://sc.ftqq.com/' + key + '.send?text=' + msg;
    requests.get(url)


# 提供给腾讯云的启动函数
def main_handler(event, context):
    try:
        cookies, id = login()
        msg = clockIn(cookies, id)
        sendMessage(msg)
    except Exception as e:
        raise e
    else:
        return 'success'


if __name__ == '__main__':
    print(main_handler({}, {}))
