USE institutional_document_tracker;

DELIMITER $$

CREATE PROCEDURE sp_process_pending_documents()
BEGIN
    DECLARE done INT DEFAULT 0;
    DECLARE v_document_id INT;
    DECLARE v_student_prn VARCHAR(30);
    DECLARE v_document_name VARCHAR(150);

    DECLARE cur_pending CURSOR FOR
        SELECT document_id, uploaded_by_prn, document_name
        FROM documents
        WHERE status = 'Pending'
          AND uploaded_by_prn IS NOT NULL;

    DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
    DECLARE EXIT HANDLER FOR SQLEXCEPTION
    BEGIN
        ROLLBACK;
        SELECT 'An exception occurred while processing pending documents.' AS error_message;
    END;

    START TRANSACTION;

    OPEN cur_pending;

    read_loop: LOOP
        FETCH cur_pending INTO v_document_id, v_student_prn, v_document_name;
        IF done = 1 THEN
            LEAVE read_loop;
        END IF;

        INSERT INTO notifications (prn, document_id, message)
        VALUES (
            v_student_prn,
            v_document_id,
            CONCAT('Pending document reminder for: ', v_document_name)
        );
    END LOOP;

    CLOSE cur_pending;
    COMMIT;
END $$

CREATE TRIGGER trg_documents_before_insert
BEFORE INSERT ON documents
FOR EACH ROW
BEGIN
    IF NEW.status IS NULL OR NEW.status = '' THEN
        SET NEW.status = 'Pending';
    END IF;
    IF NEW.review_message IS NULL OR NEW.review_message = '' THEN
        SET NEW.review_message = 'Document submitted for review.';
    END IF;
END $$

CREATE TRIGGER trg_documents_after_insert
AFTER INSERT ON documents
FOR EACH ROW
BEGIN
    IF NEW.uploaded_by_prn IS NOT NULL THEN
        INSERT INTO notifications (prn, document_id, message)
        VALUES (NEW.uploaded_by_prn, NEW.document_id, CONCAT('Document uploaded: ', NEW.document_name));
    END IF;
END $$

CREATE TRIGGER trg_documents_before_update
BEFORE UPDATE ON documents
FOR EACH ROW
BEGIN
    IF NEW.document_image <> OLD.document_image THEN
        SET NEW.updated_at = CURRENT_TIMESTAMP;
    END IF;
END $$

CREATE TRIGGER trg_documents_after_update
AFTER UPDATE ON documents
FOR EACH ROW
BEGIN
    INSERT INTO document_audit (document_id, action_type, old_status, new_status)
    VALUES (NEW.document_id, 'UPDATE', OLD.status, NEW.status);

    IF NEW.uploaded_by_prn IS NOT NULL AND (OLD.review_message <> NEW.review_message OR OLD.status <> NEW.status) THEN
        INSERT INTO notifications (prn, document_id, message)
        VALUES (
            NEW.uploaded_by_prn,
            NEW.document_id,
            CONCAT('Document review updated: ', NEW.review_message)
        );
    END IF;
END $$

CREATE TRIGGER trg_documents_before_delete
BEFORE DELETE ON documents
FOR EACH ROW
BEGIN
    INSERT INTO document_audit (document_id, action_type, old_status, new_status)
    VALUES (OLD.document_id, 'BEFORE DELETE', OLD.status, NULL);
END $$

CREATE TRIGGER trg_documents_after_delete
AFTER DELETE ON documents
FOR EACH ROW
BEGIN
    INSERT INTO document_audit (document_id, action_type, old_status, new_status)
    VALUES (OLD.document_id, 'AFTER DELETE', OLD.status, NULL);
END $$

DELIMITER ;

-- Sample call
-- CALL sp_process_pending_documents();
