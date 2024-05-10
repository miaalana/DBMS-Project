DROP DATABASE CourseManagement;
CREATE DATABASE CourseManagement;
DROP USER IF EXISTS 'proj2test'@'localhost';
CREATE USER 'proj2test'@'localhost' IDENTIFIED BY 'proj2password123';
GRANT ALL PRIVILEGES ON CourseManagement.* TO 'proj2test'@'localhost';
USE CourseManagement;

CREATE TABLE User (
    userID int,
    fname varchar(255),
    lname varchar(255),
    email varchar(255),        
    password varchar(255),
    role ENUM('Admin', 'Lecturer', 'Student') NOT NULL,
    PRIMARY KEY (userID)
);

CREATE TABLE Course (
    courseID int,
    courseName varchar(255),
    PRIMARY KEY (courseID)  
);

CREATE TABLE Enrol (
    userID int,
    courseID int,     
    FOREIGN KEY (userID) REFERENCES User(userID),
    FOREIGN KEY (courseID) REFERENCES Course(courseID),
    PRIMARY KEY (userID, courseID)  
);

CREATE TABLE Account (
    accountID int,
    userID int,
    password varchar(255),
    accountType varchar(255),
    FOREIGN KEY (userID) REFERENCES User(userID),
    PRIMARY KEY (accountID, userID) 
);

CREATE TABLE DiscussionForum (
    forumID int AUTO_INCREMENT,
    courseID int,
    forumName varchar(255),
    FOREIGN KEY (courseID) REFERENCES Course(courseID),
    PRIMARY KEY (forumID, courseID) 
);

CREATE TABLE DiscussionThread (
    threadID int AUTO_INCREMENT,
    forumID int,
    parentThreadID int,
    title varchar(255),
    content varchar(255),
    timestamp varchar(255),
    FOREIGN KEY (forumID) REFERENCES DiscussionForum(forumID),
    FOREIGN KEY (parentThreadID) REFERENCES DiscussionThread(threadID),
    PRIMARY KEY (threadID, forumID) 
);

CREATE TABLE CalendarEvent (
    eventID int AUTO_INCREMENT,
    courseID int,
    eventName varchar(255),
    dueDate varchar(255),
    FOREIGN KEY (courseID) REFERENCES Course(courseID),
    PRIMARY KEY (eventID, courseID) 
);

CREATE TABLE Section (
    sectionID int AUTO_INCREMENT,
    courseID int,
    sectionName varchar(255),
    FOREIGN KEY (courseID) REFERENCES Course(courseID),
    PRIMARY KEY (sectionID, courseID) 
);

CREATE TABLE SectionItem (
    itemID int AUTO_INCREMENT,
    sectionID int,
    itemType varchar(255),
    content varchar(255),
    FOREIGN KEY (sectionID) REFERENCES Section(sectionID),
    PRIMARY KEY (itemID, sectionID) 
);

CREATE TABLE Assignment (
    assignmentID int AUTO_INCREMENT,
    courseID int,
    userID int,
	Grade int,
    title varchar(255),
    submission varchar(255),
    submissionStatus varchar(255),
    gradingStatus varchar(255),
    dueDate varchar(255),
    FOREIGN KEY (courseID) REFERENCES Course(courseID),
    PRIMARY KEY (assignmentID, courseID) 
);

