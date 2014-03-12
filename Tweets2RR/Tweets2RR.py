# 导入json标准库
import urllib.request
import urllib.parse
import http.cookies
import http.cookiejar
import json
import re
# 导入第三方Twitter API库
from TwitterAPI import TwitterAPI

# Twitter OAuth设置
CONSUMER_KEY = ''
CONSUMER_SECRET = ''
ACCESS_TOKEN_KEY = ''
ACCESS_TOKEN_SECRET = ''

# 人人帐号设置
RENREN_ID = ''
RENREN_PASSWD = ''

# 生成TwitterAPI
TAPI = TwitterAPI(
        consumer_key=CONSUMER_KEY,
        consumer_secret=CONSUMER_SECRET,
        access_token_key=ACCESS_TOKEN_KEY,
        access_token_secret=ACCESS_TOKEN_SECRET
        )

# 抓取Twitter首页信息
def GetTweets(TAPI):
    req = TAPI.request('statuses/home_timeline', {'count': '1'})
    # 解析字符串
    res = req.text
    res = res.lstrip('[')
    res = res.rstrip(']')
    # 相关json处理
    jsn = json.loads(res)
    user = jsn['user']['screen_name']
    text = jsn['text']
    # 组合信息
    message = '[' + user + '] ' + text + ' via Twitter.'
    return message

# 模拟登陆人人网
def RLogin(RENREN_ID, RENREN_PASSWD):
    data = {'email': RENREN_ID, 'password': RENREN_PASSWD}
    temp = urllib.parse.urlencode(data)
    url = temp.encode('utf-8')
    cj = http.cookiejar.CookieJar()
    handler = urllib.request.HTTPCookieProcessor(cj)
    opener = urllib.request.build_opener(handler)
    urllib.request.install_opener(opener)
    res = opener.open('http://www.renren.com/ajaxLogin/login', url)
    res = opener.open('http://www.renren.com/home')
    temp = res.read()
    url = temp.decode('utf-8')
    uid = re.search("'ruid':'(\d+)'", url).group(1)
    return (opener, uid)

# 把从Twitter抓取到的信息发送到人人网
def RSend(RENREN_ID, RENREN_PASSWD):
    get = RLogin(RENREN_ID, RENREN_PASSWD)
    opener = get[0]
    uid = get[1]
    res = opener.open('http://www.renren.com/home')
    temp = res.read()
    url = temp.decode('utf-8')
    rt = re.search("requesttoken=(\S+)", url).group(1)
    rtk = re.search("get_check_x:'(\w+)'", url).group(1)
    message = GetTweets(TAPI)
    data = {
            'content': message,
            'hostid': uid,
            'requestToken': rt,
            '_rtk': rtk,
            'channel': 'renren'
            }
    temp = urllib.parse.urlencode(data)
    url = temp.encode('utf-8')
    res = opener.open('http://shell.renren.com/'+uid+'/status', url)

if __name__ == '__main__':
    RSend(RENREN_ID, RENREN_PASSWD)
