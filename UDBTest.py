# updateDB.py testing place

import updateDB as udb
import MySQLdb

conn = MySQLdb.connect(host="127.0.0.1",
                           user="hj",
                           passwd="test1234",
                           db="testdb")
cursor = conn.cursor()

NID = "D0915679"
userName = "紀彥廷"
userDept = "資訊工程學系"
userPasswd = "IWasTesting"
userGrade = 2
udb.addUser(NID, userName, userPasswd, userDept, userGrade, conn)
