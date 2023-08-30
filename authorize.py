import tkinter as tk
import pymysql
from datetime import datetime

window = tk.Tk()

now = datetime.now()

todaydate = "a"+str(now.year) + str(now.month) + str(now.day)

DB_NAME = "YOUR_DB"
TABLE_NAME = "YOUR_TABLE"

db = pymysql.connect(
    host="YOUR_HOST",
    user="YOUR_USER",
    password="YOUR_PASSWORD",
    database="YOUR_DB"
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
        RESULT_LABEL['text']="입실"
    elif (result[0][0] == 1):
        change = "UPDATE "+TABLE_NAME+" SET isUSing = 0 WHERE id = " + str(id)
        cursor.execute(change)
        timestamp(id)
        RESULT_LABEL['text']="퇴실"
    RESULT_LABEL.pack()
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

def check_student_quantity(): #인원 수 체크
    sql = "SELECT id FROM "+TABLE_NAME+" WHERE isUsing = 1"
    cursor.execute(sql)
    result = cursor.fetchall()
    if not result:
        return 0
    else:
        return len(result)

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
    if id.isdecimal():
        search(todaydate)
        alter(id)
        OCCUPY['text'] = str(check_student_quantity())+"명이 야자중입니다."
        OCCUPY.pack()
    else:
        RESULT_LABEL['text'] = "잘못된 요청입니다."
        RESULT_LABEL.pack()

def input_wizard(self):
    main(ID_INPUT.get())
    ID_INPUT.delete(0, "end")

window.title("야자관리 프로그램")

window.geometry("500x500+500+150")

#제목

GUI_TITLE = tk.Label(window, text="야자관리 프로그램 ver 1.0")
GUI_TITLE.pack()

ID_INPUT = tk.Entry(window)
ID_INPUT.bind("<Return>", input_wizard)
ID_INPUT.pack()

OCCUPY = tk.Label(window, text=str(check_student_quantity())+"명이 야자중입니다.")
OCCUPY.pack()

RESULT_LABEL = tk.Label(window)

window.mainloop()
