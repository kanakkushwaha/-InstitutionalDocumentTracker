from datetime import date


DEMO_DOCUMENTS = [
    {
        "id": "DOC-1001",
        "name": "Semester 5 Marksheet",
        "file_name": "semester-5-marksheet.pdf",
        "file_type": "PDF",
        "owner": "Riya Patel",
        "role": "student",
        "department": "Computer Engineering",
        "category": "Academic",
        "status": "Approved",
        "submitted_on": "2026-04-02",
        "preview_text": "Official semester marksheet containing SGPA, subject breakdown and academic verification stamp.",
    },
    {
        "id": "DOC-1002",
        "name": "Placement Resume",
        "file_name": "riya-placement-resume.pdf",
        "file_type": "PDF",
        "owner": "Riya Patel",
        "role": "student",
        "department": "Computer Engineering",
        "category": "Placement",
        "status": "Pending",
        "submitted_on": "2026-04-06",
        "preview_text": "Placement resume highlighting projects, technical skills, internships and coding achievements.",
    },
    {
        "id": "DOC-1003",
        "name": "Scholarship Form",
        "file_name": "scholarship-form-2026.pdf",
        "file_type": "PDF",
        "owner": "Aditya Nair",
        "role": "student",
        "department": "IT",
        "category": "Scholarship",
        "status": "Pending",
        "submitted_on": "2026-04-05",
        "preview_text": "Scholarship application form with personal details, income declaration and required attachments.",
    },
    {
        "id": "DOC-1004",
        "name": "Department Report",
        "file_name": "department-report-cse-april.pdf",
        "file_type": "PDF",
        "owner": "Dr. Meera Singh",
        "role": "teacher",
        "department": "Computer Engineering",
        "category": "Department",
        "status": "Approved",
        "submitted_on": "2026-04-04",
        "preview_text": "Department monthly summary report covering placement readiness, document compliance and notices.",
    },
    {
        "id": "DOC-1005",
        "name": "Attendance Sheet",
        "file_name": "attendance-sheet-mech.xlsx",
        "file_type": "Excel",
        "owner": "Prof. Kabir Jain",
        "role": "teacher",
        "department": "Mechanical",
        "category": "Academic",
        "status": "Rejected",
        "submitted_on": "2026-04-01",
        "preview_text": "Attendance sheet for mechanical division with lecture-wise presence and absentee summary.",
    },
]

DEMO_USERS = {
    "admin": [
        {
            "name": "Aarav Sharma",
            "email": "admin@institution.edu",
            "role": "Admin",
            "department": "Central Administration",
            "status": "Active",
        }
    ],
    "teachers": [
        {
            "name": "Dr. Meera Singh",
            "email": "teacher@institution.edu",
            "role": "Placement Coordinator",
            "department": "Computer Engineering",
            "status": "Active",
        },
        {
            "name": "Prof. Kabir Jain",
            "email": "kabir@institution.edu",
            "role": "Scholarship Mentor",
            "department": "Mechanical",
            "status": "Reviewing 18 docs",
        },
    ],
    "students": [
        {
            "name": "Riya Patel",
            "email": "student@institution.edu",
            "role": "Final Year Student",
            "department": "Computer Engineering",
            "status": "Placement Ready",
            "prn": "2022CE041",
        },
        {
            "name": "Aditya Nair",
            "email": "aditya@institution.edu",
            "role": "Third Year Student",
            "department": "IT",
            "status": "Scholarship Pending",
            "prn": "2023IT018",
        },
        {
            "name": "Sneha Deshmukh",
            "email": "sneha@institution.edu",
            "role": "Second Year Student",
            "department": "Mechanical",
            "status": "Docs Complete",
            "prn": "2024ME022",
        },
    ],
}

DEMO_DEPARTMENTS = [
    {
        "name": "Placement Cell",
        "lead": "Dr. Meera Singh",
        "pending": 12,
        "approved": 84,
        "theme": "sunrise",
    },
    {
        "name": "Scholarship Cell",
        "lead": "Prof. Kabir Jain",
        "pending": 9,
        "approved": 63,
        "theme": "aqua",
    },
    {
        "name": "Computer Engineering",
        "lead": "Aarav Sharma",
        "pending": 17,
        "approved": 121,
        "theme": "berry",
    },
]

