#!/usr/bin/env python3
# coding=utf-8
# -*- coding: UTF-8 -*-
from flask import Flask, request
import MySQLdb

app = Flask(__name__)
'''
    form = """
    <form method="post" action="/action" >
        文字輸出欄位：<input name="my_head">
        <input type="submit" value="送出">
    </form>
    <button >
    """
'''

@app.route('/')
def index():
    form = """
    <form method="post" action="/printAllCourse" >
        <button type="submit" name="AllCourse" value="*">Click Me</button>
    </form>
    <form method="post" action="/action2">
        <button type="submit" name="AllCourse" value="CourseID, CourseName">Click Me 2</button>
    </form>
    """
    return form


@app.route('/printAllCourse', methods=['POST'])
def printAllCourse():
    # 取得輸入的文字
    my_head = request.form.get("AllCourse")
    # 建立資料庫連線
    conn = MySQLdb.connect(host="127.0.0.1",
                           user="hj",
                           passwd="test1234",
                           db="testdb")
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
    results += "<th>課程ID</th> <th>課程名稱</th> <th>科系</th> <th>人數</th> <th>學分</th> <th>教授</th> <th>年級</th> <th>必修</th>"
    results += "</tr>"
    for (CourseID,CourseName,Dept,HowManyPeople, PeopleLimit,Points,Teacher,Grade,MustHav) in cursor.fetchall():
        results += "<tr>"
        results += "<td>{}</td> <td>{}</td> <td>{}</td> <td>{}/{}</td> <td>{}</td> <td>{}</td> <td>{}</td> <td>{}</td>".format(CourseID,CourseName,Dept,HowManyPeople,PeopleLimit,Points,Teacher,Grade,MustHav)
        results += "</tr>"
    results += "</table>"
    return results

@app.route('/action2', methods=['POST'])
def action2():
    # 取得輸入的文字
    my_head = request.form.get("AllCourse")
    #your_head = request.form.get("CourseName")
    # 建立資料庫連線
    conn = MySQLdb.connect(host="127.0.0.1",
                           user="hj",
                           passwd="test1234",
                           db="testdb")
    # 欲查詢的 query 指令
    query1 = "SELECT {} FROM AllCourse;".format(my_head)
    #query2 = "SELECT {} FROM AllCourse;".format(your_head)
    # 執行查詢
    cursor = conn.cursor()
    cursor.execute(query1)

    results = """
    <p><a href="/">Back to Query Interface</a></p>
    """
    # 取得並列出所有查詢結果
    #CourseID,CourseName,Dept,PeopleLimit,Points,Teacher,Grade,MustHave

    for (CourseID,CourseName) in cursor.fetchall():
        results += "<p>{}, {}</p>".format(CourseID,CourseName)
    return results