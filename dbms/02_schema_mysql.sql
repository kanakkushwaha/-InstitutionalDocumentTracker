CREATE DATABASE IF NOT EXISTS institutional_document_tracker;
USE institutional_document_tracker;

DROP TABLE IF EXISTS document_audit;
DROP TABLE IF EXISTS notifications;
DROP TABLE IF EXISTS documents;
DROP TABLE IF EXISTS teachers;
DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS scholarship_cell;
DROP TABLE IF EXISTS placement_cell;
DROP TABLE IF EXISTS admin;
DROP TABLE IF EXISTS departments;

CREATE TABLE departments (
    department_id INT AUTO_INCREMENT PRIMARY KEY,
    department_name VARCHAR(120) NOT NULL UNIQUE
);

CREATE TABLE admin (
    admin_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    role VARCHAR(50) NOT NULL,
    email_id VARCHAR(120) NOT NULL UNIQUE,
    contact_number VARCHAR(20) NOT NULL,
    department_id INT,
    CONSTRAINT fk_admin_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL
);

CREATE TABLE placement_cell (
    placement_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    role VARCHAR(50) NOT NULL,
    email_id VARCHAR(120) NOT NULL UNIQUE,
    contact_number VARCHAR(20) NOT NULL,
    department_id INT,
    CONSTRAINT fk_placement_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL
);

CREATE TABLE scholarship_cell (
    scholarship_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    role VARCHAR(50) NOT NULL,
    email_id VARCHAR(120) NOT NULL UNIQUE,
    contact_number VARCHAR(20) NOT NULL,
    department_id INT,
    CONSTRAINT fk_scholarship_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL
);

CREATE TABLE students (
    prn VARCHAR(30) PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    class VARCHAR(50) NOT NULL,
    email_id VARCHAR(120) NOT NULL UNIQUE,
    contact_number VARCHAR(20) NOT NULL,
    department_id INT,
    current_year VARCHAR(30),
    password VARCHAR(120),
    CONSTRAINT fk_students_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL
);

CREATE TABLE teachers (
    teacher_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(120) NOT NULL,
    email_id VARCHAR(120) NOT NULL UNIQUE,
    contact_number VARCHAR(20) NOT NULL,
    department_id INT,
    role VARCHAR(50),
    password VARCHAR(120),
    CONSTRAINT fk_teachers_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL
);

CREATE TABLE documents (
    document_id INT AUTO_INCREMENT PRIMARY KEY,
    document_name VARCHAR(150) NOT NULL,
    document_image VARCHAR(255),
    category VARCHAR(80),
    department_id INT,
    status VARCHAR(40) DEFAULT 'Pending',
    review_message TEXT,
    uploaded_by_prn VARCHAR(30),
    uploaded_by_teacherid INT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    CONSTRAINT fk_documents_department
        FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL,
    CONSTRAINT fk_documents_student
        FOREIGN KEY (uploaded_by_prn) REFERENCES students(prn)
        ON DELETE CASCADE,
    CONSTRAINT fk_documents_teacher
        FOREIGN KEY (uploaded_by_teacherid) REFERENCES teachers(teacher_id)
        ON DELETE CASCADE,
    CONSTRAINT chk_document_uploader
        CHECK (
            (uploaded_by_prn IS NOT NULL AND uploaded_by_teacherid IS NULL)
            OR (uploaded_by_prn IS NULL AND uploaded_by_teacherid IS NOT NULL)
        )
);

CREATE TABLE notifications (
    notification_id INT AUTO_INCREMENT PRIMARY KEY,
    prn VARCHAR(30) NOT NULL,
    document_id INT,
    message TEXT NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_notifications_student
        FOREIGN KEY (prn) REFERENCES students(prn)
        ON DELETE CASCADE,
    CONSTRAINT fk_notifications_document
        FOREIGN KEY (document_id) REFERENCES documents(document_id)
        ON DELETE SET NULL
);

CREATE TABLE document_audit (
    audit_id INT AUTO_INCREMENT PRIMARY KEY,
    document_id INT,
    action_type VARCHAR(30) NOT NULL,
    old_status VARCHAR(40),
    new_status VARCHAR(40),
    changed_on DATETIME DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_students_department ON students(department_id);
CREATE INDEX idx_teachers_department ON teachers(department_id);
CREATE INDEX idx_documents_status ON documents(status);
CREATE INDEX idx_documents_category ON documents(category);
CREATE INDEX idx_documents_student ON documents(uploaded_by_prn);
CREATE INDEX idx_documents_teacher ON documents(uploaded_by_teacherid);
CREATE INDEX idx_notifications_prn ON notifications(prn);
