# Written by Franco 2022/04/14


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

#not include time collision
def chooseCourse(NID, CourseID):
    return f"insert into Chosen values(\'{NID}\', {CourseID});"

#not include "detect if the course is in NID's Chosen list"
def deleteCourse(NID, CourseID):
    return f"delete from Chosen where CourseID = {CourseID} and NID = \'{NID}\';"

def currentPoint(NID):
    return f"select sum(Points) as CurrentPoint from AllCourse where CourseID in (select CourseID from Chosen where NID = {NID});"