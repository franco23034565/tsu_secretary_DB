f = open("Course.txt", 'r')

tf = open("AddCourse.sql", 'w')

def isInt(s):
    try:
        int(s)
        return True
    except:
        return False

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
        if (isInt(word)):   #is integer
            #print(int(word))
            courseInfoList.append(int(word))
        else:               #not integer
            #print('\'' + word + '\'')
            courseInfoList.append(word)
    #print(courseInfoList)
    courseTime = courseInfoList[8:]
    #print(courseTime)

    tf.write(insert_AllCourse(courseInfoList))
    tf.write(insert_CourseTime(courseInfoList[0], courseTime))
    #print(insert_AllCourse(courseInfoList))
    #print(insert_CourseTime(courseInfoList[0], courseTime))

tf.close()
f.close()