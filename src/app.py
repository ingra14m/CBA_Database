from flask import Flask, render_template, request
import pymysql
import sys
import re

sys.path.append("..")

app = Flask(__name__)


@app.route('/')  # 主页
def index():
    return render_template("index.html")  # 默认在templates下找


# 球队的网页
@app.route('/team/<name>')
def team(name):
    db = pymysql.connect(
        user='cba2020',
        passwd='cba2020',
        db='cba2020'
    )
    cursor = db.cursor()
    nameInSql = '"' + name + '"'

    sql_Team = '''
            select `姓名`, `出场数`,(`两分命中数` * 2 + `三分命中数` * 3 + `罚球命中数`)/`出场数`,(`进攻篮板` + `防守篮板`) /`出场数`,`进攻篮板`/`出场数`,`防守篮板`/`出场数`,`助攻`/`出场数`,`抢断`/`出场数`,`盖帽`/`出场数` \
            ,`失误`/`出场数`,`犯规`/`出场数`
            from basic2019
            where `球队` = %s
            order by (`两分命中数` * 2 + `三分命中数` * 3 + `罚球命中数`)/`出场数` DESC ;
    ''' % (nameInSql)

    sql_Team_Infor = '''
            select `城市`,`主教练`,`冠军数`,`助理教练`,`成立时间`,`LOGO`
            from team
            where `球队名` = %s
    ''' % (nameInSql)

    cursor.execute(sql_Team)

    information = []
    alldata = cursor.fetchall()

    for data in alldata:
        information.append(data)

    db.commit()
    cursor.execute(sql_Team_Infor)

    introduce = []
    introData = cursor.fetchall()
    for data2 in introData:
        introduce.append(data2)

    introduce[0] = list(introduce[0])
    print(introduce)

    cursor.close()

    for i in range(len(information)):
        information[i] = list(information[i])

    for i in range(len(information)):
        for j in range(2, len(information[i])):
            information[i][j] = round(float(information[i][j]), 2)

    factor = [["姓名", '出场数', '得分', '篮板', '进攻篮板', '防守篮板', '助攻', '抢断', '盖帽', '失误', '犯规']]
    information = factor + information

    db.close()
    return render_template("player-statics.html", name=name, information=information, introduce=introduce)


# 球员
@app.route('/team/<Name>/<player>')
def player(Name, player):
    db = pymysql.connect(
        user='cba2020',
        passwd='cba2020',
        db='cba2020'
    )
    NameInSQL = '"' + Name + '"'
    playerInSQL = '"' + player + '"'
    cursor = db.cursor()
    basicLib = "basic"
    message = {}  # 球员历年的基础数据
    advanced = []

    for i in range(2011, 2020):
        Lib = basicLib + str(i)
        sql_player = '''
                    select *
                    from %s
                    where `球队` = %s and `姓名` = %s
            ''' % (Lib, NameInSQL, playerInSQL)

        cursor.execute(sql_player)
        alldata2 = cursor.fetchall()

        if alldata2:
            alldata2 = [alldata2[0]]
            message.update({str(i): alldata2})

    cursor.close()

    db.close()
    return render_template("player.html", name=Name, player=player, message=message)


if __name__ == '__main__':
    app.run(debug=True)
