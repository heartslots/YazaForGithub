import pymysql
from datetime import datetime

now = datetime.now()

todaydate = "a"+str(now.year) + str(now.month) + str(now.day)

DB_NAME = "YOUR_DATABASE"
TABLE_NAME = "YOUR_TABLE"

db = pymysql.connect(
    host="YOUR_HOST",
    user="YOUR_USER",
    password="YOUR_PASSWORD",
    database="YOUR_DATABASE"
)

cursor = db.cursor()

def alter(id): #id가 입력됬을때 상태 변경
    sql = "SELECT isUsing FROM "+TABLE_NAME+" WHERE id = " + str(id)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result[0][0])
    if (result[0][0] == 0):
        change = "UPDATE "+TABLE_NAME+" SET isUsing = 1 WHERE id = " + str(id)
        cursor.execute(change)
    elif (result[0][0] == 1):
        change = "UPDATE "+TABLE_NAME+" SET isUSing = 0 WHERE id = " + str(id)
        cursor.execute(change)
        timestamp(id)
    db.commit()

def search(column_name): #컬럼 검색
    sql = "SELECT 1 FROM Information_schema.columns WHERE table_schema = '"+DB_NAME+"' AND table_name = '"+TABLE_NAME+"' AND column_name = '"+str(column_name)+"'"
    cursor.execute(sql)
    result = cursor.fetchall()
    if not result:
        add_column(column_name)

def add_column(column_name): #컬럼이 존재하지 않을 시 해당 이름으로 컬럼 추가
    sql = "ALTER TABLE "+TABLE_NAME+" ADD "+str(column_name)+" INT"
    cursor.execute(sql)
    db.commit()
    print("완료")

def timestamp(id): #종료시간 체크
    if now.minute < 10:
        NOW_TIME = int(str(now.hour)+"0"+str(now.minute))        
    else:
        NOW_TIME = int(str(now.hour)+str(now.minute))
    print(NOW_TIME)
    
    sql = "UPDATE "+TABLE_NAME+" SET "+todaydate+" = "+str(NOW_TIME)+" WHERE id = "+ str(id)
    cursor.execute(sql)
    db.commit()

def main(id):
    search(todaydate)
    alter(id)
