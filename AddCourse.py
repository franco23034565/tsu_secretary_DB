f = open("Course.txt", 'r')

#print(f.readlines())

def isInt(s):
    try:
        int(s)
        return True
    except:
        return False

#init
courseInfoList = [0, "", "", 0, 0, "", 0, ""]
CourseID = 0
CourseName = ""
Dept = ""
PeopleLimit = 0
Point = 0
Teacher = ""
Grade = 0
MustHave = False

#read line and seperate each element
for line in f.readlines():
    i=0
    for word in line.split():
        if (isInt(word)):   #is integer
            print(int(word))
            courseInfoList[i] = int(word)
            i+=1
            continue
        print('\'' + word + '\'')
        courseInfoList[i] = word
        i+=1
        print(courseInfoList)

f.close()

'''
CourseID int PRIMARY KEY,
CourseName varchar(255),
Dept varchar(20),
PeopleLimit int,
Point int,
Teacher varchar(20),
Grade int,
MustHave BOOLEAN
'''