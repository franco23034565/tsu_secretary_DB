# updateDB.py testing place

import updateDB as udb
import MySQLdb

conn = MySQLdb.connect(host="127.0.0.1",
                           user="hj",
                           passwd="test1234",
                           db="testdb")
#cursor = conn.cursor()

NID = "D0915679"
userName = "紀彥廷"
userDept = "資訊系"
userPasswd = "IWasTesting"
userGrade = 2
udb.addUser(NID, userName, userPasswd, userDept, userGrade, conn)
udb.autoChooseMustHaveList(NID, conn)
#udb.deleteCourse(NID, 9487, conn)

#print(udb.isUser(NID, "IWasTestins", conn))
    