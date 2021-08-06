#发送请求
import requests
import random
from time import sleep
#提取网页信息所需
import re
#保存数据所需
import os
import json

#各步骤所需方法


def get_page(url):
    ''' 
    获取单个 url 资源
    url:str
    return 包装后的对象，要取text 才是相应文本
  '''
    #headers伪装
    headers = {
        'User-Agent':
        'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.121 Safari/537.36'
    }
    #增大请求间隔
    sleep(random.uniform(3, 7))
    #正式发送请求
    i = 0  #重试计数器
    while i < 5:
        try:
            response = requests.get(url, headers=headers, timeout=5)
            if response.status_code == 200:  #正常返回时
                return response
            else:
                raise requests.exceptions.RequestException
        except requests.exceptions.RequestException:
            print('!reconnecting!')
            sleep(random.uniform(0.5, 1))
            i += 1
    return None  #放弃本次获取


def get_pic(url, name):
    '''
  获取图片，并按照给定名称进行保存
  name 文件名 不包含扩展名部分
  '''
    fileName = name + '.jpg'
    if os.path.exists(fileName):
        #跳过已经下载的图片
        return
    pic = get_page(url).content
    with open(fileName, 'wb+') as f:
        f.write(pic)


def extract(text, exp):
    '''
  使用给定的正则表达式从给定的文本中提取信息
  ：para text：str,给定的文本
  ：para exp：re.compile()的返回值类型
  ：return: list 返回全部符合正则表达式的匹配结果
  '''
    result = re.findall(exp, text)
    return result


def save_json(content, name):
    '''
  保存内容为 json 文件
  ：para content ：list or dict
  ：para name ：str
  '''
    fileName = name + '.json'
    j_file = json.dumps(content)  #转换到json文件
    with open(fileName, 'w', encoding='utf-8') as f:
        f.write(j_file)


#主逻辑

if __name__ == '__main__':
    #数据存储
    data = []
    #创建保存图片的文件夹
    if not os.path.exists('pic'):
        os.makedirs('pic')
    #url跳转——顺序修改url，根据页码
    for page_index in range(0, 250, 25):
        url = 'https://movie.doubancom/top250?start={}&filter='.format(
            page_index)
        #获取当前页面
        html = get_page(url).text

        #.遍历当前页面的各个电影
        html = extract(html,
                      re.compile(r'<ol class="grid_view">(.*?)</ol>',
                                  re.S))[0]
        chunks = extract(html, re.compile(r'<li>(.*?></li>', re.S))

        for i, chunk in enumerate(chunks):
            film_index = page_index + i + 1

            #对应当前电影的列表项
            info = {}
            info['index'] = film_index

            #标题
            title_exp = re.compile(r'<span class="title">(.*?)</span>', re.S)
            title_inf = extract(chunk, title_exp)
            info['title'] = title_inf[0]
            print('{}\t{}'.format(film_index, info['title']))

            #海报
            pic_exp = re.compile(
                r'<div class="pic">.*?<img.*?src="(.*?)".*?>.*?</div>', re.S)
            pic_url = extract(chunk, pic_exp)
            pic_name = 'pic' + os.path.sep + str(film_index) + ' ' + str(
                info['title'])
            #get_pic(pic_url[0], pic_name)

            # 导演
            director_exp = re.compile(r'<div class="bd">.*?导演: (.*?)&.*?</div>', re.S)
            director_inf = extract(chunk, director_exp)
            info['director'] = director_inf[0].split(' / ')
            print('\t{}'.format(info['director']))

            # 上映日期+地区+类型
            try:
              general_exp = re.compile(r'<div class="bd">.*?<br>(.*?)</p>.*?</div>', re.S)
              general_inf = extract(chunk, general_exp)[0].replace('&nbsp;', '').split('/')
              date_inf = general_inf[0].replace('\n', '').replace(' ', '')
              region_inf = general_inf[1].split(' ')
              genre_inf = extract(general_inf[2], re.compile(r'(.*)\n', re.S))[0].split(' ')
              info['date'] = date_inf
              info['region'] = region_inf
              info['genre'] = genre_inf
              print('\t{} {} {}'.format(date_inf, region_inf, genre_inf))
            except:
              info['date'] = '0'
              info['region'] = []
              info['genre'] = []

            data.append(info) # 新增列表项
    #保存记录
    fileName = 'info'
    save_json(data, fileName)
