from flask import Flask, render_template, request, jsonify
import pymysql
import sys
import json

sys.path.append("..")

app = Flask(__name__)


@app.route('/')  # 主页
def index():
    return render_template("index.html")  # 默认在templates下找


@app.route('/champions')  # 主页
def champions():
    # db = pymysql.connect(
    #     user='root',
    #     passwd='',
    #     db='cba'
    # )
    db = pymysql.connect(
        user='cba2020',
        passwd='cba2020',
        db='cba2020'

    )
    cursor = db.cursor()
    sqlfind = '''
            select `冠军数`
            from team
    '''
    cursor.execute(sqlfind)

    champ = []
    allchamp = cursor.fetchall()
    for data in allchamp:
        champ.append(data)

    db.commit()  # 在哪里commit
    cursor.close()
    db.close()

    return render_template("league-table.html")  # 默认在templates下找


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

    cursor.close()

    for i in range(len(information)):
        information[i] = list(information[i])

    for i in range(len(information)):
        for j in range(2, len(information[i])):
            information[i][j] = round(float(information[i][j]), 2)

    factor = [["姓名", '出场数', '得分', '篮板', '进攻篮板',
               '防守篮板', '助攻', '抢断', '盖帽', '失误', '犯规']]
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
    player0 = player
    if '-' in player:
        player = player.split('-')
        player = "%" + player[-1]
    playerInSQL = '"' + player + '"'
    cursor = db.cursor()
    basicLib = "basic"  # 球员历年的基础数据
    playerinfo = []
    data = []
    advanced = []

    for i in range(2019, 2010, -1):
        Lib = basicLib + str(i)
        if i == 2019:
            sql_player = '''
                    select 年份,球队,出场数,时间/出场数,(两分命中数*2+3*三分命中数+罚球命中数)/出场数,(进攻篮板+防守篮板)/出场数,助攻/出场数,抢断/出场数,盖帽/出场数,失误/出场数,犯规/出场数,if(两分出手数+三分出手数<>0,(两分命中数+三分命中数)/(两分出手数+三分出手数)*100,0),if(三分出手数<>0,(三分命中数)/(三分出手数)*100,0),if(罚球出手数<>0,(罚球命中数)/(罚球出手数)*100,0),位置,球衣号码
                    from %s
                    where `姓名` like %s
                    ''' % (Lib, playerInSQL)
        else:
            sql_player = '''
                    select 年份,球队,出场数,时间/出场数,总得分/出场数,(进攻篮板+防守篮板)/出场数,助攻/出场数,抢断/出场数,盖帽/出场数,失误/出场数,犯规/出场数,命中率,三分命中率,罚球命中率,位置,球衣号码
                    from %s
                    where `姓名` like %s
                    ''' % (Lib, playerInSQL)

        cursor.execute(sql_player)
        alldata2 = cursor.fetchall()

        if alldata2:
            for j in alldata2:
                data.append(j)
            for j in range(len(data)):
                data[j] = list(data[j])

    for i in range(len(data)):
        data[i][3] = ('%.1f' % float(data[i][3]))
        for j in range(4, 11):
            data[i][j] = ('%.2f' % float(data[i][j]))
        for j in range(11, 14):
            data[i][j] = '%.1f' % float(data[i][j]) + "%"
    factor = [["年份", "球队", "出场数", "时间", "得分", "总篮板", "助攻", "抢断", "盖帽", "失误", "犯规", "命中率",
               "三分命中率", "罚球命中率", "位置", "球衣"]]
    data = factor + data

    sql_playerinfo = '''
                    select *
                    from player
                    where `姓名` like %s
                    ''' % playerInSQL
    cursor.execute(sql_playerinfo)
    playerinfo = cursor.fetchone()

    sql_advanced = '''
            select (`助攻` * 100.0) / (`两分出手数` * 1.0 + `三分出手数` * 1.0 + `罚球出手数` * 0.44 + `助攻` * 1.0 + `失误` * 1.0)
            from basic2019
            where `姓名` like %s
    ''' % (playerInSQL)

    cursor.execute(sql_advanced)
    advanced.append((cursor.fetchone()[0]))

    sql_advanced = '''
            select 助攻/失误
            from basic2019
            where `姓名` like %s
    ''' % (playerInSQL)

    cursor.execute(sql_advanced)
    advanced.append((cursor.fetchone()[0]))

    sql_advanced = '''
            select ((两分命中数*2+3*三分命中数+罚球命中数+进攻篮板+防守篮板+助攻+抢断-失误+盖帽)-((两分出手数+三分出手数-两分命中数-三分命中数)-(罚球出手数-罚球命中数)))/出场数
            from basic2019
            where `姓名` like %s
    ''' % (playerInSQL)

    cursor.execute(sql_advanced)
    advanced.append((cursor.fetchone()[0]))

    sql_advanced = '''
            select (两分命中数*2+3*三分命中数+罚球命中数+0.4*(两分命中数+三分命中数)-0.7*(两分出手数+三分出手数)-0.4*(罚球出手数-罚球命中数)+0.7*进攻篮板+0.3*防守篮板+0.7*助攻+抢断+0.7*盖帽-失误-0.4*犯规)/出场数
            from basic2019
            where `姓名` like %s
    ''' % (playerInSQL)

    cursor.execute(sql_advanced)
    advanced.append((cursor.fetchone()[0]))

    sql_advanced = '''
            select 失误*100/(两分出手数+三分出手数+罚球出手数*0.44+失误)
            from basic2019
            where `姓名` like %s
    ''' % (playerInSQL)

    cursor.execute(sql_advanced)
    advanced.append((cursor.fetchone()[0]))

    sql_advanced = '''
            select 罚球出手数*100/(两分出手数+三分出手数+罚球出手数+失误)
            from basic2019
            where `姓名` like %s
    ''' % (playerInSQL)

    cursor.execute(sql_advanced)
    advanced.append((cursor.fetchone()[0]))

    sql_advanced = '''
                select (`两分命中数` + 1.5 * `三分命中数`) / (`两分出手数` + `三分出手数`) * 100.0
                from basic2019
                where `姓名` like %s
        ''' % (playerInSQL)

    cursor.execute(sql_advanced)
    advanced.append((cursor.fetchone()[0]))

    sql_advanced = '''
                    select (两分命中数*2.0+3*三分命中数+罚球命中数) / (2.0 * (`两分出手数` + `三分出手数` + 0.44 * `罚球出手数`)) * 100.0
                    from basic2019
                    where `姓名` like %s
            ''' % (playerInSQL)

    cursor.execute(sql_advanced)
    advanced.append((cursor.fetchone()[0]))

    sql_advanced = '''
            
                        select (`助攻` + 0.0) / (A.`时间` / (C.`球队总时间`/ 5.0) * (B.`球队命中数` * 1.0) - A.`两分命中数` - A.`三分命中数` ) * 100.0 
                        from basic2019 A,`球队命中总数` B, TotalTime C
                        where A.`姓名` like %s and A.球队 = B.球队 AND B.`球队` = C.`球队`
                ''' % (playerInSQL)

    cursor.execute(sql_advanced)
    advanced.append((cursor.fetchone()[0]))

    sql_advanced = '''

                            select  (`两分出手数` + `三分出手数` + 0.44 * `罚球出手数` + `失误` + 0.0) * (C.`球队总时间`/ 5.0) / A.`时间`/ (B.`球队出手数` * 1.0 + 0.44 * B.`罚球` + B.`球队失误`) * 100.0
                            from basic2019 A,`球队命中总数3` B, TotalTime C
                            where A.`姓名` like %s and A.球队 = B.球队 AND B.`球队` = C.`球队`
                    ''' % (playerInSQL)

    cursor.execute(sql_advanced)
    advanced.append((cursor.fetchone()[0]))

    cursor.close()
    db.close()

    for i in range(len(advanced)):
        advanced[i] = "%.2f" % float(advanced[i])

    print(advanced)
    return render_template("player-details.html", name=Name, player=player0, playerinfo=playerinfo, data=data,
                           advanced=advanced)


