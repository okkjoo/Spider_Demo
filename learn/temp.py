import requests
import re

post_url = 'http://exercise.kingname.info/exercise_requests_post'
get_url = 'http://exercise.kingname.info/exercise_requests_get.html'
# html = requests.get(url).content.decode()
# print(html)

data = {'name': 'kingname', 'password': '1234567'}
# html_formdata = requests.post(get_url,json=data).content.decode()
# print(html_formdata)

html = requests.get(get_url).content.decode()
title = re.search('title>(.*?)<', html, re.S).group(1)
content_list = re.findall('<p>(.*?)<', html, re.S)
content_str = '\n'.join(content_list)
print(f'页面标题：{title}')
print(f'页面正文内容：\n{content_str}')