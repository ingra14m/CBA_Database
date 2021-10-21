import pymysql

# db = pymysql.connect("sh-cdb-1xzdh3ty.sql.tencentcdb.com", "root", "Asdf0506@", "CBA_Final")

db = pymysql.connect(
    host='sh-cdb-1xzdh3ty.sql.tencentcdb.com',
    port=60557,
    user='root',
    passwd='Asdf0506@',
    db='CBA_Final'

)

sql = '''
        select *
        from basic2019;
    '''

cursor = db.cursor()
cursor.execute(sql)
db.commit()

cursor.close()
db.close()