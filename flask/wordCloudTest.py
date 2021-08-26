import sqlite3
import os.path
import jieba  # 绘图
from matplotlib import pyplot as plt  # 绘图，数据可视化
from wordcloud import WordCloud  # 词云
from PIL import Image  # 图片处理
import numpy as np  # 矩阵运算

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "doubanTop250.db")


def connect_db():
    return sqlite3.connect(db_path)


conn = sqlite3.connect("doubanTop250.db")
cur = conn.cursor()
sql = "select introduction from movie250"
data = cur.execute(sql)
text = ''
# stopWord = ['的']
for item in data:
    # print (item[0])
    text = text + item[0]
# print(text)
cur.close()
conn.close()

cut = jieba.cut(text)
string = ' '.join(cut)
# print(string)
# print(len(string))

img = Image.open(r'.\static\assets\img\tree.png')  # 打开遮罩图片
img_arry = np.array(img)  # 将图片转换为数组
wc = WordCloud(
    background_color='white',
    mask=img_arry,
    font_path='msyh.ttc'
    # font_path='C:\Windows\Fonts微软雅黑.ttf'
)
wc.generate_from_text(string)


fig = plt.figure(1)
plt.imshow(wc)
plt.axis('off')  # 是否显示坐标轴

# plt.show()

plt.savefig(r'.\static\assets\img\word.png', dpi=500)
