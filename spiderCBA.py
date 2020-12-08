import pandas as pd
import numpy
import urllib.request
from bs4 import BeautifulSoup
import urllib.error
import sqlite3
import xlwt
import sys
import re
import pymysql
import requests


def main():
    baseurl = "http://cbadata.sports.sohu.com/teams/team_tech/"   # 爬取的网页
    for year in range(2019, 2020):

        datalist = getData(baseurl, year) # 获取data
        # savePath = ".\\CBAdata"  + str(year) + ".xls"# 存储的路径

        saveData(datalist, year)  # 保存，写到硬盘中

team = ["八一","吉林","四川","浙江","江苏","山东","广东","新疆","上海","广州","辽宁","北京","福建","深圳","山西","广厦","天津","青岛","同曦","北控"]
findName = re.compile(r'<td><a href=".*?">(.*?)</a></td>')  # 引号内的括号是必加的，如果.*不加限制，会直接匹配到最后
findData = re.compile(r'<td>(\d+.*\d?|-)</td>')
findTitle = re.compile(r'<th>(.*?)</th>')
# findImage = re.compile(r'<img.*?src="(.*?)"', re.S)  # 使.包括换行符
# findTitle = re.compile(r'<span class="title">(.*?)</span>')
# findStar = re.compile(r'<span class="rating_num" property="v:average">(.*?)</span>')
# findJudge = re.compile(r'<span>(\d*)人评价</span>')
# findQuo = re.compile(r'<span class="inq">(.*?)</span>')
# findBD = re.compile(r'<p class="">(.*?)</p>', re.S)    # .*?是有门道的，因为如果没有?就会匹配到最后那个</p>

url = ""
def getData(baseurl, year):
    datalist = []
    for i in range(0,13):             # 依次获取1-10页的网页
        url = ""
        if i < 9:
            url = baseurl + "Te00" + str(i + 1) + "/" + str(year) + "/" + str(year) + "/"
        else:
            url = baseurl + "Te0" + str(i + 1) + "/" + str(year) + "/" + str(year) + "/"
        if i == 2:
            url = baseurl + "NTe003" + "/" + str(year) + "/" + str(year) + "/"
    response = requests.get(url=url, headers=self.headers)



    for i in range(25,31):             # 依次获取25-30页的网页
        if i == 26:
            continue
        url = baseurl + "Te0" + str(i) + "/" + str(year) + "/" + str(year) + "/"
        html = askURL(url)            # 保存当前页面获取到的网页的源码

        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all("div", class_ = "cutE"):  # 区分find_all与select的区别，不特殊的是标签，其他类名后要加'_'

            item = str(item)
            data = []  # 存一支CBA球队球员数据的所有信息

            # 这个正则匹配仅仅会输出匹配的规则中  带括号的不确定的部分和匹配规则中未说明的部分
            Name = re.findall(findName, item)         # 爬取名字
            FinialName = list(set(Name))
            FinialName.sort(key=Name.index)
            data.append(FinialName)

            Data = re.findall(findData, item)         # 爬取数据
            NewData = []

            Title = re.findall(findTitle, item)        # 爬取数据的标题
            NewTitle = Title[1:16] + Title[17:32]
            data.append(NewTitle)

            for i in range(0, int(len(Data) / 2), 15):    # 对球员的数据进行分类处理，获得NewData
                subData = []
                for j in range(0 + i, 15 + i):
                    Data[j] = Data[j].replace(",", "")
                    if (Data[j] == "-"):
                        subData.append("0")
                    else:
                        subData.append(Data[j])
                for z in range(0 + i + (len(FinialName)) * 15, 15 + i + (len(FinialName)) * 15):
                    Data[z] = Data[z].replace(",", "")
                    if (Data[z] == "-"):
                        subData.append("0")
                    else:
                        subData.append(Data[z])
                NewData.append(subData)
            data.append(NewData)
            datalist.append(data)

    for i in range(0,2):
        url = baseurl + "NTe0" + str(i + 13) + "/" + str(year) + "/" + str(year) + "/"
        html = askURL(url)  # 保存当前页面获取到的网页的源码

        soup = BeautifulSoup(html, "html.parser")

        for item in soup.find_all("div", class_="cutE"):  # 区分find_all与select的区别，不特殊的是标签，其他类名后要加'_'

            item = str(item)
            data = []  # 存一支CBA球队球员数据的所有信息

            # 这个正则匹配仅仅会输出匹配的规则中  带括号的不确定的部分和匹配规则中未说明的部分
            Name = re.findall(findName, item)  # 爬取名字
            FinialName = list(set(Name))
            FinialName.sort(key=Name.index)
            data.append(FinialName)

            Data = re.findall(findData, item)  # 爬取数据
            NewData = []

            Title = re.findall(findTitle, item)  # 爬取数据的标题
            NewTitle = Title[1:16] + Title[17:32]
            data.append(NewTitle)

            for i in range(0, int(len(Data) / 2), 15):  # 对球员的数据进行分类处理，获得NewData
                subData = []
                for j in range(0 + i, 15 + i):
                    Data[j] = Data[j].replace(",", "")
                    if (Data[j] == "-"):
                        subData.append("0")
                    else:
                        subData.append(Data[j])
                for z in range(0 + i + (len(FinialName)) * 15, 15 + i + (len(FinialName)) * 15):
                    Data[z] = Data[z].replace(",", "")
                    if (Data[z] == "-"):
                        subData.append("0")
                    else:
                        subData.append(Data[z])
                NewData.append(subData)
            data.append(NewData)
            datalist.append(data)

    return datalist

def saveData(savedata, year):

    db = pymysql.connect("localhost","root","asdf0506","CBA" )
    cursor = db.cursor()
    # 使用 execute() 方法执行 SQL 查询
    if year != 2020:
        for i in range(0, len(savedata)):
            col = savedata[i][0]

            team[i] = '"' + team[i] + '"'

            for j in range(0, len(col)):
                # print(savedata[i][2][j])
                col[j] = '"' + col[j] + '"'
                print(col[j], ",".join(savedata[i][2][j][:2]), ",".join(savedata[i][2][j][17:]), year, team[i])
                sql = '''
                    insert into Basic2019
                    VALUES (%s,%s,%s,%d,%s);
                ''' % (col[j], ",".join(savedata[i][2][j][:2]), ",".join(savedata[i][2][j][17:]), year, team[i])
                # print(col[j])
                cursor.execute(sql)
                db.commit()

        db.close()
    else:
        for i in range(0, len(savedata)):
            col = savedata[i][0]

            for j in range(0, len(col)):
                col[j] = '"' + col[j] + '"'
                sql = '''
                    insert into Basic2019
                    VALUES (%s,%s,%s,%d);
                ''' % (col[j], ",".join(savedata[i][2][j][:2]), ",".join(savedata[i][2][j][17:]), year)
                # print(col[j])
                cursor.execute(sql)
                db.commit()

        db.close()

    # for i in range(0, len(savedata)):
    #     SheetName = BaseSheetName + str(i + 1)
    #     worksheet = workbook.add_sheet(SheetName, cell_overwrite_ok=True)
    #
    #     col = savedata[i][0]
    #     row = savedata[i][1]
    #
    #     for j in range(0, len(col)):
    #         worksheet.write(j + 1, 0, col[j])
    #
    #     for j in range(0, len(row)):
    #         worksheet.write(0, j + 1, row[j])
    #
    #     for z in range(0, len(col)):
    #         for k in range(0, len(row)):
    #             worksheet.write(z + 1, k + 1, savedata[i][2][z][k])
    #
    # workbook.save(savePath)

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