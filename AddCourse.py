f = open("Course.txt", 'r')

tf = open("AddCourse.sql", 'w')


def insert_AllCourse(infoList):
    seq_com = f"insert into allcourse values({infoList[0]}, {infoList[1]}, {infoList[2]}, {infoList[3]}, {infoList[4]}, {infoList[5]}, {infoList[6]}, {infoList[7]});\n"
    return seq_com


def insert_CourseTime(CourseID, CTList):
    i=0
    seq_com = ""
    for CT in CTList:
        if i%2 == 0:
            seq_com += f"insert into coursetime values({CourseID}, {CT}, "
            i+=1
        else:
            seq_com += f"{CT});\n"
            i=0
    return seq_com


#read line and seperate each element
for line in f.readlines():
    courseInfoList = []
    for word in line.split():
        courseInfoList.append(word)

    courseTime = courseInfoList[8:]

    tf.write(insert_AllCourse(courseInfoList))
    tf.write(insert_CourseTime(courseInfoList[0], courseTime))

tf.close()
f.close()