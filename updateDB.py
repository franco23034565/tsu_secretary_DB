from hashlib import sha256
import MySQLdb

def tsuSHA256(aString):
    return str(sha256(aString.encode("utf-8")).hexdigest())

def haveSameNID(NID, conn):
    cursor = conn.cursor()
    cursor.execute(f"select count(*) from Users where NID = \'{NID}\';")
    results = 0
    for (a,) in cursor.fetchall():
        results = a
    if (results == 1):
        return True
    return False

# tested: ABLE TO USE
#add user with password using SHA256 hash function
def addUser(NID, UserName, UserPassword, Dept, Grade, conn):
    if (haveSameNID(NID, conn)):
        return False
    cursor = conn.cursor()
    passwd = tsuSHA256(UserPassword)
    results = f"insert into Users values(\'{NID}\', \'{UserName}\', \'{passwd}\', \'{Dept}\', {Grade});"
    cursor.execute(results)
    conn.commit()
    return True

# tested: ABLE TO USE
def listChosenListID(NID):
    results = f"select CourseID from AllCourse where CourseID in (select CourseID from Chosen where NID = \'{NID}\');"
    return results


def pyChosenList(NID, conn):
    cursor = conn.cursor()
    cursor.execute(listChosenListID(NID))
    finalList = []
    for (a,) in cursor.fetchall():
        finalList.append(a)
    return finalList

# tested: ABLE TO USE
def showWishListID(NID):
    return f"select CourseID from AllCourse where CourseID in (select CourseID from WishList where NID = \'{NID}\');"

def pyWishList(NID, conn):
    cursor = conn.cursor()
    cursor.execute(showWishListID(NID))
    finalList = []
    for (a,) in cursor.fetchall():
        finalList.append(a)
    return finalList

# tested: ABLE TO USE
#list all Courses that a user must have
def mustHaveList(NID):
    return f"select CourseID from AllCourse where MustHave = true and Dept in (select Dept from Users where NID = \'{NID}\');"

# tested: ABLE TO USE
#automate the "choose MustHave" process
def autoChooseMustHaveList(NID, conn):
    cursor = conn.cursor()
    cursor.execute(mustHaveList(NID))
    for (CourseID,) in cursor.fetchall():
        addAllCoursePeople = f"update AllCourse set HowManyPeople = HowManyPeople + 1 where CourseID = {CourseID};"
        addChosen = f"insert into Chosen values(\'{NID}\', {CourseID});"
        #print(addAllCoursePeople)
        #print(addChosen)
        cursor.execute(addAllCoursePeople)
        conn.commit()
        cursor.execute(addChosen)
        conn.commit()
  
def isMustHaveCourse(Dept,CourseID, cursor):
    results =  f"SELECT MustHave, Dept FROM AllCourse WHERE CourseID = {CourseID};"
    cursor.execute(results)
    tempA = cursor.fetchall()
    
    #source: python_example.py
    if (tempA[0] == True) and (tempA[1] == Dept) :
        return True
    return False


#tested: ABLE TO USE
def timeCollision(NID,conn):
    cursor = conn.cursor()
    exxe = f"""select count(*) from CourseTime where TimeID in (select TimeID from CourseTime where CourseID in (select CourseID from Chosen where NID = '{NID}')) and
TimeID in (select TimeID from CourseTime where CourseID in (SELECT CourseID FROM WishList WHERE NID = '{NID}'));"""
    cursor.execute(exxe)
    results = 0
    for (a,) in cursor.fetchall():
        results = a
    if (results == 0):
        return False
    return True
    
