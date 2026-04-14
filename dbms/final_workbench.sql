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
('Aarav Sharma', 'System Admin', 'aarav.sharma@pccoepune.org', '9999999999', 1);

INSERT INTO Placement_Cell (Name, Role, Email_ID, Contact_Number, Department_ID) VALUES
('Kabir Malhotra', 'Placement Coordinator', 'kabir.malhotra@pccoepune.org', '8888888888', 2),
('Sonal Tambe', 'Placement Officer', 'sonal.tambe@pccoepune.org', '8888888887', 2),
('Rahul Chitre', 'Placement Executive', 'rahul.chitre@pccoepune.org', '8888888886', 2),
('Priya Deshmukh', 'Placement Officer', 'priya.deshmukh@pccoepune.org', '8888888885', 2),
('Amit Ranade', 'Placement Executive', 'amit.ranade@pccoepune.org', '8888888884', 2),
('Neha Pansare', 'Placement Officer', 'neha.pansare@pccoepune.org', '8888888883', 2),
('Rohan Pawar', 'Placement Executive', 'rohan.pawar@pccoepune.org', '8888888882', 2),
('Anjali Rane', 'Placement Officer', 'anjali.rane@pccoepune.org', '8888888881', 2),
('Deepak Khedkar', 'Placement Executive', 'deepak.khedkar@pccoepune.org', '8888888870', 2),
('Shruti Sathe', 'Placement Officer', 'shruti.sathe@pccoepune.org', '8888888869', 2),
('Vikas Nimbalkar', 'Placement Executive', 'vikas.nimbalkar@pccoepune.org', '8888888868', 2),
('Pallavi Mokashi', 'Placement Officer', 'pallavi.mokashi@pccoepune.org', '8888888867', 2),
('Kiran Naik', 'Placement Executive', 'kiran.naik@pccoepune.org', '8888888866', 2),
('Manish Bendre', 'Placement Officer', 'manish.bendre@pccoepune.org', '8888888865', 2),
('Tanvi Bhujbal', 'Placement Executive', 'tanvi.bhujbal@pccoepune.org', '8888888864', 2),
('Komal Bhise', 'Placement Officer', 'komal.bhise@pccoepune.org', '8888888863', 2),
('Ajay Dhamale', 'Placement Executive', 'ajay.dhamale@pccoepune.org', '8888888862', 2),
('Snehal Chavan', 'Placement Officer', 'snehal.chavan@pccoepune.org', '8888888861', 2),
('Tejas Bhosale', 'Placement Executive', 'tejas.bhosale@pccoepune.org', '8888888860', 2),
('Yash Suryawanshi', 'Placement Officer', 'yash.suryawanshi@pccoepune.org', '8888888859', 2);

INSERT INTO Scholarship_Cell (Name, Role, Email_ID, Contact_Number, Department_ID) VALUES
('Neha Karmarkar', 'Scholarship Coordinator', 'neha.karmarkar@pccoepune.org', '7777777777', 3),
('Priya Gokhale', 'Scholarship Officer', 'priya.gokhale@pccoepune.org', '7777777776', 3),
('Aditi Dongre', 'Scholarship Executive', 'aditi.dongre@pccoepune.org', '7777777775', 3),
('Rohan Thombre', 'Scholarship Officer', 'rohan.thombre@pccoepune.org', '7777777774', 3),
('Sonal Bhadane', 'Scholarship Executive', 'sonal.bhadane@pccoepune.org', '7777777773', 3),
('Deepak Lagad', 'Scholarship Officer', 'deepak.lagad@pccoepune.org', '7777777772', 3),
('Shruti Karale', 'Scholarship Executive', 'shruti.karale@pccoepune.org', '7777777771', 3),
('Aman Darade', 'Scholarship Officer', 'aman.darade@pccoepune.org', '7777777770', 3),
('Pallavi Thorat', 'Scholarship Executive', 'pallavi.thorat@pccoepune.org', '7777777769', 3),
('Rakesh Chorge', 'Scholarship Officer', 'rakesh.chorge@pccoepune.org', '7777777768', 3),
('Snehal Hole', 'Scholarship Executive', 'snehal.hole@pccoepune.org', '7777777767', 3),
('Komal Madne', 'Scholarship Officer', 'komal.madne@pccoepune.org', '7777777766', 3),
('Tejas Khaire', 'Scholarship Executive', 'tejas.khaire@pccoepune.org', '7777777765', 3),
('Yash Gedam', 'Scholarship Officer', 'yash.gedam@pccoepune.org', '7777777764', 3),
('Kunal Pethkar', 'Scholarship Executive', 'kunal.pethkar@pccoepune.org', '7777777763', 3),
('Megha Raut', 'Scholarship Officer', 'megha.raut@pccoepune.org', '7777777762', 3),
('Tanvi Ingle', 'Scholarship Executive', 'tanvi.ingle@pccoepune.org', '7777777761', 3),
('Vikas Nale', 'Scholarship Officer', 'vikas.nale@pccoepune.org', '7777777760', 3),
('Anjali Khese', 'Scholarship Executive', 'anjali.khese@pccoepune.org', '7777777759', 3),
('Akash Kharat', 'Scholarship Officer', 'akash.kharat@pccoepune.org', '7777777758', 3);

