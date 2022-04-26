#!/usr/bin/env python3
# coding=utf-8
# -*- coding: UTF-8 -*-
from unittest import result
from flask import Flask, request
import MySQLdb
import updateDB as DB
conn = MySQLdb.connect(host="127.0.0.1",
                           user="hj",
                           passwd="test1234",
                           db="testdb")
cursor = conn.cursor()

def studentIDToName(NID,conn):
    cursor = conn.cursor()
    cursor.execute(f"select UserName from Users where NID = \'{NID}\';")
    studentName = ""
    for (a,) in cursor.fetchall():
        studentName = a
    return studentName

app = Flask(__name__)
'''
    form = """
    <form method="post" action="/action" >
        文字輸出欄位：<input name="my_head">
        <input type="submit" value="送出">
    </form>
    <button >
    
    <form method="post" action="/action2">
        <button type="submit" name="AllCourse" value="CourseID, CourseName">Click Me 2</button>
        登入帳號：<input type="text" name="user">
        密碼：<input type="password" name="passwd">
        <input type="submit" name="submit" value="送出">
    </form>
    """
'''
#<form method="post" action="/printOwnCourse">
 #       <p>登入帳號：<p><input type="text" name="user">
  #      <p>密碼：<p><input type="password" name="passwd">
   #     <p><button type="submit" value="*">送出</button>
    #</from>
#
 #   <form method="post" action="/index2" >
  #      <button type="submit" value="*">新增使用者</button>
   # </form>


@app.route('/')

def index():

    form = f"""
    <form method="post" action="/index2">
        <button type="submit" value="*">新增使用者</button>
    </form>
    <form method="post" action="/printAllCourse" >
        <button type="submit" name="AllCourse" value="*">顯示所有課程</button>
    </form>
    <form method="post" action="/printOwnCourse">
        <p>登入帳號：</p><input type="text" name="user">
        <p>密碼：</p><input type="password" name="passwd">
        <p><button type="submit" value="*">送出</button>
    </from>
    """
    return form

@app.route('/printOwnCourse', methods=['POST'])
def printOwnCourse():
    truth = {0:"否", 1:"是"}
    username = request.form.get("user")
    passwd = request.form.get("passwd")
    if username == "" or passwd == "":
        results = "<h1>帳號密碼不能為空</h1>"
        results += """<p><a href="/">Back to Query Interface</a></p>"""
        return results
    elif (DB.isUser(username, passwd, conn)== False):
        results = "<h1>帳號或密碼錯誤</h1>"
        results += """<p><a href="/">Back to Query Interface</a></p>"""
        results += """ <form method="post" action="/index2" >
                            <button type="submit" value="*">新增使用者</button>
                        </form>
                    """
        return results
    else:
        global StudentID
        StudentID = username
        studentName = studentIDToName(username, conn)
        cursor.execute(DB.listChosenList(StudentID))
        results = """
    <style>
        table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        }
        td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
        }
        tr:nth-child(even) {
        background-color: #dddddd;
        }
    </style>
    <p><a href="/">Back to Query Interface</a></p>
    """
    results +=  f"<h1>Welcome, {studentName} </h1>"
    results +=  f"""<form method="post" action="/AddCourse" >
                        <button type="submit" name="courseID" value="0">去選課!</button>
                    </form>"""
                
    results += f"<h2>已選課表</h2>"
    results += "<table>"
    # 取得並列出所有查詢結果
    #CourseID,CourseName,Dept,PeopleLimit,Points,Teacher,Grade,MustHave
    results += "<tr>"
    results += "<th>課程ID</th> <th>課程名稱</th> <th>科系</th> <th>人數</th> <th>學分</th> <th>教授</th> <th>年級</th> <th>必修</th>"
    results += "</tr>"
    for (CourseID,CourseName,Dept,HowManyPeople, PeopleLimit,Points,Teacher,Grade,MustHav) in cursor.fetchall():
        results += "<tr>"
        results += "<td>{}</td> <td>{}</td> <td>{}</td> <td>{}/{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td>".format(CourseID,CourseName,Dept,HowManyPeople,PeopleLimit,Points,Teacher,Grade,truth[MustHav])
        results += "</tr>"
    results += "</table>"
    return results




