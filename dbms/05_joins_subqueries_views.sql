USE institutional_document_tracker;

-- View 1: student document details
CREATE OR REPLACE VIEW vw_student_documents AS
SELECT
    d.document_id,
    d.document_name,
    d.category,
    d.status,
    d.review_message,
    s.prn,
    s.name AS student_name,
    dep.department_name
FROM documents d
JOIN students s ON d.uploaded_by_prn = s.prn
LEFT JOIN departments dep ON d.department_id = dep.department_id;

-- View 2: teacher uploaded documents
CREATE OR REPLACE VIEW vw_teacher_documents AS
SELECT
    d.document_id,
    d.document_name,
    d.category,
    d.status,
    t.teacher_id,
    t.name AS teacher_name,
    dep.department_name
FROM documents d
JOIN teachers t ON d.uploaded_by_teacherid = t.teacher_id
LEFT JOIN departments dep ON d.department_id = dep.department_id;

-- 1. Inner join: students and departments
SELECT s.prn, s.name, dep.department_name
FROM students s
INNER JOIN departments dep ON s.department_id = dep.department_id;

-- 2. Left join: all students with uploaded documents
SELECT s.prn, s.name, d.document_name, d.status
FROM students s
LEFT JOIN documents d ON s.prn = d.uploaded_by_prn;

-- 3. Right join style report: all departments and teachers
SELECT dep.department_name, t.name AS teacher_name
FROM teachers t
RIGHT JOIN departments dep ON t.department_id = dep.department_id;

-- 4. Join with placement cell
SELECT p.name AS coordinator_name, dep.department_name
FROM placement_cell p
JOIN departments dep ON p.department_id = dep.department_id;

-- 5. Subquery: students having pending documents
SELECT prn, name
FROM students
WHERE prn IN (
    SELECT uploaded_by_prn
    FROM documents
    WHERE status = 'Pending' AND uploaded_by_prn IS NOT NULL
);

-- 6. Subquery: departments with more than 1 document
SELECT department_name
FROM departments
WHERE department_id IN (
    SELECT department_id
    FROM documents
    GROUP BY department_id
    HAVING COUNT(*) > 1
);

-- 7. Group by: number of documents by category
SELECT category, COUNT(*) AS total_documents
FROM documents
GROUP BY category;

-- 8. Group by + having: students with more than 2 uploaded documents
SELECT uploaded_by_prn, COUNT(*) AS document_count
FROM documents
WHERE uploaded_by_prn IS NOT NULL
GROUP BY uploaded_by_prn
HAVING COUNT(*) > 2;

-- 9. Correlated subquery: highest document count student
SELECT s.prn, s.name
FROM students s
WHERE (
    SELECT COUNT(*)
    FROM documents d
    WHERE d.uploaded_by_prn = s.prn
) = (
    SELECT MAX(doc_count)
    FROM (
        SELECT COUNT(*) AS doc_count
        FROM documents
        WHERE uploaded_by_prn IS NOT NULL
        GROUP BY uploaded_by_prn
    ) AS counts
);

-- 10. Use view to show student document dashboard
SELECT *
FROM vw_student_documents
WHERE status = 'Pending';

-- 11. Join notifications with students and documents
SELECT n.notification_id, s.name AS student_name, d.document_name, n.message
FROM notifications n
JOIN students s ON n.prn = s.prn
LEFT JOIN documents d ON n.document_id = d.document_id;

-- 12. Self-contained report using join + aggregate
SELECT dep.department_name, COUNT(d.document_id) AS total_docs, SUM(d.status = 'Pending') AS pending_docs
FROM departments dep
LEFT JOIN documents d ON dep.department_id = d.department_id
GROUP BY dep.department_name
HAVING COUNT(d.document_id) >= 1;
