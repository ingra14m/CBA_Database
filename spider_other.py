from lxml import etree
import requests
import pymysql
import re

# 目前原始数据拿到，球员照片还没搞到
url = ""
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36'
}


def getData(baseurl, year):
    datalist = []
    for i in [1,2,4,6,7,8,9,10,11,12,13,14,15,16,113,114,182,368,369]:  # 依次获取1-10页的网页
        url = ""
        # if i < 9:
        #     url = baseurl + "Te00" + str(i + 1) + "/" + str(year) + "/"
        # else:
        #     url = baseurl + "Te0" + str(i + 1) + "/" + str(year) + "/"
        # if i == 2:
        #     url = baseurl + "NTe003" + "/" + str(year) + "/"
        url = baseurl + str(i) +"/"
        # url = url + str(year)
        response = requests.get(url=url, headers=headers)
        # data = response.content.decode().replace("<!--", "").replace("-->", "")
        data = response.content
        parse_data = etree.HTML(data)
        # title_list = parse_data.xpath('/html/body/div[8]/div/div/table//tr')
        title_list = parse_data.xpath('//*[@id="blk01"]/div[1]//a/img')
        final = []
        for title in title_list:
            temp = {}
            temp['name'] = title.xpath('./@alt')[0]
            temp['image'] = title.xpath('./@src')[0]
            datalist.append(temp)

    return datalist

baseurl = "http://cba.sports.sina.com.cn/cba/team/show/"
for year in range(2019,2020):
    data = getData(baseurl, year)

    db = pymysql.connect("localhost", "root", "asdf0506", "CBA")  # 连接数据库
    cursor = db.cursor()  # 创建游标
    table = 'Basic' + str(year)
    for j in range(0, len(data)):
        print(data[j])
        try:
            sql = '''
                update %s set `照片` = %s where %s = `姓名`;
            ''' % (table, '"'+data[j]['image']+'"', '"' + data[j]['name'] + '"')
            cursor.execute(sql)  # 执行SQL语句
            db.commit()  # 将内存中更改的数据提交给数据库
        except:
            continue
    print("Done")

db.close()