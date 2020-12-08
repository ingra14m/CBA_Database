import pandas as pd
import numpy
import urllib.request
from bs4 import BeautifulSoup
import urllib.error
import sqlite3
import xlwt
import sys
import re


def main():
    baseurl = "http://cba.sports.163.com/team/11000000"   # 爬取的网页
    datalist = getData(baseurl) # 获取data

    savePath = ".\\CBAdata.xls" # 存储的路径

    saveData(savePath, datalist)  # 保存，写到硬盘中

findName = re.compile(r'<td><a href=".*?">(.*?)</a></td>')  # 引号内的括号是必加的，如果.*不加限制，会直接匹配到最后
findData = re.compile(r'<td>(\d.*?)</td>')
findCat = re.compile(r'<td>([\u4e00-\u9fa5]{0,})</td>')

def getData(baseurl):
    datalist = []

    for i in range(1,21):             # 依次获取1-10页的网页
        url = ""
        if i < 10:
            url = baseurl + "0" + str(i) + "/data.html"
        else:
            url = baseurl + str(i) + "/data.html"
        html = askURL(url)            # 保存当前页面获取到的网页的源码

        soup = BeautifulSoup(html, "html.parser")
        for item in soup.find_all("tbody"):  # 区分find_all与select的区别，不特殊的是标签，其他类名后要加'_'

            item = str(item)
            data = []  # 存一支CBA球队球员数据的所有信息

            # 这个正则匹配仅仅会输出匹配的规则中  带括号的不确定的部分和匹配规则中未说明的部分
            Name = re.findall(findName, item)         # 爬取名字
            data.append(Name)

            Data = re.findall(findData, item)         # 爬取数据
            data.append(Data)

            cat = re.findall(findCat, item)
            cat = cat[1:4] + cat[5:11] + cat[12:]
            data.append(cat)

            datalist.append(data)

    return datalist

def saveData(savePath, savedata):

    workbook = xlwt.Workbook(encoding='utf-8')
    BaseSheetName = "Sheet"

    for i in range(0, len(savedata)):
        SheetName = BaseSheetName + str(i + 1) + "sub"
        worksheet = workbook.add_sheet(SheetName, cell_overwrite_ok=True)

        col = savedata[i][0]
        row = savedata[i][2]

        for j in range(0, len(col)):
            worksheet.write(j + 1, 0, col[j])

        for j in range(0, len(row)):
            worksheet.write(0, j + 1, row[j])

        for z in range(0, len(col)):
            for k in range(0, len(row)):
                worksheet.write(z + 1, k + 1, savedata[i][1][z * len(row) + k])

    workbook.save(savePath)

def askURL(url):
    header = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36"
    }
    req = urllib.request.Request(url=url, headers=header)

    html = ""
    try:
        response = urllib.request.urlopen(req)
        html = response.read().decode('utf-8')     # 只是获取源码
    except urllib.error.URLError as e:
        if hasattr(e, "code"):
            print(e.code)
        if hasattr(e, "reason"):
            print(e.reason)
    return html

if __name__ == "__main__" :   # 显式的指定函数进入的入口
    main()
    print("Spider is over!")
