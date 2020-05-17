#!/usr/bin/env python3.7.0
# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 13:59
# @Author  : XiaShengSheng
# @FileName: data_processing.py
# @Software: PyCharm
import pandas as pd
import jieba
import pymysql
import re
db_pymysql = pymysql.connect(host='localhost',port=3306,user='root',passwd='666666',db='ReviewDatas',use_unicode=True, charset="utf8")
data = pd.read_sql('select * from jd_mdcomments',con=db_pymysql)
print(data)
# 统计productname下面共有多少条数据
ppgs = data['productname'].value_counts()
print(ppgs)
# 统计共有多少条评论数据
comments = data.mdcomment
print(comments.shape)

# 去重
comments = comments.drop_duplicates()
print(comments.shape)

# 去除掉评论中的\r \n
comments = comments.apply(lambda x: re.sub('\n', '', x))
comments = comments.apply(lambda x: re.sub('\r', '', x))
# 去除掉评论中的html语言下的表情符号&hellip;&hellip;
comments = comments.apply(lambda x: re.sub('&[a-zA-Z]+;', '', x))

meide_xh = data[data.productname == '美的（Midea）2100W速热电热水器60升 遥控预约洗浴 健康洗一级节能 加长防电墙F60-15WB5(Y)']['productxh'].value_counts()
print(meide_xh)


# 自定义函数实现机械压缩（单一重复、过分强调的评论）
def yasuo(str):
    # 这里i代表每次处理的字符单位数，如i=1时处理“好好好好”的情况，i=2时处理“很好很好很好”的情况
    # i=1&i=2时用一种处理方式，即当重复数量>2时才进行压缩，因为出现“滔滔不绝”、“美的的确好”
    # 跟“容我思考思考”“这真的真的好看”等不好归为冗余的情况。但当出现3次及以上时基本就是冗余了。
    for i in [1, 2]:
        j = 0
        while j < len(str) - 2 * i:
            # 判断重复了至少两次
            if str[j: j + i] == str[j + i: j + 2 * i] and str[j: j + i] == str[j + 2 * i: j + 3 * i]:
                k = j + 2 * i
                while k + i < len(str) and str[j: j + i] == str[k + i: k + 2 * i]:
                    k += i
                str = str[: j + i] + str[k + i:]
            j += 1
        i += 1
    # i=3&i=4时用一种处理方式，当重复>1时就进行压缩，因为3个字以上时重复不再构成成语或其他常用语，
    # 基本上即使冗余了。因为大于五个字的重复比较少出现，为了减少算法复杂度可以只处理到i=4。
    for i in [3, 4, 5]:
        j = 0
        while j < len(str) - 2 * i:
            # 判断重复了至少一次
            if str[j: j + i] == str[j + i: j + 2 * i]:
                k = j + i
                while k + i < len(str) and str[j: j + i] == str[k + i: k + 2 * i]:
                    k += i
                str = str[: j + i] + str[k + i:]
            j += 1
        i += 1
    return str


# 验证压缩函数阶段
str1 = yasuo("美的服务真的真的真的真的特别特别好")
print(str1)
comments.astype('str').apply(lambda x: len(x)).sum()
data1 = comments.astype('str').apply(lambda x: yasuo(x))
# 统计每个评论的字符串长度
data1.astype('str').apply(lambda x: len(x)).sum()
data2 = data1.apply(lambda x: len(x))
data3 = pd.concat((data1, data2), axis=1)
print(data3)

# 改变data3的列名
data3.columns = ['评论', '长度']
print(data3)
# 对长度进行统计
data4 = data3['长度'].value_counts().sort_index()[1:198]
print(data4)
# 提取字符长度大于4的
data5 = data3.loc[data3['长度'] > 4, '评论']
print(data5.shape)
# 分词
# 1、是例子
print(list(jieba.cut("我爱中国，天安门的国旗")))
# 2、开始分词
data6 = data5.apply(lambda x: list(jieba.cut(x)))
print(data6)

# 去除停用词
stop = pd.read_csv('data/stoplist.txt', sep='yang', encoding='utf-8', header=None,engine='python')
print(stop)

stop = [' '] + list(stop[0])
data7 = data6.apply(lambda x: [i for i in x if i not in stop])
print(data7)

# 导入情感评价表
feeling = pd.read_csv('data/BosonNLP_sentiment_score.txt', engine='python',sep=' ', encoding='utf-8', header=None)
feeling.columns = ['word', 'score']
print(feeling)

# 定义评分函数  对每条评论进行评分
feel = list(feeling['word'])


def classfi(my_list):
    SumScore = 0
    for i in my_list:
        if i in feel:
            SumScore += feeling['score'][feel.index(i)]
    return SumScore


data8 = data7.apply(lambda x: classfi(x))
print(data8)

# 把评论划分成两部分：正向评价  负向评价
pos = data7[data8 >= 0]
neg = data7[data8 < 0]
data7[data8 == 0]
pos.to_csv('data/pos.txt', encoding='utf-8', index=False, header=False)
neg.to_csv('data/neg.txt', encoding='utf-8', index=False, header=False)

pos = pd.read_csv('data/pos.txt', encoding='utf-8', header=None)
neg = pd.read_csv('data/neg.txt', encoding='utf-8', header=None)

neg[1] = neg[0].apply(lambda s: s.split(' '))  # 定义一个分割函数，然后用 apply 广播
pos[1] = pos[0].apply(lambda s: s.split(' '))


from gensim import models, corpora
# 构造LDA模型，提取关键字
## 负面主题分析
neg_dict = corpora.Dictionary(neg[1])  # 建立词典
neg_corpus = [neg_dict.doc2bow(i) for i in neg[1]]  # 建立语料库
neg_lda = models.LdaModel(neg_corpus, num_topics=3, id2word=neg_dict)  # LDA 模型训练
print("\n负面评价")
for i in range(3):
    print("主题%d : " % i)
    print(neg_lda.print_topic(i))  # 输出每个主题

## 正面主题分析
pos_dict = corpora.Dictionary(pos[1])
pos_corpus = [pos_dict.doc2bow(i) for i in pos[1]]
pos_lda = models.LdaModel(pos_corpus, num_topics=3, id2word=pos_dict)
print("\n正面评价")
for i in range(3):
    print("主题%d : " % i)
    print(pos_lda.print_topic(i))  # 输出每个主题