INSERT INTO Students (PRN, Name, Class, Email_ID, Contact_Number, Department_ID, Current_Year, Password) VALUES
('124B1F095', 'Kanak Kushwaha', 'SY', 'kanak.kushwaha24@pccoepune.org', '9800000001', 1, '2nd Year BTech', 'PCCOE@123'),
('124B1F096', 'Aarohi Patil', 'SY', 'aarohi.patil24@pccoepune.org', '9800000002', 1, '2nd Year BTech', 'PCCOE@123'),
('124B1F097', 'Vivaan Shah', 'SY', 'vivaan.shah24@pccoepune.org', '9800000003', 1, '2nd Year BTech', 'PCCOE@123'),
('124B1F098', 'Ishita Nair', 'SY', 'ishita.nair24@pccoepune.org', '9800000004', 1, '2nd Year BTech', 'PCCOE@123'),
('124B1F099', 'Parth Jadhav', 'SY', 'parth.jadhav24@pccoepune.org', '9800000005', 1, '2nd Year BTech', 'PCCOE@123'),
('124B1F100', 'Nehal More', 'SY', 'nehal.more24@pccoepune.org', '9800000006', 1, '2nd Year BTech', 'PCCOE@123'),
('124B1F101', 'Pranav Joshi', 'SY', 'pranav.joshi24@pccoepune.org', '9800000007', 1, '2nd Year BTech', 'PCCOE@123'),
('124B1F102', 'Diya Sharma', 'SY', 'diya.sharma24@pccoepune.org', '9800000008', 1, '2nd Year BTech', 'PCCOE@123'),
('124B1F103', 'Saket Verma', 'SY', 'saket.verma24@pccoepune.org', '9800000009', 1, '2nd Year BTech', 'PCCOE@123'),
('124B1F104', 'Anvi Gupta', 'SY', 'anvi.gupta24@pccoepune.org', '9800000010', 1, '2nd Year BTech', 'PCCOE@123'),
('123B1F105', 'Kunal Patwardhan', 'TY', 'kunal.patwardhan23@pccoepune.org', '9800000011', 1, '3rd Year BTech', 'PCCOE@123'),
('123B1F106', 'Riya Patel', 'TY', 'riya.patel23@pccoepune.org', '9800000012', 1, '3rd Year BTech', 'PCCOE@123'),
('123B1F107', 'Aditya Nair', 'TY', 'aditya.nair23@pccoepune.org', '9800000013', 1, '3rd Year BTech', 'PCCOE@123'),
('123B1F108', 'Sneha Deshmukh', 'TY', 'sneha.deshmukh23@pccoepune.org', '9800000014', 1, '3rd Year BTech', 'PCCOE@123'),
('123B1F109', 'Rahul Shinde', 'TY', 'rahul.shinde23@pccoepune.org', '9800000015', 1, '3rd Year BTech', 'PCCOE@123'),
('123B1F110', 'Aman Kulkarni', 'TY', 'aman.kulkarni23@pccoepune.org', '9800000016', 1, '3rd Year BTech', 'PCCOE@123'),
('123B1F111', 'Sharvari Pawar', 'TY', 'sharvari.pawar23@pccoepune.org', '9800000017', 1, '3rd Year BTech', 'PCCOE@123'),
('123B1F112', 'Tanmay Desai', 'TY', 'tanmay.desai23@pccoepune.org', '9800000018', 1, '3rd Year BTech', 'PCCOE@123'),
('123B1F113', 'Mitali Bhosale', 'TY', 'mitali.bhosale23@pccoepune.org', '9800000019', 1, '3rd Year BTech', 'PCCOE@123'),
('123B1F114', 'Yash Khanna', 'TY', 'yash.khanna23@pccoepune.org', '9800000020', 1, '3rd Year BTech', 'PCCOE@123'),
('124B1I115', 'Tanvi Kulkarni', 'SY', 'tanvi.kulkarni24@pccoepune.org', '9800000021', 4, '2nd Year BTech', 'PCCOE@123'),
('124B1I116', 'Rudra Sawant', 'SY', 'rudra.sawant24@pccoepune.org', '9800000022', 4, '2nd Year BTech', 'PCCOE@123'),
('124B1I117', 'Mitali Shinde', 'SY', 'mitali.shinde24@pccoepune.org', '9800000023', 4, '2nd Year BTech', 'PCCOE@123'),
('124B1I118', 'Harsh Desai', 'SY', 'harsh.desai24@pccoepune.org', '9800000024', 4, '2nd Year BTech', 'PCCOE@123'),
('124B1I119', 'Kashish Yadav', 'SY', 'kashish.yadav24@pccoepune.org', '9800000025', 4, '2nd Year BTech', 'PCCOE@123'),
('124B1I120', 'Rhea Naidu', 'SY', 'rhea.naidu24@pccoepune.org', '9800000026', 4, '2nd Year BTech', 'PCCOE@123'),
('124B1I121', 'Atharv Kale', 'SY', 'atharv.kale24@pccoepune.org', '9800000027', 4, '2nd Year BTech', 'PCCOE@123'),
('124B1I122', 'Pallavi Mane', 'SY', 'pallavi.mane24@pccoepune.org', '9800000028', 4, '2nd Year BTech', 'PCCOE@123'),
('124B1I123', 'Saanvi Salunke', 'SY', 'saanvi.salunke24@pccoepune.org', '9800000029', 4, '2nd Year BTech', 'PCCOE@123'),
('124B1I124', 'Om Chavan', 'SY', 'om.chavan24@pccoepune.org', '9800000030', 4, '2nd Year BTech', 'PCCOE@123'),
('123B1I125', 'Vedant Shirole', 'TY', 'vedant.shirole23@pccoepune.org', '9800000031', 4, '3rd Year BTech', 'PCCOE@123'),
('123B1I126', 'Gauri Pathak', 'TY', 'gauri.pathak23@pccoepune.org', '9800000032', 4, '3rd Year BTech', 'PCCOE@123'),
('123B1I127', 'Aryan Jain', 'TY', 'aryan.jain23@pccoepune.org', '9800000033', 4, '3rd Year BTech', 'PCCOE@123'),
('123B1I128', 'Khushi Mehta', 'TY', 'khushi.mehta23@pccoepune.org', '9800000034', 4, '3rd Year BTech', 'PCCOE@123'),
('123B1I129', 'Soham Pinge', 'TY', 'soham.pinge23@pccoepune.org', '9800000035', 4, '3rd Year BTech', 'PCCOE@123'),
('123B1I130', 'Prajakta Lokhande', 'TY', 'prajakta.lokhande23@pccoepune.org', '9800000036', 4, '3rd Year BTech', 'PCCOE@123'),
('123B1I131', 'Tushar Gite', 'TY', 'tushar.gite23@pccoepune.org', '9800000037', 4, '3rd Year BTech', 'PCCOE@123'),
('123B1I132', 'Nikita Gaikwad', 'TY', 'nikita.gaikwad23@pccoepune.org', '9800000038', 4, '3rd Year BTech', 'PCCOE@123'),
('123B1I133', 'Swaraj Mohite', 'TY', 'swaraj.mohite23@pccoepune.org', '9800000039', 4, '3rd Year BTech', 'PCCOE@123'),
('123B1I134', 'Mrunal Jagtap', 'TY', 'mrunal.jagtap23@pccoepune.org', '9800000040', 4, '3rd Year BTech', 'PCCOE@123');

