create table Users(
NID varchar(10),
Name varchar(20),
Account varchar(255),
Password varchar(255),
Dept varchar(20),
Grade int
);

create table Chosen(
NID varchar(10),
CourseID int
);

create table AllCourse(
CourseID int,
CourseName varchar(255),
Dept varchar(20),
PeopleLimit int,
Point int,
Teacher varchar(20),
Grade int,
MustHave BOOLEAN
);

create table CourseTime(
CourseID int,
Time int,
Classroom varchar(20)
);