'''

#not include time collision 未完成
def chooseCourse(NID, CourseID):
    
    timeTable = timeCollision(NID, CourseID)
    currentTimeOfCourse = f"SELECT TimeID FROM CourseTime WHERE CourseID = {CourseID}"
    result = f"IF (NOT EXISTS(SELECT TimeID FROM {currentTimeOfCourse} INNER JOIN {timeTable} ON {currentTimeOfCourse}.TimeID = {timeTable}.TimeID))"
    if 
    
    results = f"update AllCourse set HowManyPeople = HowManyPeople + 1 where CourseID = {CourseID};"
    results += f"insert into Chosen values(\'{NID}\', {CourseID});"
    return results
'''
# tested: ABLE TO USE
# 調用此函式需把回傳值results放入html裡呈現結果
def deleteCourse(NID, CourseID, conn):
    results = ""
    cursor = conn.cursor()
    cursor.excute(f"SELECT Points FROM AllCourse WHERE CourseID = {CourseID}")
    pointOfCourse = cursor.fetchone()
    pointOfresult = currentPoint(NID, conn) - pointOfCourse[0];
    if pointOfresult < 9:
        results += """  <script>
                            function(){
                                alert("\"不能退選\", 退選當前課程會低於學分下限!!")
                            }
                        </script>
                    """
        return results
    if isMustHaveCourse(CourseID) == True:
        results += """  <script>
                            function alert(){
                                alert("你已退選您的\"必選課程\"!!")
                            }
                        </script>
                   """
    results1 =  f"delete from Chosen where CourseID = {CourseID} and NID = \'{NID}\';\n"
    cursor.execute(results1)
    conn.commit()
    results2 = f"update AllCourse set HowManyPeople = HowManyPeople - 1 where CourseID = {CourseID};"
    cursor.execute(results2)
    conn.commit()
    return results

def SameNameCourseCount(NID, CourseID):
    results  = f"select count(*) as CourseCount from AllCourse"
    results += f"where CourseName in (select CourseName from AllCourse where CourseID in (select CourseID from Chosen where NID = \'{NID}\'))" #在已選課表中的所有課名
    results += f" and "
    results += f"CourseID <> {CourseID};"
    return results

def isCourse(CourseID, conn):
    cursor = conn.cursor()
    cursor.execute(f"select count(*) from AllCourse where CourseID = {CourseID};")
    results = 0
    for (a,) in cursor.fetchall():
        results = a
    if (results == 1):
        return True
    return False

def addInWishList(NID, CourseID, conn):
    cursor = conn.cursor()
    if (isCourse(CourseID, conn) == False):
        return False
    if CourseID in pyChosenList(NID, conn) or CourseID in pyWishList(NID, conn):
        return False
    results = f"insert into WishList values(\'{NID}\', {CourseID});"
    cursor.execute(results)
    conn.commit()
    return True

def isExceedLimitOfStudent(CourseID, cursor):
    results = f"SELECT HowManyPeople,PeopleLimit FROM AllCourse WHERE CourseID = {CourseID};"
    cursor.execute(results)
    tempA = cursor.fetchall()
    #return tempA
    return tempA[0][0]>=tempA[0][1]#true or false

#lists all CourseName, CourseID, Point that don't exceed limit of Point
#results is tuple list
def ListChoosableCourse(NID, cursor):
    #source: python_example.py
    cursor.execute(f"SELECT sum(Points) FROM AllCourse WHERE CourseID in (SELECT CourseID FROM Chosen WHERE NID = \'{NID}\');")
    currentTotalPointsOfStudent = cursor.fetchall()
    cursor.execute(f"SELECT CourseName, CourseID, Point FROM AllCourse WHERE CourseID NOT IN (SELECT CourseID FROM Chosen where NID = \'{NID}\');")
    notChosenList = cursor.fetchall()
    results = []
    for (CourseName, CourseID, Point) in notChosenList:
        sum = currentTotalPointsOfStudent + Point
        if 9 <= sum and sum <= 30:
            results.append((CourseName, CourseID, Point)) 
    return results


def isLessThanPointUpperLimit(NID, cursor):
    results = f"SELECT sum(Points) FROM AllCourse WHERE CourseID in (SELECT CourseID FROM Chosen WHERE NID = \'{NID}\');"
    #source: python_example.py
    cursor.execute(results)
    temp = cursor.fetchone()
    if temp[0] <= 30:
        return True
    return False


def isGreaterThanPointLowerLimit(NID, cursor):
    results = f"SELECT sum(Points) FROM AllCourse WHERE CourseID in (SELECT CourseID FROM Chosen WHERE NID = \'{NID}\');"
    #source: python_example.py
    cursor.execute(results)
    temp = cursor.fetchone()
    if temp[0] >= 9:
        return True
    return False

def isMustHaveCourse(CourseID, cursor):
    results =  f"SELECT MustHave FROM AllCourse WHERE CourseID = {CourseID}"
    #source: python_example.py
    cursor.execute(results)
    temp = cursor.fetchall()
    if temp[0] == True:
        return True
    return False

