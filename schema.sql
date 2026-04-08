CREATE DATABASE IF NOT EXISTS institutional_document_tracker;
USE institutional_document_tracker;

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
    FOREIGN KEY (department_id) REFERENCES departments(department_id)
        ON DELETE SET NULL,
    FOREIGN KEY (uploaded_by_prn) REFERENCES students(prn)
        ON DELETE CASCADE,
    FOREIGN KEY (uploaded_by_teacherid) REFERENCES teachers(teacher_id)
        ON DELETE CASCADE
);
