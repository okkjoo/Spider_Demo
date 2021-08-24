# coding=utf-8
from bs4 import BeautifulSoup
import re
import urllib.request, urllib.error
import xlwt
import sqlite3
#匹配规则
findLink = re.compile(r'<a href="(.*?)">')
findImgSrc = re.compile(r'<img.*src="(.*?)"', re.S)
findTitle = re.compile(r'<span class="title">(.*?)</span>')
findRating = re.compile(
    r'<span class="rating_num" property="v:average">(.*?)</span>')
findJudge = re.compile(r'<span>(\d*)人评价</span>')
findInq = re.compile(r'<span class="inq">(.*?)</span>')
findBd = re.compile(r'<div class="bd">.*<p class="">(.*?)</p>', re.S)


def main():
    baseUrl = 'https://movie.douban.com/top250?start='
    # 爬取网页
    dataList = get_data(baseUrl)
    # 保存数据
    savePath = '.\\doubanTop250.xls'
    save_data(savePath)


# 爬取网页
def get_data(baseUrl):
    dataList = []
    for i in range(0, 10):
        url = baseUrl + str(i * 25)
        html = ask_url(url)
        # 逐一解析数据
        soup = BeautifulSoup(html, 'html.parser')
        for item in soup.find_all('div', class_='item'):
            data = []  #保存一部电影的所有信息
            item = str(item)

            link = re.findall(findLink, item)[0]
            data.append(link)

            ImgSrc = re.findall(findImgSrc, item)[0]
            data.append(ImgSrc)

            titles = re.findall(findTitle, item)
            if (len(titles) == 2):
                ctitle = titles[0]
                data.append(ctitle)
                otitle = titles[1].replace("/", "")
                data.append(otitle)
            else:
                data.append(titles[0])
                data.append(" ")

            rating = re.findall(findRating, item)[0]
            data.append(rating)

            judgeNum = re.findall(findJudge, item)[0]
            data.append(judgeNum)

            inq = re.findall(findInq, item)
            if len(inq) != 0:
                inq = inq[0].replace("。", "")
                data.append(inq)
            else:
                data.append(" ")

            bd = re.findall(findBd, item)[0]
            bd = re.sub('<br(\s+)?/>(\s+?)', ' ', bd)
            bd = re.sub('/', ' ', bd)
            data.append(bd.strip())

            dataList.append(data)
    return dataList


#得到指定一个URL的网页内容
def ask_url(url):
    # 模拟浏览器头部信息
    head = {
        "User-Agent":
        " Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.159 Safari/537.36"
    }
    request = urllib.request.Request(url, headers=head)
    html = ""
    try:
        response = urllib.request.urlopen(request)
        html = response.read().decode('utf-8')
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reasoon"):
            print(e.reason)

    return html


#保存数据
def save_data(savePath):
    return


if __name__ == '__main__':
    main()