DEMO_ACTIVITY = [
    "Admin approved 14 academic records this week.",
    "Placement cell requested 6 fresh resumes for campus drive.",
    "Scholarship desk flagged 3 incomplete fee receipts.",
    "Teacher upload traffic increased by 22 percent today.",
]

STUDENT_REQUIREMENTS = [
    {"title": "Marksheet", "category": "Academic", "formats": "PDF / JPG", "status": "Approved"},
    {"title": "Aadhaar or PAN", "category": "ID Proof", "formats": "PDF / JPG", "status": "Pending"},
    {"title": "College ID", "category": "Identity", "formats": "JPG / PNG", "status": "Approved"},
    {"title": "Resume", "category": "Placement", "formats": "PDF", "status": "Pending"},
    {"title": "Scholarship Form", "category": "Scholarship", "formats": "PDF", "status": "Pending"},
    {"title": "Bonafide Certificate", "category": "Academic", "formats": "PDF", "status": "Missing"},
    {"title": "Fee Receipt", "category": "Finance", "formats": "PDF / JPG", "status": "Approved"},
]


def get_dashboard_payload():
    pending = sum(1 for doc in DEMO_DOCUMENTS if doc["status"] == "Pending")
    approved = sum(1 for doc in DEMO_DOCUMENTS if doc["status"] == "Approved")
    rejected = sum(1 for doc in DEMO_DOCUMENTS if doc["status"] == "Rejected")
    return {
        "stats": [
            {
                "label": "Total Users",
                "value": len(DEMO_USERS["admin"]) + len(DEMO_USERS["teachers"]) + len(DEMO_USERS["students"]),
                "detail": "Students, teachers and admins",
            },
            {
                "label": "Documents Uploaded",
                "value": len(DEMO_DOCUMENTS),
                "detail": "Academic, placement, scholarship",
            },
            {
                "label": "Pending Approvals",
                "value": pending,
                "detail": "Needs admin review",
            },
            {
                "label": "Approval Rate",
                "value": f"{round((approved / len(DEMO_DOCUMENTS)) * 100)}%",
                "detail": f"{rejected} recently rejected",
            },
        ],
        "documents": DEMO_DOCUMENTS,
        "departments": DEMO_DEPARTMENTS,
        "activity": DEMO_ACTIVITY,
        "generated_on": date.today().isoformat(),
    }


def get_student_payload():
    student = DEMO_USERS["students"][0]
    my_docs = [doc for doc in DEMO_DOCUMENTS if doc["owner"] == student["name"]]
    approved = sum(1 for doc in my_docs if doc["status"] == "Approved")
    pending = sum(1 for doc in my_docs if doc["status"] == "Pending")
    completion = round((sum(1 for item in STUDENT_REQUIREMENTS if item["status"] == "Approved") / len(STUDENT_REQUIREMENTS)) * 100)
    return {
        "student": student,
        "my_docs": my_docs,
        "requirements": STUDENT_REQUIREMENTS,
        "highlights": [
            {"label": "Profile Completion", "value": f"{completion}%", "detail": "Documents and personal data"},
            {"label": "Approved Docs", "value": approved, "detail": "Ready for verification"},
            {"label": "Pending Review", "value": pending, "detail": "Awaiting teacher/admin action"},
            {"label": "Placement Readiness", "value": "86%", "detail": "Resume plus academic stack"},
        ],
        "timeline": [
            {"title": "Resume uploaded", "date": "06 Apr 2026", "note": "Sent to placement cell"},
            {"title": "Marksheet approved", "date": "02 Apr 2026", "note": "Academic verification completed"},
            {"title": "Scholarship form submitted", "date": "05 Apr 2026", "note": "Pending finance review"},
        ],
        "focus_cards": [
            {"title": "Placement Pack", "body": "Resume, marksheet and ID proof for upcoming drives."},
            {"title": "Scholarship Ready", "body": "Track fee receipt, bonafide and form approval in one view."},
            {"title": "Academic Vault", "body": "Keep all semester and identity records safe and searchable."},
        ],
    }


def get_document_by_id(doc_id):
    return next((doc for doc in DEMO_DOCUMENTS if doc["id"] == doc_id), None)
