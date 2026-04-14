USE institutional_document_tracker;

INSERT INTO departments (department_name) VALUES
('Computer Engineering'),
('Placement Cell'),
('Scholarship Cell'),
('Information Technology');

INSERT INTO admin (name, role, email_id, contact_number, department_id) VALUES
('Aarav Sharma', 'System Admin', 'aarav.sharma@pccoepune.org', '9988776655',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'));

INSERT INTO placement_cell (name, role, email_id, contact_number, department_id) VALUES
('Kabir Malhotra', 'Placement Coordinator', 'kabir.malhotra@pccoepune.org', '9820012345',
    (SELECT department_id FROM departments WHERE department_name = 'Placement Cell'));

INSERT INTO scholarship_cell (name, role, email_id, contact_number, department_id) VALUES
('Neha Karmarkar', 'Scholarship Coordinator', 'neha.karmarkar@pccoepune.org', '9833301122',
    (SELECT department_id FROM departments WHERE department_name = 'Scholarship Cell'));

INSERT INTO teachers (name, email_id, contact_number, department_id, role, password) VALUES
('Prof. Meera Singh', 'meera.singh@pccoepune.org', '9911223344',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    'Teacher', 'Staff@123'),
('Prof. Kabir Jain', 'kabir.jain@pccoepune.org', '9876543211',
    (SELECT department_id FROM departments WHERE department_name = 'Information Technology'),
    'Teacher', 'Staff@123');

INSERT INTO students (prn, name, class, email_id, contact_number, department_id, current_year, password) VALUES
('124B1F095', 'Kanak Kushwaha', 'SY', 'kanak.kushwaha24@pccoepune.org', '9898989898',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    '2nd Year BTech', 'PCCOE@123'),
('123B1F106', 'Riya Patel', 'TY', 'riya.patel23@pccoepune.org', '9870011223',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    '3rd Year BTech', 'PCCOE@123'),
('124B1I120', 'Rhea Naidu', 'SY', 'rhea.naidu24@pccoepune.org', '9870011224',
    (SELECT department_id FROM departments WHERE department_name = 'Information Technology'),
    '2nd Year BTech', 'PCCOE@123');

INSERT INTO documents (
    document_name,
    document_image,
    category,
    department_id,
    status,
    review_message,
    uploaded_by_prn,
    uploaded_by_teacherid
) VALUES
('10th Marksheet', 'app/static/uploads/10th-marksheet.pdf', 'Academic',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    'Approved', 'Verified and matched with admission records.',
    '124B1F095', NULL),

('12th Marksheet', 'app/static/uploads/12th-marksheet.pdf', 'Academic',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    'Pending', 'Upload a clearer scan with visible board stamp.',
    '124B1F095', NULL),

('Leaving Certificate', 'app/static/uploads/leaving-certificate.pdf', 'Academic',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    'Approved', 'Accepted by the admin office.',
    '124B1F095', NULL),

('First Year Marksheet', NULL, 'Academic',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    'Not Uploaded', 'Upload this document to start verification.',
    '2024CE052', NULL),

('Second Year Marksheet', NULL, 'Academic',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    'Not Uploaded', 'Required according to current academic year.',
    '2024CE052', NULL),

('Placement Resume', 'app/static/uploads/riya-placement-resume.pdf', 'Placement',
    (SELECT department_id FROM departments WHERE department_name = 'Placement Cell'),
    'Pending', 'Please update your resume headline and skills section.',
    '123B1F106', NULL),

('GitHub Profile Link', 'https://github.com/riya-patel-dev', 'Placement',
    (SELECT department_id FROM departments WHERE department_name = 'Placement Cell'),
    'Approved', 'Profile reviewed and accepted by placement mentor.',
    '123B1F106', NULL),

('LinkedIn Profile Link', 'https://www.linkedin.com/in/riya-patel-dev', 'Placement',
    (SELECT department_id FROM departments WHERE department_name = 'Placement Cell'),
    'Pending', 'Please add headline, skills and latest projects before final review.',
    '123B1F106', NULL),

('Portfolio / Other Professional Link', 'https://riya-patel-portfolio.example.com', 'Placement',
    (SELECT department_id FROM departments WHERE department_name = 'Placement Cell'),
    'Pending', 'Portfolio can be added with project screenshots and contact section.',
    '123B1F106', NULL),

('Placement Offer Letter', 'app/static/uploads/placement-offer-letter.pdf', 'Placement',
    (SELECT department_id FROM departments WHERE department_name = 'Placement Cell'),
    'Pending', 'Add the company seal and signed first page.',
    '123B1F106', NULL),

('Scholarship Form', 'app/static/uploads/scholarship-form-2026.pdf', 'Scholarship',
    (SELECT department_id FROM departments WHERE department_name = 'Scholarship Cell'),
    'Pending', 'Fee receipt still under verification.',
    '124B1I120', NULL),

('Fee Receipt', 'app/static/uploads/fee-receipt.jpg', 'Finance',
    (SELECT department_id FROM departments WHERE department_name = 'Scholarship Cell'),
    'Approved', 'Payment proof confirmed.',
    '124B1I120', NULL),

('Department Report', 'app/static/uploads/department-report-cse-april.pdf', 'Department',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    'Approved', 'Shared with admin dashboard.',
    NULL, (SELECT teacher_id FROM teachers WHERE email_id = 'meera.singh@pccoepune.org')),

('Attendance Sheet', 'app/static/uploads/attendance-sheet.pdf', 'Academic',
    (SELECT department_id FROM departments WHERE department_name = 'Computer Engineering'),
    'Pending', 'Teacher should upload latest monthly attendance.',
    NULL, (SELECT teacher_id FROM teachers WHERE email_id = 'meera.singh@pccoepune.org'));
