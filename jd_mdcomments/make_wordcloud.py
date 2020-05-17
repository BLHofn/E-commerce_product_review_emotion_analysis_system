#!/usr/bin/env python3.7.0
# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 14:01
# @Author  : XiaShengSheng
# @FileName: make_wordcloud.py
# @Software: PyCharm
from collections import Counter
import jieba

record = open("data/neg.txt", 'r', encoding='utf-8')

#print(record)
#%%
#读取文档，分词，并将分词后的单词用空格连接，形成字符串。
cut_words = ' '
for line in record:
    line.strip('')
    #seg_list = jieba.cut_for_search(line) #搜索引擎模式
    #seg_list = jieba.cut(line,cut_all=True) #全模式
    seg_list = jieba.cut(line) #精准模式
    cut_words += (' '.join(seg_list))

#print(cut_words)

#%%
#读取停用词,形成停用词列表
stop = open("data/stoplist.txt", 'r',encoding='UTF-8')

stop_words=[]
for line in stop:
    line.strip( )
    stop_words.append(line.strip())

#print(stop_words)

#%%
#去除停用词，
cut_list = cut_words.split()
words=[]
for s in cut_list:
    s.strip()
    if s in stop_words:
        continue
    else:
        words.append(s)

print(words)

#%%
#统计词频
c = Counter()
for x in words:
    if len(x) > 1 and x != '\r\n':
        c[x] += 1

print('\n词频统计结果：')
for (k, v) in c.most_common(200):   # 输出词频最高的前200个词
    print("%s:%d" % (k, v))

type(c)
#%%
#自定义字体颜色
import matplotlib.colors as colors
#将字体颜色定义为黑白灰系的颜色
color = ['#d8dcd6','#929591','#59656d','#000000']
colormap = colors.ListedColormap(color)

#%%
#引入词云包，绘制词云图，通过词频绘制词云图
from wordcloud import WordCloud

wordshow = WordCloud(font_path="C:/Windows/Fonts/STSONG.ttf",
             background_color="white"
             ,width=400
             ,height=300
             ,max_words=100
             ,max_font_size=60
             ,collocations=False
             ,colormap=colormap
             ,stopwords=stop_words)
wc = wordshow.fit_words(c)
# wc.to_file('data/pf9.png')
#%%
#停用词去除后，需用空格连接字符
cloudword = ' '.join(words)

print(cloudword)

#%%
#通过自动分词，绘制词云图
wordshow = WordCloud(font_path="C:/Windows/Fonts/STSONG.ttf",
             background_color="white"
             ,width=800
             ,height=600
             ,max_words=150
             ,max_font_size=60
             ,collocations=False
             ,stopwords=stop_words)

wc = wordshow.generate(cloudword)

wc.to_file('data/neg.jpg')