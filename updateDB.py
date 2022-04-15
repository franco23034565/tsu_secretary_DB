# Written by Franco 2022/04/14


from unittest import result


def addUser(NID, UserName, UserPassword, Dept, Grade):
    return f"insert into Users values(\'{NID}\', \'{UserName}\', \'{UserPassword}\', \'{Dept}\', {Grade});"

def MustHaveList(NID):
    return f"select CourseID from AllCourse where MustHave = true and Dept in (select Dept from Users where NID = {NID});"

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
    return f"insert into Chosen values(\'{NID}\', {CourseID});"

#not include "detect if the course is in NID's Chosen list"
def deleteCourse(NID, CourseID):
    return f"delete from Chosen where CourseID = {CourseID} and NID = \'{NID}\';"

#null table donotes that don't exist same CourseName
def isSameNameCourse(CourseName):
    return f"SELECT CourseName FROM AllCourse WHERE CourseName = {CourseName};"

#null table donotes that don't exceed limit of student
def isExceedLimitOfStudent(CourseID):
    return f"SELECT HowManyPeople FROM AllCourse WHERE CourseID = {CourseID} and HowManyPeople >= PeopleLimit;"

#lists all CourseName, CourseID, Point that don't exceed limit of Point
def ListChosenCourse(NID):
    #source: python_example.py
    cursor.execute(f"SELECT sum(Point) FROM AllCourse WHERE CourseID in (SELECT COURSEID FROM Chosen WHERE NID = {NID});")
    currentToatalPointsOfStudent = cursor.fetchall()
    cursor.execute(f"SELECT CourseName, CourseID, Point FROM AllCourse WHERE CourseID NOT IN (SELECT CourseID FROM Chosen);")
    notChosenList = cursor.fetchall()
    for (CourseName, CourseID, Point) in notChosenList:
        sum = currentToatalPointsOfStudent + Point
        if 9 <= sum and sum <= 30:
            results = (CourseName, CourseID, Point)
    return results

def isHigherPointLimit(NID):
    results = f"SELECT sum(Point) FROM AllCourse WHERE CourseID in (SELECT COURSEID FROM Chosen WHERE NID = {NID});"
    #source: python_example.py
    cursor.execute(results)
    if 30 < cursor.fetchall():
        return True
    return False

def isLowerPointLimit(NID):
    results = f"SELECT sum(Point) FROM AllCourse WHERE CourseID in (SELECT COURSEID FROM Chosen WHERE NID = {NID});"
    #source: python_example.py
        cursor.execute(results)
        if cursor.fetchall() < 30:
            return True
        return False

def isMustHaveCourse(CourseID):
    results =  f"SELECT MustHave FROM AllCourse WHERE CourseID = {CourseID}"
    #source: python_example.py
    cursor.execute(results)
    if cursor.fetchall() == True:
        return True
    return False

#Test
NID = 'D0915679'
CourseID = 9527
print(MustHaveList(NID))