@app.route('/printAllCourse', methods=['POST'])
def printAllCourse():
    truth = {0:"否", 1:"是"}
    # 取得輸入的文字
    my_head = request.form.get("AllCourse")
    # 建立資料庫連線
    
    # 欲查詢的 query 指令
    #query1 = "SELECT * FROM AllCourse;"
    query1 = "SELECT {} FROM AllCourse;".format(my_head)
    # 執行查詢
    cursor = conn.cursor()
    cursor.execute(query1)

    results = """
    <style>
        table {
        font-family: arial, sans-serif;
        border-collapse: collapse;
        width: 100%;
        }
        td, th {
        border: 1px solid #dddddd;
        text-align: left;
        padding: 8px;
        }
        tr:nth-child(even) {
        background-color: #dddddd;
        }
    </style>
    <p><a href="/">Back to Query Interface</a></p>
    """
    results += "<table>"
    # 取得並列出所有查詢結果
    #CourseID,CourseName,Dept,PeopleLimit,Points,Teacher,Grade,MustHave
    results += "<tr>"
    results += "<th>課程ID</th> <th>課程名稱</th> <th>科系</th> <th>人數</th> <th>學分</th> <th>教授</th> <th>年級</th> <th>必修</th> <th>時間地點</th>"
    results += "</tr>"
    for (CourseID,CourseName,Dept,HowManyPeople, PeopleLimit,Points,Teacher,Grade,MustHav) in cursor.fetchall():
        results += "<tr>"
        results += "<td>{}</td> <td>{}</td> <td>{}</td> <td>{}/{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td>".format(CourseID,CourseName,Dept,HowManyPeople,PeopleLimit,Points,Teacher,Grade,truth[MustHav], DB.courseTimeString(CourseID,conn))
        results += "</tr>"
    results += "</table>"
    results += "<h1>Welcome</h1>"
    return results

@app.route('/index2', methods=['POST'])
def index2():
    form = """
    <form method="post" action="/AddUsers">
        <p>帳號：<p><input type="text" name="user">
        <p>密碼：<p><input type="password" name="passwd">
        <p>你的資料:
        <p>名字<input type="text" name="name">
        <p>系所<input type="text" name="dept">
        <p>年級<input type="text" name="grade">
        <p><button type="submit" value="*">送出</button>
    </from>
    """
    return form 

@app.route('/AddUsers', methods=['POST'])
def AddUsers():
    NID = request.form.get("user")
    UserPassword = request.form.get("passwd")
    UserName = request.form.get("name")
    Dept = request.form.get("dept")
    Grade = request.form.get("grade")
    DB.addUser(NID, UserName, UserPassword, Dept, Grade, conn)
    DB.autoChooseMustHaveList(NID,conn)
    results = "<h1>新增成功，已將必選課程列入課表</h1>"
    results += """<p><a href="/">Back to Query Interface</a></p>"""
    return results

@app.route('/AddCourse',methods=['POST'])
def AddCourse():
    truth = {0:"否", 1:"是"}

    CourseID = request.form.get("courseID")
    if not(CourseID=="0"):
        DB.addInWishList(StudentID,CourseID,conn)

    cursor.execute(DB.showWishList(StudentID))
    results = """
        <style>
            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            tr:nth-child(even) {
                background-color: #dddddd;
            }
        </style>
        <p><a href="/">Back to Query Interface</a></p>"""
    results +=  f"<h1>Welcome, {studentIDToName(StudentID, conn)} </h1>"
    results +=   f"""<form method="post" action="" >
                        課程ID:<p><input type="text" name="courseID">
                        <button type="submit" >加入願望清單</button>
                    </form>
                """
    results += f"<h2>願望清單</h>"
    results += "<table>"
    # 取得並列出所有查詢結果
    #CourseID,CourseName,Dept,PeopleLimit,Points,Teacher,Grade,MustHave
    results += "<tr>"
    results += "<th>課程ID</th> <th>課程名稱</th> <th>科系</th> <th>人數</th> <th>學分</th> <th>教授</th> <th>年級</th> <th>必修</th>"
    results += "</tr>"
    for (CourseID,CourseName,Dept,HowManyPeople, PeopleLimit,Points,Teacher,Grade,MustHav) in cursor.fetchall():
        results += "<tr>"
        results += "<td>{}</td> <td>{}</td> <td>{}</td> <td>{}/{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td>".format(CourseID,CourseName,Dept,HowManyPeople,PeopleLimit,Points,Teacher,Grade,truth[MustHav])
        results += "</tr>"
    results += "</table>"
    return results

@app.route('/index3', methods=['POST'])
def index3():
    CourseID=request.form.get("courseID")
    DB.addInWishList(StudentID,CourseID,conn)
    results = """
        <style>
            table {
                font-family: arial, sans-serif;
                border-collapse: collapse;
                width: 100%;
            }
            td, th {
                border: 1px solid #dddddd;
                text-align: left;
                padding: 8px;
            }
            tr:nth-child(even) {
                background-color: #dddddd;
            }
        </style>
        <p><a href="/">Back to Query Interface</a></p>"""
    return results