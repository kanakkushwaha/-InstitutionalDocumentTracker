USE institutional_document_tracker;

DELIMITER $$

CREATE FUNCTION fn_pending_documents_by_department(p_department_id INT)
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE v_count INT;
    SELECT COUNT(*)
    INTO v_count
    FROM documents
    WHERE department_id = p_department_id
      AND status = 'Pending';
    RETURN v_count;
END $$

CREATE FUNCTION fn_student_document_count(p_prn VARCHAR(30))
RETURNS INT
DETERMINISTIC
BEGIN
    DECLARE v_count INT;
    SELECT COUNT(*)
    INTO v_count
    FROM documents
    WHERE uploaded_by_prn = p_prn;
    RETURN v_count;
END $$

CREATE PROCEDURE sp_add_student (
    IN p_prn VARCHAR(30),
    IN p_name VARCHAR(120),
    IN p_class VARCHAR(50),
    IN p_email VARCHAR(120),
    IN p_contact VARCHAR(20),
    IN p_department_id INT,
    IN p_current_year VARCHAR(30),
    IN p_password VARCHAR(120)
)
BEGIN
    INSERT INTO students (prn, name, class, email_id, contact_number, department_id, current_year, password)
    VALUES (p_prn, p_name, p_class, p_email, p_contact, p_department_id, p_current_year, p_password);
END $$

CREATE PROCEDURE sp_review_document (
    IN p_document_id INT,
    IN p_new_status VARCHAR(40),
    IN p_message TEXT
)
BEGIN
    UPDATE documents
    SET status = p_new_status,
        review_message = p_message
    WHERE document_id = p_document_id;
END $$

CREATE PROCEDURE sp_department_document_summary(IN p_department_id INT)
BEGIN
    SELECT
        dep.department_name,
        COUNT(d.document_id) AS total_documents,
        SUM(d.status = 'Approved') AS approved_documents,
        SUM(d.status = 'Pending') AS pending_documents
    FROM departments dep
    LEFT JOIN documents d ON dep.department_id = d.department_id
    WHERE dep.department_id = p_department_id
    GROUP BY dep.department_name;
END $$

DELIMITER ;

-- Sample calls
-- SELECT fn_pending_documents_by_department(1);
-- SELECT fn_student_document_count('2022CE041');
-- CALL sp_add_student('2025CE100', 'Test Student', 'FE Computer', 'test@institution.edu', '9000000012', 1, '1st Year BTech', 'pass123');
-- CALL sp_review_document(1, 'Approved', 'Document verified successfully.');
-- CALL sp_department_document_summary(1);
