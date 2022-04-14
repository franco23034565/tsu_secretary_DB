# 徐書記 期中專題

`dbschema.sql` 為 DB Schema 的初始化

`AddCourse.py` 為 **幫資料庫加課程** 的 自動化程式

1. 打到Course.txt
2. 執行AddCourse.py
3. 自動產生AddCourse.sql檔

格式:
`courseID courseName Dept MaxPeople Point instructor grade MustHave CourseTime Place CourseTime Place......`

`updateDB.py` 為 預計可能用到的sql指令

- 新增用戶
`addUser(NID, UserName, UserPassword, Dept, Grade)`

* 列出必修單
`MustHaveList(NID)`

* 衝堂檢查
如果結果沒東西，就沒衝堂
`def timeCollision(NID, CourseID)`

* 選課（不包含衝堂檢查）
`chooseCourse(NID, CourseID)`

- 退選（不包含檢測"CourseID是否在該用戶的chosen中"）
`deleteCourse(NID, CourseID)`
