
from unittest import result
from hashlib import sha256
import MySQLdb

def tsuSHA256(aString):
    return str(sha256(aString.encode("utf-8")).hexdigest())

def addUser(NID, UserName, UserPassword, Dept, Grade):
    passwd = tsuSHA256(UserPassword)
    return f"insert into Users values(\'{NID}\', \'{UserName}\', \'{passwd}\', \'{Dept}\', {Grade});"

def MustHaveList(NID):
    return f"select CourseID from AllCourse where MustHave = true and Dept in (select Dept from Users where NID = \'{NID}\');"

def isMustHaveCourse(Dept,CourseID):
    results =  f"SELECT MustHave, Dept FROM AllCourse WHERE CourseID = {CourseID}"
    cursor.execute(results)
    tempA = cursor.fetchall() 
    
    #source: python_example.py
    if (tempA[0] == True) and (tempA[1] == Dept) :
        return True
    return False

#if theres thing in this table, then theres time collision
def timeCollision(NID, CourseID):
    result =  f"SELECT TimeID from CourseTime WHERE CourseID IN (SELECT CourseID FROM Chosen WHERE NID = \'{NID}\')"
    result += f" and "
    result += f"TimeID IN (SELECT TimeID FROM CourseTime WHERE CourseID = {CourseID});"
    return result

#not include time collision 未完成
def chooseCourse(NID, CourseID):
    '''
    timeTable = timeCollision(NID, CourseID)
    currentTimeOfCourse = f"SELECT TimeID FROM CourseTime WHERE CourseID = {CourseID}"
    result = f"IF (NOT EXISTS(SELECT TimeID FROM {currentTimeOfCourse} INNER JOIN {timeTable} ON {currentTimeOfCourse}.TimeID = {timeTable}.TimeID))"
    if 
    '''
    results = f"update AllCourse set HowManyPeople = HowManyPeople + 1 where CourseID = {CourseID};"
    results += f"insert into Chosen values(\'{NID}\', {CourseID});"
    return results

#not include "detect if the course is in NID's Chosen list"
def deleteCourse(NID, CourseID):
    return f"delete from Chosen where CourseID = {CourseID} and NID = \'{NID}\';"

def SameNameCourseCount(NID, CourseID):
    results  = f"select count(*) as CourseCount from AllCourse"
    results += f"where CourseName in (select CourseName from AllCourse where CourseID in (select CourseID from Chosen where NID = \'{NID}\'))" #在已選課表中的所有課名
    results += f" and "
    results += f"CourseID <> {CourseID};"
    return results

def isExceedLimitOfStudent(CourseID):
    results = f"SELECT HowManyPeople,PeopleLimit FROM AllCourse WHERE CourseID = {CourseID};"
    cursor.execute(results)
    tempA = cursor.fetchall()
    return tempA[0]>tempA[1]#true or false

#lists all CourseName, CourseID, Point that don't exceed limit of Point
def ListChosenCourse(NID):
    #source: python_example.py
    cursor.execute(f"SELECT sum(Point) FROM AllCourse WHERE CourseID in (SELECT COURSEID FROM Chosen WHERE NID = \'{NID}\');")
    currentToatalPointsOfStudent = cursor.fetchall()
    cursor.execute(f"SELECT CourseName, CourseID, Point FROM AllCourse WHERE CourseID NOT IN (SELECT CourseID FROM Chosen);")
    notChosenList = cursor.fetchall()
    for (CourseName, CourseID, Point) in notChosenList:
        sum = currentToatalPointsOfStudent + Point
        if 9 <= sum and sum <= 30:
            results = (CourseName, CourseID, Point)
    return results

def isLessThanPointUpperLimit(NID):
    results = f"SELECT sum(Points) FROM AllCourse WHERE CourseID in (SELECT CourseID FROM Chosen WHERE NID = \'{NID}\');"
    #source: python_example.py
    cursor.execute(results)
    if cursor.fetchall() <= 30:
        return True
    return False

def isGreaterThanPointLowerLimit(NID):
    results = f"SELECT sum(Points) FROM AllCourse WHERE CourseID in (SELECT CourseID FROM Chosen WHERE NID = \'{NID}\');"
    #source: python_example.py
    cursor.execute(results)
    if cursor.fetchall() >= 9:
        return True
    return False

def isMustHaveCourse(CourseID):
    results =  f"SELECT MustHave FROM AllCourse WHERE CourseID = {CourseID}"
    #source: python_example.py
    cursor.execute(results)
    if cursor.fetchall() == True:
        return True
    return False

def currentPoint(NID):
    return f"select sum(Points) as CurrentPoint from AllCourse where CourseID in (select CourseID from Chosen where NID = \'{NID}\');"


#return [星期幾(string), 第幾節課(int)]
def TimeIDToTime(TimeID):
    weekRef = {1 :"一", 2: "二", 3: "三", 4: "四",
               5: "五", 6: "六", 7: "日"}
    week = (int)(TimeID/100)
    #print(week)
    theClass = TimeID % 100
    return [weekRef[week], theClass]


#Test
NID = 'D0915679'
passwd = str(input('Input Password: '))
UserName = "紀彥廷"
Dept = "資工"
Grade = 2
print(addUser(NID, UserName, passwd, Dept, Grade))