# tested: ABLE TO USE
# if current point = 0, then return None
def currentPoint(NID, conn):
    cursor = conn.cursor()   
    results = f"select sum(Points) as CurrentPoint from AllCourse where CourseID in (select CourseID from Chosen where NID = \'{NID}\');"
    cursor.execute(results)
    CurrentPoints = 0
    for (a,) in cursor.fetchall():
        CurrentPoints = a
    return CurrentPoints

#return [星期幾(string), 第幾節課(int)]
def TimeIDToTime(TimeID):
    weekRef = {1 :"一", 2: "二", 3: "三", 4: "四",
               5: "五", 6: "六", 7: "日"}
    week = (int)(TimeID/100)
    #print(week)
    theClass = TimeID % 100
    return [weekRef[week], theClass]

# tested: ABLE TO USE
def isUser(NID, passwd, conn):
    cursor = conn.cursor()
    userPassWd = tsuSHA256(passwd)
    searchsql = f"select count(*) from Users where NID = \'{NID}\' and UserPassword = \'{userPassWd}\';"
    cursor.execute(searchsql)
    results = 0
    for (amount,) in cursor.fetchall():
        results += amount
    if results == 1:
        return True
    return False

# tested: ABLE TO USE
def listChosenList(NID):
    results = f"select * from AllCourse where CourseID in (select CourseID from Chosen where NID = \'{NID}\');"
    return results

# tested: ABLE TO USE
def wishListPoint(NID, conn):
    cursor = conn.cursor()   
    results = f"select sum(Points) as CurrentPoint from AllCourse where CourseID in (select CourseID from WishList where NID = \'{NID}\');"
    cursor.execute(results)
    CurrentPoints = 0
    for (a,) in cursor.fetchall():
        CurrentPoints = a
    return CurrentPoints

# tested: ABLE TO USE
def wishListPointAddChosenPoint(NID, conn):
    return currentPoint(NID, conn) + wishListPoint(NID, conn)

# tested: ABLE TO USE
def showWishList(NID):
    return f"select * from AllCourse where CourseID in (select CourseID from WishList where NID = \'{NID}\');"


# tested: ABLE TO USE

def chooseCourse(NID,conn):
    if (timeCollision(NID, conn) == True):
        return "衝堂"     #衝堂
    
    if (wishListPointAddChosenPoint(NID, conn) > 30):
        return "超出學分上限"     #超出上限
    
    wishList = f"select CourseID from WishList where NID = \'{NID}\';"
    cursor = conn.cursor()
    cursor.execute(wishList)
    results = "成功!"
    for (CourseID,) in cursor.fetchall():
        if (isExceedLimitOfStudent(CourseID, cursor) == True):
            #print(f"{CourseID} Exceed People Limit\n")
            results += f", 超出人數上限：{CourseID}"
            continue
        cursor.execute(f"insert into Chosen values(\'{NID}\', {CourseID});")
        conn.commit()
        cursor.execute(f"update AllCourse set HowManyPeople = HowManyPeople + 1 where CourseID = {CourseID};")
        conn.commit()
        cursor.execute(f"delete from WishList where CourseID = {CourseID} and NID = \'{NID}\';")
        conn.commit()
    return results


#True when success
def deleteFromWishList(NID, CourseID, conn):

    inWishList = f"select count(*) from WishList where CourseID = {CourseID} and NID = \'{NID}\';"
    cursor = conn.cursor()
    cursor.execute(inWishList)
    wishCount = 0
    for (a,) in cursor.fetchall():
        wishCount = a
    if (wishCount != 1):
        return False
    cursor.execute(f"delete from WishList where CourseID = {CourseID} and NID = \'{NID}\';")
    conn.commit()
    return True

#（星期幾）第？節，在哪裡\n
def courseTimeString(CourseID, conn):
    cursor = conn.cursor()
    allResults = f"select TimeID, Classroom from CourseTime where CourseID = {CourseID};"
    cursor.execute(allResults)
    #return cursor.fetchall()
    finalResults = ""
    for (a,b) in cursor.fetchall():
        coursetime = TimeIDToTime(a)
        finalResults += f"（{coursetime[0]}）第{coursetime[1]}節，{b}\n"
    return finalResults