@app.route('/operate', methods=['GET', 'POST'])
def team_Tackle():
    mydata = json.loads(request.form.get('data'))
    db = pymysql.connect(
        user='cba2020',
        passwd='cba2020',
        db='cba2020'

    )

    db.cursor()

    teamQuery = mydata['team']  # 为了接收传过来的是哪个球队
    teamQueryN = '"' + teamQuery + '"'

    sql_playerinTeam = '''
        select `姓名`
        from basic2019
        where `球队` = %s
    ''' % (teamQueryN)

    cursor = db.cursor()
    cursor.execute(sql_playerinTeam)

    playerinTeam = []
    ddata = cursor.fetchall()
    for item in ddata:
        playerinTeam.append(item)

    cursor.close()
    db.close()
    return jsonify({"team": playerinTeam})


@app.route('/TacklePlayer', methods=['GET', 'POST'])
def player_Tackle():
    # 我把另一个队员的数据都传到player-details 1747行的data['player']里了，当前页面球员的基本数据是你们定义的ccs,sj,df等数组里的最后一个，高阶数据在advanced1到advanced6的6个变量里面
    mydata = json.loads(request.form.get('data'))
    db = pymysql.connect(
        user='cba2020',
        passwd='cba2020',
        db='cba2020'

    )

    db.cursor()
    # print(mydata['player'])
    playerQuery = mydata['player']  # 为了接收传过来的是哪个球队
    playerQueryN = '"' + playerQuery + '"'
    sql_playerData = '''
            select 姓名,(两分命中数*2+3*三分命中数+罚球命中数)/出场数,(进攻篮板+防守篮板)/出场数,助攻/出场数,抢断/出场数,盖帽/出场数,失误/出场数,犯规/出场数,
            if(两分出手数+三分出手数<>0,(两分命中数+三分命中数)/(两分出手数+三分出手数)*100,0),
            if(三分出手数<>0,(三分命中数)/(三分出手数)*100,0),
            if(罚球出手数<>0,(罚球命中数)/(罚球出手数)*100,0),
            (`助攻` * 100.0) / (`两分出手数` * 1.0 + `三分出手数` * 1.0 + `罚球出手数` * 0.44 + `助攻` * 1.0 + `失误` * 1.0),
            助攻/失误,
            ((两分命中数*2+3*三分命中数+罚球命中数+进攻篮板+防守篮板+助攻+抢断-失误+盖帽)-((两分出手数+三分出手数-两分命中数-三分命中数)-(罚球出手数-罚球命中数)))/出场数,
            (两分命中数*2+3*三分命中数+罚球命中数+0.4*(两分命中数+三分命中数)-0.7*(两分出手数+三分出手数)-0.4*(罚球出手数-罚球命中数)+0.7*进攻篮板+0.3*防守篮板+0.7*助攻+抢断+0.7*盖帽-失误-0.4*犯规)/出场数,
            失误*100/(两分出手数+三分出手数+罚球出手数*0.44+失误),
            罚球出手数*100/(两分出手数+三分出手数+罚球出手数+失误),
            (`两分命中数` + 1.5 * `三分命中数`) / (`两分出手数` + `三分出手数`) * 100.0,
            (两分命中数*2.0+3*三分命中数+罚球命中数) / (2.0 * (`两分出手数` + `三分出手数` + 0.44 * `罚球出手数`)) * 100.0,
            助攻/(A.时间/(C.球队总时间/5.0)*(B.球队命中数)-A.两分命中数-A.三分命中数)*100.0,
            (`两分出手数` + `三分出手数` + 0.44 * `罚球出手数` + `失误` + 0.0) * (C.`球队总时间`/ 5.0) / A.`时间`/ (D.`球队出手数` * 1.0 + 0.44 * D.`罚球` + D.`球队失误`) * 100.0
            from basic2019 A, 球队命中总数 B, TotalTime C,`球队命中总数3` D
            where A.`姓名` = %s and A.球队=B.球队 and B.球队=C.球队 and A.球队=D.球队 and D.球队=C.球队
        ''' % (playerQueryN)

    cursor = db.cursor()
    cursor.execute(sql_playerData)

    playerCompared = []
    ddata = cursor.fetchall()
    for item in ddata:
        for iitem in range(len(item)):
            try:
                playerCompared.append(float(item[iitem]))
            except ValueError:
                playerCompared.append(str(item[iitem]))
            except BaseException as e:
                print(e)
    print(playerCompared)
    cursor.close()
    db.close()

    for i in range(1, len(playerCompared)):
        playerCompared[i] = "%.2f" % float(playerCompared[i])

    # 返回数据
    return jsonify({"player": playerCompared})


if __name__ == '__main__':
    app.run(debug=True)