INSERT INTO Teachers (Name, Email_ID, Contact_Number, Department_ID, Role, Password) VALUES
('Prof. Meera Singh', 'meera.singh@pccoepune.org', '5555555555', 1, 'Teacher', 'Staff@123'),
('Prof. Kabir Jain', 'kabir.jain@pccoepune.org', '6666666666', 4, 'Teacher', 'Staff@123');

INSERT INTO Documents
    (Document_Name, Document_Type, Upload_Date, Category, Department_ID, Status, Review_Message, Uploaded_By_PRN, Uploaded_By_TeacherID)
VALUES
('10th Marksheet', 'PDF', CURDATE(), 'Academic', 1, 'Approved', 'Verified and matched with admission records.', '124B1F095', NULL),
('12th Marksheet', 'PDF', CURDATE(), 'Academic', 1, 'Pending', 'Upload a clearer scan with visible board stamp.', '124B1F095', NULL),
('Leaving Certificate', 'PDF', CURDATE(), 'Academic', 1, 'Approved', 'Accepted by the admin office.', '124B1F095', NULL),
('Semester 5 Marksheet', 'PDF', CURDATE(), 'Academic', 1, 'Approved', 'Verified by academic office.', '123B1F106', NULL),
('Aadhaar Card', 'PDF', CURDATE(), 'ID Proof', 1, 'Approved', 'Identity proof accepted.', '124B1F095', NULL),
('Placement Resume', 'PDF', CURDATE(), 'Placement', 2, 'Pending', 'Please update your resume headline and skills section.', '123B1F106', NULL),
('GitHub Profile Link', 'LINK', CURDATE(), 'Placement', 2, 'Approved', 'Profile reviewed and accepted by placement mentor.', '123B1F106', NULL),
('LinkedIn Profile Link', 'LINK', CURDATE(), 'Placement', 2, 'Pending', 'Please add headline, skills and latest projects before final review.', '123B1F106', NULL),
('Scholarship Form', 'PDF', CURDATE(), 'Scholarship', 3, 'Pending', 'Fee receipt still under verification.', '124B1I120', NULL),
('Fee Receipt', 'JPG', CURDATE(), 'Finance', 3, 'Approved', 'Payment proof confirmed.', '124B1I120', NULL),
('OfferLetter', 'PDF', CURDATE(), 'Placement', 2, 'Pending', 'Add company seal and signed page.', '124B1F101', NULL),
('Resume', 'PDF', CURDATE(), 'Placement', 2, 'Approved', 'Resume accepted.', '124B1F100', NULL),
('Marksheet', 'PDF', CURDATE(), 'Academic', 4, 'Approved', 'Academic verification complete.', '124B1F100', NULL),
('ResearchPaper', 'DOC', CURDATE(), 'Department', 1, 'Approved', 'Shared with department.', NULL, 1),
('Attendance Sheet', 'PDF', CURDATE(), 'Academic', 1, 'Pending', 'Upload latest monthly attendance.', NULL, 1);

INSERT INTO Notifications (PRN, Document_ID, Message) VALUES
('124B1F095', 2, 'Upload a clearer scan with visible board stamp.'),
('123B1F106', 6, 'Please update your resume headline and skills section.'),
('124B1I120', 9, 'Fee receipt still under verification.');

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
VALUES ('124B1F200', 'Test User', 'SY', 'test.user24@pccoepune.org', '9999999990', 1, '2nd Year BTech', 'PCCOE@123');

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
