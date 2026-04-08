USE institutional_document_tracker;

-- 1. Display all students
SELECT * FROM students;

-- 2. Display all approved student documents
SELECT document_name, status, uploaded_by_prn
FROM documents
WHERE uploaded_by_prn IS NOT NULL AND status = 'Approved';

-- 3. Display all pending placement documents
SELECT document_name, category, status
FROM documents
WHERE category = 'Placement' AND status = 'Pending';

-- 4. Insert a new student
INSERT INTO students (prn, name, class, email_id, contact_number, department_id, current_year, password)
VALUES (
    '2025CE099',
    'Omkar Joshi',
    'FE Computer',
    'omkar@institution.edu',
    '9000000001',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    '1st Year BTech',
    'student456'
);

-- 5. Insert a new document uploaded by a student
INSERT INTO documents (
    document_name, document_image, category, department_id, status, review_message, uploaded_by_prn, uploaded_by_teacherid
) VALUES (
    'Semester 1 Marksheet',
    'app/static/uploads/semester-1-marksheet.pdf',
    'Academic',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    'Pending',
    'Waiting for academic review.',
    '2025CE099',
    NULL
);

-- 6. Update student contact number
UPDATE students
SET contact_number = '9000000011'
WHERE prn = '2025CE099';

-- 7. Update document review message
UPDATE documents
SET review_message = 'Please upload higher resolution PDF.'
WHERE document_name = 'Semester 1 Marksheet';

-- 8. Delete one notification
DELETE FROM notifications
WHERE notification_id = (
    SELECT notification_id FROM (
        SELECT notification_id FROM notifications ORDER BY notification_id DESC LIMIT 1
    ) AS temp
);

-- 9. Use operator and function
SELECT prn, name, UPPER(current_year) AS year_label
FROM students
WHERE department_id = (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering');

-- 10. Count total pending documents
SELECT COUNT(*) AS pending_document_count
FROM documents
WHERE status = 'Pending';

-- 11. Concatenate student name and class
SELECT prn, CONCAT(name, ' - ', class) AS student_info
FROM students;

-- 12. Set operator using UNION
SELECT email_id AS email_contact, 'Teacher' AS source FROM teachers
UNION
SELECT email_id AS email_contact, 'Student' AS source FROM students;
