# Institutional Document Tracker

## 1. Problem Statement

The Institutional Document Tracker System is developed to manage and track academic, placement, scholarship, and administrative documents inside a college. The system connects Students, Teachers, Admin, Placement Cell, Scholarship Cell, and Departments so that documents can be uploaded, reviewed, approved, rejected, and monitored digitally.

The main problems solved by this system are:

- manual paperwork and document loss
- no centralized record for students and teachers
- difficulty in monitoring placement and scholarship documents
- delay in verification and communication between departments
- lack of transparency in document review status

## 2. Conceptual Design Using ER Modeling

### Main Entities

1. `DEPARTMENTS`
   Attributes:
   - `Department_ID` (Primary Key)
   - `Department_Name`

2. `ADMIN`
   Attributes:
   - `Admin_ID` (Primary Key)
   - `Name`
   - `Role`
   - `Email_ID`
   - `Contact_Number`
   - `Department_ID` (Foreign Key)

3. `PLACEMENT_CELL`
   Attributes:
   - `Placement_ID` (Primary Key)
   - `Name`
   - `Role`
   - `Email_ID`
   - `Contact_Number`
   - `Department_ID` (Foreign Key)

4. `SCHOLARSHIP_CELL`
   Attributes:
   - `Scholarship_ID` (Primary Key)
   - `Name`
   - `Role`
   - `Email_ID`
   - `Contact_Number`
   - `Department_ID` (Foreign Key)

5. `STUDENTS`
   Attributes:
   - `PRN` (Primary Key)
   - `Name`
   - `Class`
   - `Email_ID`
   - `Contact_Number`
   - `Department_ID` (Foreign Key)
   - `Current_Year`
   - `Password`

6. `TEACHERS`
   Attributes:
   - `Teacher_ID` (Primary Key)
   - `Name`
   - `Email_ID`
   - `Contact_Number`
   - `Department_ID` (Foreign Key)
   - `Role`
   - `Password`

7. `DOCUMENTS`
   Attributes:
   - `Document_ID` (Primary Key)
   - `Document_Name`
   - `Document_Image`
   - `Category`
   - `Department_ID` (Foreign Key)
   - `Status`
   - `Review_Message`
   - `Uploaded_By_PRN` (Foreign Key)
   - `Uploaded_By_TeacherID` (Foreign Key)
   - `Created_At`
   - `Updated_At`

8. `NOTIFICATIONS`
   Attributes:
   - `Notification_ID` (Primary Key)
   - `PRN` (Foreign Key)
   - `Document_ID` (Foreign Key)
   - `Message`
   - `Created_At`

9. `DOCUMENT_AUDIT`
   Attributes:
   - `Audit_ID` (Primary Key)
   - `Document_ID`
   - `Action_Type`
   - `Old_Status`
   - `New_Status`
   - `Changed_On`

### Relationships

1. One `DEPARTMENT` can have many `STUDENTS`
   Cardinality:
   - Department `1 : N` Students

2. One `DEPARTMENT` can have many `TEACHERS`
   Cardinality:
   - Department `1 : N` Teachers

3. One `DEPARTMENT` can be linked with one or more `ADMIN`, `PLACEMENT_CELL`, and `SCHOLARSHIP_CELL` records

4. One `STUDENT` can upload many `DOCUMENTS`
   Cardinality:
   - Student `1 : N` Documents

5. One `TEACHER` can upload many `DOCUMENTS`
   Cardinality:
   - Teacher `1 : N` Documents

6. One `DOCUMENT` belongs to one `DEPARTMENT`
   Cardinality:
   - Department `1 : N` Documents

7. One `STUDENT` can receive many `NOTIFICATIONS`
   Cardinality:
   - Student `1 : N` Notifications

### Generalization / Specialization

The system conceptually treats `Admin`, `Teacher`, `Placement Cell`, and `Scholarship Cell` as specialized roles working with institutional documents. In implementation for DBMS presentation, these are shown as separate entities to clearly represent responsibilities and relationships.

## 3. Conversion of ER Model to Relational Model

The ER model is converted into the following relational tables:

- `departments(department_id, department_name)`
- `admin(admin_id, name, role, email_id, contact_number, department_id)`
- `placement_cell(placement_id, name, role, email_id, contact_number, department_id)`
- `scholarship_cell(scholarship_id, name, role, email_id, contact_number, department_id)`
- `students(prn, name, class, email_id, contact_number, department_id, current_year, password)`
- `teachers(teacher_id, name, email_id, contact_number, department_id, role, password)`
- `documents(document_id, document_name, document_image, category, department_id, status, review_message, uploaded_by_prn, uploaded_by_teacherid, created_at, updated_at)`
- `notifications(notification_id, prn, document_id, message, created_at)`
- `document_audit(audit_id, document_id, action_type, old_status, new_status, changed_on)`

## 4. Normalization

### First Normal Form (1NF)

- All tables have atomic values.
- No repeating groups are stored inside a single column.
- Each row is uniquely identified by a primary key.

### Second Normal Form (2NF)

- All non-key attributes are fully dependent on the primary key.
- Example:
  In `documents`, fields such as `document_name`, `status`, and `review_message` depend completely on `document_id`.

### Third Normal Form (3NF)

- Transitive dependency is removed.
- Department details are stored in `departments` instead of repeating inside `students`, `teachers`, and `documents`.
- Admin, Placement Cell, and Scholarship Cell contact information is stored separately instead of mixing it with student or teacher tables.

### BCNF

- Every determinant is a candidate key or primary key in the core relations.
- This improves consistency and avoids redundancy in document and user data.

## 5. Why This Design Is Good

- It reduces data redundancy.
- It supports document monitoring by both teachers and admin.
- It keeps review messages and notifications structured.
- It is suitable for academic DBMS demonstration and real web application extension.
