#!/usr/bin/python3

# 官方标准库
import os
import re
import time
# 第三方库
import requests
import feedparser
import dropbox

# 草榴四大版块的RSS设定
ASIA_NON = 'http://t66y.com/rss.php?fid=2'
ASIA_YES = 'http://t66y.com/rss.php?fid=15'
EURO_USA = 'http://t66y.com/rss.php?fid=4'
ANIME = 'http://t66y.com/rss.php?fid=5'

# 抓取RSS
def GetRSS(RSS): ###
    get = feedparser.parse(RSS)
    return get

# 获取包含页面链接在内的原始字符串，比如页面链接和标题
def GetOgl(Feed, i): ###
    get_1 = Feed['entries'][i]['links']
    get_2 = Feed['entries'][i]['title']
    return(get_1, get_2)

# 得到页面链接
def PageLink(String): ###
    s = String[0]
    get = s['href']
    return get

# 抓取页面
def GetPage(Plink): ###
    get = requests.get(Plink)
    get.encoding = 'gbk'
    get = get.text
    return get

# 提取原始特征码，
# 显然这里应该添加try...else...，
# 避免那些没有特征码的网页导致程序抛出异常
def GetFeatuerCode(Page):
    get = re.search(r'http://www.rmdown.com/link.php\?hash=(\w+)', Page)
    try:
        get = get.group(0)
        get = get[36:]
        return get
    except AttributeError:
        return 'None'


# 综合处理页面
def GetMT(stream):
    # 抓取原始字符串和页面名称 ###
    ostr = []
    title = []
    for i in range(0, 20):
        temp = GetOgl(stream, i)
        ostr.append(temp[0])
        title.append(temp[1])

    # 取得页面链接 ###
    plink = []
    for i in range(0, 20):
        temp = PageLink(ostr[i])
        plink.append(temp)

    # 开始抓取页面 ###
    page = []
    for i in range(0, 20):
        temp = GetPage(plink[i])
        page.append(temp)

    # 提取原始特征码 ###
    fcode = []
    for i in range(0, 20):
        if page[i] != 'None':
            temp = GetFeatuerCode(page[i])
            fcode.append(temp)
        else:
            pass
    for i in range(0, len(fcode)):
        print(fcode[i])
    print('-------------------------------------------')

    # 组合成磁链 ###
    magnet = []
    for i in range(0, len(fcode)):
        temp = fcode[i][3:]
        temp = 'magnet:?xt=urn:btih:' + temp
        magnet.append(temp)

    return(magnet, title, len(fcode))

# 上传到Dropbox相关文件夹
def Upload2Dropbox():
    # 首先获取access_token
    f = open('actid.txt', 'r')
    ac = f.readlines()
    ACCESS_TOKEN = ac[0].strip()
    print('ACCESS_TOKEN = ', ACCESS_TOKEN)
    f.close()

    # 登陆
    client = dropbox.client.DropboxClient(ACCESS_TOKEN)

    # 组装文件名
    temp = time.localtime()
    t_str = str(temp.tm_year) + ' - ' + str(temp.tm_mon) + ' - ' + str(temp.tm_mday) + ' ' + '更新.txt'

    # 开始上传文件
    filename = '/亚洲无码区/' + t_str
    f = open('亚洲无码区.txt', 'rb')
    res = client.put_file(filename, f)
    print(res)
    filename = '/亚洲有码区/' + t_str
    f = open('亚洲有码区.txt', 'rb')
    res = client.put_file(filename, f)
    print(res)
    filename = '/欧美原创区/' + t_str
    f = open('欧美原创区.txt', 'rb')
    res = client.put_file(filename, f)
    print(res)
    filename = '/动漫原创区/' + t_str
    f = open('动漫原创区.txt', 'rb')
    res = client.put_file(filename, f)
    print(res)

    return 0

if __name__ == '__main__':
    # 抓取四大版块的RSS ###
    asnon = GetRSS(ASIA_NON)
    asyes = GetRSS(ASIA_YES)
    euusa = GetRSS(EURO_USA)
    anime = GetRSS(ANIME)
    print('Wait...')
    print('-------------------------------------------')

    # 综合处理得到magnet和title ###
    temp = GetMT(asnon)
    asnon_magnet = temp[0]
    asnon_title = temp[1]
    asnon_num = temp[2]
    temp = GetMT(asyes)
    asyes_magnet = temp[0]
    asyes_title = temp[1]
    asyes_non = temp[2]
    temp = GetMT(euusa)
    euusa_magnet = temp[0]
    euusa_title = temp[1]
    euusa_num = temp[2]
    temp = GetMT(anime)
    anime_magnet = temp[0]
    anime_title = temp[1]
    anime_num = temp[2]

    # 删除原有文件
    os.remove('亚洲无码区.txt')
    os.remove('亚洲有码区.txt')
    os.remove('欧美原创区.txt')
    os.remove('动漫原创区.txt')
    print('Writing new files...')
    print('-------------------------------------------')
    # 开始把magent和title 写入相应文件，注意格式控制 ###
    f = open('亚洲无码区.txt', 'w+')
    for i in range(0, asnon_num):
        temp = asnon_title[i] + '\n>>> ' + asnon_magnet[i] + '\n\n'
        f.writelines(temp)
    f.close()
    f = open('亚洲有码区.txt', 'w+')
    for i in range(0, asyes_non):
        temp = asyes_title[i] + '\n>>> ' + asyes_magnet[i] + '\n\n'
        f.writelines(temp)
    f.close()
    f = open('欧美原创区.txt', 'w+')
    for i in range(0, euusa_num):
        temp = euusa_title[i] + '\n>>> ' + euusa_magnet[i] + '\n\n'
        f.writelines(temp)
    f.close()
    f = open('动漫原创区.txt', 'w+')
    for i in range(0, anime_num):
        temp = anime_title[i] + '\n>>> ' + anime_magnet[i] + '\n\n'
        f.writelines(temp)
    f.close()

    # Upload to Dropbox
    print('Uploading to Dropbox...')
    print('-------------------------------------------')
    rc = Upload2Dropbox()
    if rc == 0:
        print('-------------------------------------------')
        print('Successful.')
        print('-------------------------------------------')
    else:
        print('-------------------------------------------')
        print('Failed.')
        print('-------------------------------------------')
