# 徐書記 期中專題

`dbschema.sql` 為 DB Schema 的初始化

`AddCourse.py` 為 **幫資料庫加課程** 的 自動化程式

1. 打到Course.txt
2. 執行AddCourse.py
3. 自動連線mysql並加入課程

格式:
`courseID courseName Dept HowManyPeople MaxPeople Point instructor grade MustHave CourseTime Place CourseTime Place......`

`updateDB.py` 為 預計可能用到的sql指令

- 新增用戶(密碼使用SHA256加密)
`addUser(NID, UserName, UserPassword, Dept, Grade, conn)`

* 自動選必修
`autoChooseMustHaveList(NID, conn)`

* 衝堂檢查
`timeCollision(NID,conn)`
True or False

* 加入願望清單（課程不存在 已選 已於願望清單皆return false）
`addInWishList(NID, CourseID, conn)`
True or False

* 當前學分數
`currentPoint(NID, conn)`

* 判斷是否為使用者（包括密碼檢查）
`isUser(NID, passwd, conn)`
True or False

* 列出已選課表
`listChosenList(NID)`

* 願望清單學分數
`wishListPoint(NID, conn)`

* 當前學分數加願望清單學分數
`wishListPointAddChosenPoint(NID, conn)`

* 將願望清單合併到已選清單（衝堂 超學分上限 超人數皆檢查）
`chooseCourse(NID,conn)`

* 從願望清單移除
`deleteFromWishList(NID, CourseID, conn)`

- 退選（不包含檢測"CourseID是否在該用戶的chosen中"）
`deleteCourse(NID, CourseID)`
