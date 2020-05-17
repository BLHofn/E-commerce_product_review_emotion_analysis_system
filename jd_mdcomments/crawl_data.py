#!/usr/bin/env python3.7.0
# -*- coding: utf-8 -*-
# @Time    : 2020/4/8 13:56
# @Author  : XiaShengSheng
# @FileName: crawl_data.py
# @Software: PyCharm
import re
import requests
import json
import csv
import time
import pymysql

# 数据库配置文件
print('正在尝试连接到mysql服务器...')
db = pymysql.connect(host='localhost', user='root', password='666666', port=3306, db='ReviewDatas')
print('连接成功')
cursor = db.cursor()
# 写入csv文件
# 1. 创建文件对象
f = open('data/jdcomments.csv', 'w', encoding='utf-8')
# 2. 基于文件对象构建 csv写入对象
csv_writer = csv.writer(f)
# 3. 构建列表头
csv_writer.writerow(["电商平台", "订单状态", "产品名称", "用户名", "评论", "产品型号", "产品大小", "订单开始时间", "评论时间"])
headers = {
    'referer': 'https://item.jd.com/1106432.html',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36 Edg/80.0.361.69'
}
url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=1106432&score=0&sortType=5&page=0&pageSize=10&isShadowSku=0&rid=0&fold=1'
for i in range(100):
    print('第 0：','当前页数：', i)
    url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=1106432&score=0&sortType=5&page=' + str(
        i) + '&pageSize=10&isShadowSku=0&rid=0&fold=1'
    resp = requests.get(url, headers=headers)
    redata = re.search('\((.*)\);', resp.text)
    data = json.loads(redata.group(1))
    comments = data['comments']
    for comment in comments:
        mdcomment = comment['content']
        orderstatus = comment['status']
        color = comment['productColor']
        size = comment['productSize']
        user = comment['nickname']
        ordertime = comment['referenceTime']
        commenttime = comment['creationTime']
        productname = comment['referenceName']

        productxh = color + size
        # 4. 写入csv文件内容
        csv_writer.writerow(
            ["京东商城", orderstatus, productname, user, mdcomment, productxh, ordertime, commenttime])
        # 写入数据到数据库
        mess = ("INSERT INTO jd_mdcomments(user,productname,productxh,mdcomment,ordertime) VALUES(%s,%s,%s,%s,%s)")
        data = (user, productname, productxh, mdcomment, ordertime)
        cursor.execute(mess, data)
        db.commit()

        message = {
            'platform': "京东商城",
            'orderStatus': orderstatus,
            'productName': productname,
            'userName': user,
            'content': mdcomment,
            'color': color,
            'size': size,
            'orderTime': ordertime,
            'commentsTime': commenttime,
        }
        print(message)
for j in range(8):
    if j!=(0,4,6):
        for k in range(20):
            print('第：',j,'当前页数：', k)
            url = 'https://club.jd.com/comment/productPageComments.action?callback=fetchJSON_comment98&productId=1106432&score=' + str(j) + '&sortType=5&page=' + str(k) + '&pageSize=10&isShadowSku=0&rid=0&fold=1'
            resp = requests.get(url, headers=headers)
            redata = re.search('\((.*)\);', resp.text)
            data = json.loads(redata.group(1))
            comments = data['comments']
            for comment in comments:
                mdcomment = comment['content']
                orderstatus = comment['status']
                color = comment['productColor']
                size = comment['productSize']
                user = comment['nickname']
                ordertime = comment['referenceTime']
                commenttime = comment['creationTime']
                productname = comment['referenceName']

                productxh = color + size
                # 4. 写入csv文件内容
                csv_writer.writerow(
                    ["京东商城", orderstatus, productname, user, mdcomment, productxh, ordertime, commenttime])
                # 写入数据到数据库
                mess = ("INSERT INTO jd_mdcomments(user,productname,productxh,mdcomment,ordertime) VALUES(%s,%s,%s,%s,%s)")
                data = (user, productname, productxh, mdcomment, ordertime)
                cursor.execute(mess, data)
                db.commit()

                message = {
                    'platform': "京东商城",
                    'orderStatus': orderstatus,
                    'productName': productname,
                    'userName': user,
                    'content': mdcomment,
                    'color': color,
                    'size': size,
                    'orderTime': ordertime,
                    'commentsTime': commenttime,
                }
                print(message)
cursor.close()
db.close()