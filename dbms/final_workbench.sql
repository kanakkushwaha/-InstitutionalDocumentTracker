-- =========================================
-- INSTITUTIONAL DOCUMENT TRACKER
-- FULL AND FINAL MYSQL WORKBENCH SCRIPT
-- =========================================

DROP DATABASE IF EXISTS InstitutionalTracker;
CREATE DATABASE InstitutionalTracker;
USE InstitutionalTracker;

-- =========================================
-- TABLES
-- =========================================

CREATE TABLE Departments (
    Department_ID INT AUTO_INCREMENT PRIMARY KEY,
    Department_Name VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE Admin (
    Admin_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Role VARCHAR(50) NOT NULL,
    Email_ID VARCHAR(100) NOT NULL UNIQUE,
    Contact_Number VARCHAR(15) NOT NULL UNIQUE,
    Department_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES Departments(Department_ID)
        ON DELETE SET NULL
);

CREATE TABLE Placement_Cell (
    Placement_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Role VARCHAR(50) NOT NULL,
    Email_ID VARCHAR(100) NOT NULL UNIQUE,
    Contact_Number VARCHAR(15) NOT NULL UNIQUE,
    Department_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES Departments(Department_ID)
        ON DELETE SET NULL
);

CREATE TABLE Scholarship_Cell (
    Scholarship_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Role VARCHAR(50) NOT NULL,
    Email_ID VARCHAR(100) NOT NULL UNIQUE,
    Contact_Number VARCHAR(15) NOT NULL UNIQUE,
    Department_ID INT,
    FOREIGN KEY (Department_ID) REFERENCES Departments(Department_ID)
        ON DELETE SET NULL
);

CREATE TABLE Students (
    PRN VARCHAR(20) PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Class VARCHAR(50) NOT NULL,
    Email_ID VARCHAR(100) NOT NULL UNIQUE,
    Contact_Number VARCHAR(15) NOT NULL,
    Department_ID INT,
    Current_Year VARCHAR(30),
    Password VARCHAR(100),
    FOREIGN KEY (Department_ID) REFERENCES Departments(Department_ID)
        ON DELETE SET NULL
);

CREATE TABLE Teachers (
    Teacher_ID INT AUTO_INCREMENT PRIMARY KEY,
    Name VARCHAR(100) NOT NULL,
    Email_ID VARCHAR(100) NOT NULL UNIQUE,
    Contact_Number VARCHAR(15) NOT NULL,
    Department_ID INT,
    Role VARCHAR(50),
    Password VARCHAR(100),
    FOREIGN KEY (Department_ID) REFERENCES Departments(Department_ID)
        ON DELETE SET NULL
);

CREATE TABLE Documents (
    Document_ID INT AUTO_INCREMENT PRIMARY KEY,
    Document_Name VARCHAR(150) NOT NULL,
    Document_Type VARCHAR(50) NOT NULL,
    Upload_Date DATE DEFAULT (CURRENT_DATE),
    Category VARCHAR(50),
    Department_ID INT,
    Status VARCHAR(40) DEFAULT 'Pending',
    Review_Message TEXT,
    Uploaded_By_PRN VARCHAR(20),
    Uploaded_By_TeacherID INT,
    FOREIGN KEY (Department_ID) REFERENCES Departments(Department_ID)
        ON DELETE SET NULL,
    FOREIGN KEY (Uploaded_By_PRN) REFERENCES Students(PRN)
        ON DELETE CASCADE,
    FOREIGN KEY (Uploaded_By_TeacherID) REFERENCES Teachers(Teacher_ID)
        ON DELETE CASCADE
);

CREATE TABLE Notifications (
    Notification_ID INT AUTO_INCREMENT PRIMARY KEY,
    PRN VARCHAR(20),
    Document_ID INT,
    Message VARCHAR(255),
    Created_At DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (PRN) REFERENCES Students(PRN)
        ON DELETE CASCADE,
    FOREIGN KEY (Document_ID) REFERENCES Documents(Document_ID)
        ON DELETE SET NULL
);

CREATE TABLE Audit_Log (
    Log_ID INT AUTO_INCREMENT PRIMARY KEY,
    Message VARCHAR(255),
    Log_Time DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- =========================================
-- INDEXES
-- =========================================

CREATE INDEX idx_student_email ON Students(Email_ID);
CREATE INDEX idx_teacher_email ON Teachers(Email_ID);
CREATE INDEX idx_doc_type ON Documents(Document_Type);
CREATE INDEX idx_doc_status ON Documents(Status);
CREATE INDEX idx_doc_prn ON Documents(Uploaded_By_PRN);
CREATE INDEX idx_doc_teacher ON Documents(Uploaded_By_TeacherID);

-- =========================================
-- SAMPLE DATA
-- =========================================

INSERT INTO Departments (Department_Name) VALUES
('Computer Engineering'),
('Placement Cell'),
('Scholarship Cell'),
('Information Technology');

INSERT INTO Admin (Name, Role, Email_ID, Contact_Number, Department_ID) VALUES
('Aarav Sharma', 'System Admin', 'admin@institution.edu', '9999999999', 1);

INSERT INTO Placement_Cell (Name, Role, Email_ID, Contact_Number, Department_ID) VALUES
('Dr. Meera Singh', 'Placement Coordinator', 'place@institution.edu', '8888888888', 2);

INSERT INTO Scholarship_Cell (Name, Role, Email_ID, Contact_Number, Department_ID) VALUES
('Prof. Kabir Jain', 'Scholarship Coordinator', 'scholar@institution.edu', '7777777777', 3);

INSERT INTO Students (PRN, Name, Class, Email_ID, Contact_Number, Department_ID, Current_Year, Password) VALUES
('2022CE041', 'Riya Patel', 'BE Computer', 'student@institution.edu', '9898989898', 1, '4th Year BTech', 'student123'),
('2023IT018', 'Aditya Nair', 'TE IT', 'aditya@institution.edu', '9870011223', 4, '3rd Year BTech', 'student234'),
('2024CE052', 'Sneha Deshmukh', 'SE Computer', 'sneha@institution.edu', '9870011224', 1, '2nd Year BTech', 'student345'),
('124B1F100', 'Sharvari', 'SY', 's@gmail.com', '1111111111', 4, '2nd Year BTech', 'pass100'),
('124B1F101', 'Anita', 'SY', 'a@gmail.com', '2222222222', 4, '2nd Year BTech', 'pass101'),
('124B1F102', 'Rahul', 'TY', 'r@gmail.com', '3333333333', 1, '3rd Year BTech', 'pass102'),
('124B1F103', 'Aman', 'SY', 'aman@gmail.com', '4444444444', 4, '2nd Year BTech', 'pass103');

INSERT INTO Teachers (Name, Email_ID, Contact_Number, Department_ID, Role, Password) VALUES
('Dr. Meera Singh', 'teacher@institution.edu', '5555555555', 2, 'Teacher', 'teacher123'),
('Prof. B', 'b@college.com', '6666666666', 1, 'Teacher', 'teacher234');

INSERT INTO Documents
    (Document_Name, Document_Type, Upload_Date, Category, Department_ID, Status, Review_Message, Uploaded_By_PRN, Uploaded_By_TeacherID)
VALUES
('10th Marksheet', 'PDF', CURDATE(), 'Academic', 1, 'Approved', 'Verified and matched with admission records.', '2022CE041', NULL),
('12th Marksheet', 'PDF', CURDATE(), 'Academic', 1, 'Pending', 'Upload a clearer scan with visible board stamp.', '2022CE041', NULL),
('Leaving Certificate', 'PDF', CURDATE(), 'Academic', 1, 'Approved', 'Accepted by the admin office.', '2022CE041', NULL),
('Semester 5 Marksheet', 'PDF', CURDATE(), 'Academic', 1, 'Approved', 'Verified by academic office.', '2022CE041', NULL),
('Aadhaar Card', 'PDF', CURDATE(), 'ID Proof', 1, 'Approved', 'Identity proof accepted.', '2022CE041', NULL),
('Placement Resume', 'PDF', CURDATE(), 'Placement', 2, 'Pending', 'Please update your resume headline and skills section.', '2022CE041', NULL),
('GitHub Profile Link', 'LINK', CURDATE(), 'Placement', 2, 'Approved', 'Profile reviewed and accepted by placement mentor.', '2022CE041', NULL),
('LinkedIn Profile Link', 'LINK', CURDATE(), 'Placement', 2, 'Pending', 'Please add headline, skills and latest projects before final review.', '2022CE041', NULL),
('Scholarship Form', 'PDF', CURDATE(), 'Scholarship', 3, 'Pending', 'Fee receipt still under verification.', '2022CE041', NULL),
('Fee Receipt', 'JPG', CURDATE(), 'Finance', 3, 'Approved', 'Payment proof confirmed.', '2022CE041', NULL),
('OfferLetter', 'PDF', CURDATE(), 'Placement', 2, 'Pending', 'Add company seal and signed page.', '124B1F101', NULL),
('Resume', 'PDF', CURDATE(), 'Placement', 2, 'Approved', 'Resume accepted.', '124B1F100', NULL),
('Marksheet', 'PDF', CURDATE(), 'Academic', 4, 'Approved', 'Academic verification complete.', '124B1F100', NULL),
('ResearchPaper', 'DOC', CURDATE(), 'Department', 1, 'Approved', 'Shared with department.', NULL, 1),
('Attendance Sheet', 'PDF', CURDATE(), 'Academic', 1, 'Pending', 'Upload latest monthly attendance.', NULL, 1);

INSERT INTO Notifications (PRN, Document_ID, Message) VALUES
('2022CE041', 2, 'Upload a clearer scan with visible board stamp.'),
('2022CE041', 6, 'Please update your resume headline and skills section.'),
('2022CE041', 9, 'Fee receipt still under verification.');

-- =========================================
-- DML QUERIES
-- =========================================

-- 1. SELECT all students
SELECT * FROM Students;

-- 2. UPDATE a student class
UPDATE Students SET Class = 'TY' WHERE PRN = '124B1F101';

-- 3. DELETE one student
DELETE FROM Students WHERE PRN = '124B1F103';

-- 4. operator =
SELECT * FROM Students WHERE Department_ID = 1;

-- 5. operator LIKE
SELECT * FROM Students WHERE Name LIKE 'A%';

-- 6. COUNT function
SELECT COUNT(*) AS Total_Students FROM Students;

-- 7. MAX function
SELECT MAX(PRN) AS Highest_PRN FROM Students;

-- 8. INSERT a new student
INSERT INTO Students (PRN, Name, Class, Email_ID, Contact_Number, Department_ID, Current_Year, Password)
VALUES ('124B1F200', 'TestUser', 'SY', 'test@gmail.com', '9999999990', 1, '2nd Year BTech', 'test123');

-- 9. INSERT a new document
INSERT INTO Documents (Document_Name, Document_Type, Upload_Date, Category, Department_ID, Status, Review_Message, Uploaded_By_PRN, Uploaded_By_TeacherID)
VALUES ('Bonafide Certificate', 'PDF', CURDATE(), 'Academic', 1, 'Pending', 'Submitted for review.', '124B1F200', NULL);

-- 10. UPDATE document review message
UPDATE Documents
SET Review_Message = 'Please upload clearer PDF copy.'
WHERE Document_Name = 'Bonafide Certificate';

-- 11. DELETE one notification
DELETE FROM Notifications
WHERE Notification_ID = (
    SELECT Notification_ID FROM (
        SELECT Notification_ID FROM Notifications ORDER BY Notification_ID DESC LIMIT 1
    ) AS temp
);

-- 12. UNION set operator
SELECT Email_ID AS Contact_Email, 'Student' AS Source FROM Students
UNION
SELECT Email_ID AS Contact_Email, 'Teacher' AS Source FROM Teachers;

-- =========================================
-- JOINS
-- =========================================

-- 1. INNER JOIN
SELECT s.Name, d.Department_Name
FROM Students s
INNER JOIN Departments d ON s.Department_ID = d.Department_ID;

-- 2. LEFT JOIN
SELECT s.Name, doc.Document_Name
FROM Students s
LEFT JOIN Documents doc ON s.PRN = doc.Uploaded_By_PRN;

-- 3. RIGHT JOIN
SELECT doc.Document_Name, s.Name
FROM Documents doc
RIGHT JOIN Students s ON doc.Uploaded_By_PRN = s.PRN;

-- 4. Teacher with department
SELECT t.Name AS Teacher_Name, d.Department_Name
FROM Teachers t
JOIN Departments d ON t.Department_ID = d.Department_ID;

-- =========================================
-- SUBQUERIES
-- =========================================

-- 5. IN
SELECT Name FROM Students
WHERE PRN IN (SELECT Uploaded_By_PRN FROM Documents WHERE Uploaded_By_PRN IS NOT NULL);

-- 6. NOT IN
SELECT Name FROM Students
WHERE PRN NOT IN (
    SELECT Uploaded_By_PRN FROM Documents WHERE Uploaded_By_PRN IS NOT NULL
);

-- 7. EXISTS
SELECT Name
FROM Students s
WHERE EXISTS (
    SELECT 1
    FROM Documents d
    WHERE d.Uploaded_By_PRN = s.PRN
);

-- 8. MAX subquery with HAVING
SELECT Department_ID
FROM Students
GROUP BY Department_ID
HAVING COUNT(*) = (
    SELECT MAX(cnt)
    FROM (
        SELECT COUNT(*) AS cnt
        FROM Students
        GROUP BY Department_ID
    ) AS temp
);

-- =========================================
-- GROUP BY AND HAVING
-- =========================================

-- 9. GROUP BY
SELECT Department_ID, COUNT(*) AS Total_Students
FROM Students
GROUP BY Department_ID;

-- 10. GROUP BY with HAVING
SELECT Department_ID, COUNT(*) AS Student_Count
FROM Students
GROUP BY Department_ID
HAVING COUNT(*) > 1;

-- 11. GROUP BY documents
SELECT Category, COUNT(*) AS Total_Documents
FROM Documents
GROUP BY Category
HAVING COUNT(*) >= 1;

-- =========================================
-- VIEW
-- =========================================

DROP VIEW IF EXISTS Student_Document_View;

CREATE VIEW Student_Document_View AS
SELECT
    s.Name AS Student_Name,
    d.Document_Name,
    d.Document_Type,
    d.Status,
    d.Review_Message
FROM Students s
JOIN Documents d ON s.PRN = d.Uploaded_By_PRN;

-- =========================================
-- FUNCTION
-- =========================================

DROP FUNCTION IF EXISTS GetDocCount;

DELIMITER //
CREATE FUNCTION GetDocCount(prn_val VARCHAR(20))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE total INT;
    SELECT COUNT(*) INTO total
    FROM Documents
    WHERE Uploaded_By_PRN = prn_val;
    RETURN total;
END //
DELIMITER ;

-- =========================================
-- PROCEDURES
-- =========================================

DROP PROCEDURE IF EXISTS GetStudents;
DROP PROCEDURE IF EXISTS ShowStudents;

DELIMITER //
CREATE PROCEDURE GetStudents(IN dept INT)
BEGIN
    SELECT * FROM Students WHERE Department_ID = dept;
END //
DELIMITER ;

DELIMITER //
CREATE PROCEDURE ShowStudents()
BEGIN
    DECLARE done INT DEFAULT FALSE;
    DECLARE sname VARCHAR(100);

    DECLARE cur CURSOR FOR SELECT Name FROM Students;
    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

    OPEN cur;

    read_loop: LOOP
        FETCH cur INTO sname;
        IF done THEN
            LEAVE read_loop;
        END IF;
        SELECT sname AS Student_Name;
    END LOOP;

    CLOSE cur;
END //
DELIMITER ;

-- =========================================
-- TRIGGERS
-- =========================================

DROP TRIGGER IF EXISTS after_insert_student;
DROP TRIGGER IF EXISTS after_insert_document;
DROP TRIGGER IF EXISTS after_update_document;

DELIMITER //
CREATE TRIGGER after_insert_student
AFTER INSERT ON Students
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(Message)
    VALUES (CONCAT('New Student Added: ', NEW.Name));
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER after_insert_document
AFTER INSERT ON Documents
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(Message)
    VALUES (CONCAT('New Document Added: ', NEW.Document_Name));
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER after_update_document
AFTER UPDATE ON Documents
FOR EACH ROW
BEGIN
    INSERT INTO Audit_Log(Message)
    VALUES (
        CONCAT(
            'Document Status Changed: ',
            OLD.Document_Name,
            ' from ',
            OLD.Status,
            ' to ',
            NEW.Status
        )
    );
END //
DELIMITER ;

-- =========================================
-- TESTING / DEMO QUERIES
-- =========================================

SELECT * FROM Students;
SELECT * FROM Teachers;
SELECT * FROM Documents;
SELECT * FROM Student_Document_View;
SELECT GetDocCount('124B1F100') AS Document_Count_For_124B1F100;
CALL GetStudents(1);
CALL ShowStudents();
SELECT * FROM Audit_Log;
