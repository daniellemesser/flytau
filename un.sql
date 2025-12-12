#תרגיל 1
#בנו טבלאות המייצגות את הסכימה הבאה (בשם University), ומלאו מספר רשומות בכל טבלה:
#Students (Student_ID, First_Name, Last_Name, BirthDate, Phone_Number, City)
#Courses (Course_ID, Course_Name, Lecturer_ID, Is_Mandatory) 
#Lecturer (Lecturer_ID, First_Name, Last_Name, Degree)
#Grades (Student_ID, Course_ID, Year, Grade)
#Cities (City, Region, Phone_Code)
#פתרון


###########################################EX1

###DDL
CREATE SCHEMA university ;
USE university; 

CREATE TABLE students (
    StudentID INT NOT NULL,
    FirstName VARCHAR(45) NULL,
    LastName VARCHAR(45) NULL,
    BirthDate DATE NULL,
    PhoneNumber VARCHAR(45) NULL,
    City VARCHAR(45) NULL,
    PRIMARY KEY (StudentID)
);

CREATE TABLE lecturer (
    LecturerID INT NOT NULL,
    FirstName VARCHAR(45) NULL,
    LastName VARCHAR(45) NULL,
    Degree VARCHAR(45) NULL,
    PRIMARY KEY (LecturerID)
);
 
CREATE TABLE courses (
    CourseID INT NOT NULL,
    CourseName VARCHAR(45) NULL,
    LecturerID INT NULL,
    IsMandatory TINYINT NULL DEFAULT 0,
    PRIMARY KEY (CourseID),
    FOREIGN KEY (LecturerID)
        REFERENCES lecturer (LecturerID)
        ON DELETE CASCADE ON UPDATE CASCADE
);
 
CREATE TABLE grades (
    StudentID INT NOT NULL,
    CourseID INT NOT NULL,
    Year YEAR NOT NULL,
    Grade INT NULL,
    PRIMARY KEY (StudentID , CourseID , Year),
    FOREIGN KEY (StudentID)
        REFERENCES students (StudentID)
        ON DELETE CASCADE ON UPDATE CASCADE,
    FOREIGN KEY (CourseID)
        REFERENCES courses (CourseID)
        ON DELETE CASCADE ON UPDATE CASCADE
);
  
CREATE TABLE cities (
    City VARCHAR(45) NOT NULL,
    Region VARCHAR(45) NULL,
    PhoneCode VARCHAR(45) NULL,
    PRIMARY KEY (City)
);
 

###DML 
INSERT INTO students VALUES 
(1, 'Emma', 'Stone', '1988-11-06', '05034534212', 'Los Angeles'),
(2, 'Alexander', 'Teller', '1987-02-20', '05034534212', 'Tel-Aviv');


INSERT INTO lecturer (LecturerID, FirstName, Degree) VALUES 
(1, 'Erez', 'PhD'),
(2, 'Eran', 'PhD'); 


INSERT INTO courses VALUES 
(1, 'databases', 1, 1),
(2, 'bigdata', 1, 0),
(3, 'information system', 2, 0);


INSERT INTO grades  VALUES 
(1, 1, 2016, 100),
(2, 1, 2016, 59),
(2, 1, 2017, 100),
(1, 2, 2017, 100),
(2, 2, 2017, 80); 
 
 
INSERT INTO cities (City)  VALUES 
('Los Angeles'),
('Tel-Aviv'); 

#Delete Lecturer and test the foreign key CASCADE constraint
DELETE FROM lecturer
WHERE LecturerID = 1;
# Return the deleted courses (1, 2) because of cascaded deletion of LecturerID=1
INSERT INTO lecturer (LecturerID, FirstName, Degree) VALUES 
(1, 'Erez', 'PhD');
INSERT INTO courses VALUES 
(1, 'databases', 1, 1),
(2, 'bigdata', 1, 0);
 