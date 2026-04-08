from pathlib import Path

from app import db
from app.models import Department, Document, User
from app.workbench_sync import ensure_workbench_tables, reset_workbench_sync_cache, sync_workbench_user

STUDENT_ACCOUNT_DATA = [
    ("Aarohi Patil", "student.2025ce001@institution.edu", "stu-2025ce001", "2025CE001", "Computer Engineering"),
    ("Vivaan Shah", "student.2025ce002@institution.edu", "stu-2025ce002", "2025CE002", "Computer Engineering"),
    ("Ishita Nair", "student.2025ce003@institution.edu", "stu-2025ce003", "2025CE003", "Computer Engineering"),
    ("Parth Jadhav", "student.2025ce004@institution.edu", "stu-2025ce004", "2025CE004", "Computer Engineering"),
    ("Nehal More", "student.2025ce005@institution.edu", "stu-2025ce005", "2025CE005", "Computer Engineering"),
    ("Tanvi Kulkarni", "student.2025it006@institution.edu", "stu-2025it006", "2025IT006", "Information Technology"),
    ("Rudra Sawant", "student.2025it007@institution.edu", "stu-2025it007", "2025IT007", "Information Technology"),
    ("Mitali Shinde", "student.2025it008@institution.edu", "stu-2025it008", "2025IT008", "Information Technology"),
    ("Harsh Desai", "student.2025it009@institution.edu", "stu-2025it009", "2025IT009", "Information Technology"),
    ("Kashish Yadav", "student.2025it010@institution.edu", "stu-2025it010", "2025IT010", "Information Technology"),
    ("Pranav Joshi", "student.2024ce011@institution.edu", "stu-2024ce011", "2024CE011", "Computer Engineering"),
    ("Diya Sharma", "student.2024ce012@institution.edu", "stu-2024ce012", "2024CE012", "Computer Engineering"),
    ("Saket Verma", "student.2024ce013@institution.edu", "stu-2024ce013", "2024CE013", "Computer Engineering"),
    ("Anvi Gupta", "student.2024ce014@institution.edu", "stu-2024ce014", "2024CE014", "Computer Engineering"),
    ("Kunal Patwardhan", "student.2024ce015@institution.edu", "stu-2024ce015", "2024CE015", "Computer Engineering"),
    ("Rhea Naidu", "student.2024it016@institution.edu", "stu-2024it016", "2024IT016", "Information Technology"),
    ("Atharv Kale", "student.2024it017@institution.edu", "stu-2024it017", "2024IT017", "Information Technology"),
    ("Pallavi Mane", "student.2024it018@institution.edu", "stu-2024it018", "2024IT018", "Information Technology"),
    ("Yash Khanna", "student.2024it019@institution.edu", "stu-2024it019", "2024IT019", "Information Technology"),
    ("Saanvi Salunke", "student.2024it020@institution.edu", "stu-2024it020", "2024IT020", "Information Technology"),
]

TEACHER_ACCOUNT_DATA = [
    "meera",
    "kabir",
    "anjali",
    "rohan",
    "nisha",
    "arpit",
    "sonal",
    "vikram",
    "neha",
    "rahul",
    "priya",
    "abhay",
    "pooja",
    "samir",
    "kiran",
    "monal",
    "deepak",
    "shruti",
    "amit",
    "rutuja",
]

ADMIN_ACCOUNT_DATA = [
    "aarav",
    "kanak",
    "riya",
    "aditya",
    "sneha",
    "rohit",
    "pooja",
    "neha",
    "vishal",
    "anjali",
    "kabir",
    "meera",
    "rohan",
    "sonal",
    "abhay",
    "priya",
    "shruti",
    "deepak",
    "rutuja",
    "amit",
]

PLACEMENT_ACCOUNT_DATA = [
    ("Kabir Malhotra", "placement.kabir@institution.edu", "place-kabir1"),
    ("Sonal Verma", "placement.sonal@institution.edu", "place-sonal1"),
]

SCHOLARSHIP_ACCOUNT_DATA = [
    ("Neha Joshi", "scholarship.neha@institution.edu", "schol-neha1"),
    ("Priya Nair", "scholarship.priya@institution.edu", "schol-priya1"),
]

SEED_DEPARTMENTS = [
    {
        "name": "Computer Engineering",
        "category": "Academic",
        "contact_email": "ce@institution.edu",
        "contact_number": "9876543210",
    },
    {
        "name": "Information Technology",
        "category": "Academic",
        "contact_email": "it@institution.edu",
        "contact_number": "9876543211",
    },
    {
        "name": "Placement Cell",
        "category": "Placement",
        "contact_email": "placement@institution.edu",
        "contact_number": "9820012345",
    },
    {
        "name": "Scholarship Cell",
        "category": "Scholarship",
        "contact_email": "scholarship@institution.edu",
        "contact_number": "9833301122",
    },
    {
        "name": "Administration",
        "category": "Administrative",
        "contact_email": "admin.office@institution.edu",
        "contact_number": "9811101101",
    },
]


def _format_name(name):
    return " ".join(part.capitalize() for part in name.split("."))


def _contact_number(seed_number):
    return f"98{seed_number:08d}"


def _build_seed_users():
    users = []

    for index, (name, email, password, prn, department) in enumerate(STUDENT_ACCOUNT_DATA, start=1):
        users.append(
            {
                "name": name,
                "email": email,
                "password": password,
                "role": "student",
                "department": department,
                "prn": prn,
                "contact_number": _contact_number(index),
            }
        )

    for index, name in enumerate(TEACHER_ACCOUNT_DATA, start=101):
        department = "Computer Engineering" if index % 2 else "Information Technology"
        users.append(
            {
                "name": f"Prof. {_format_name(name)}",
                "email": f"teacher.{name}@institution.edu",
                "password": f"teach-{name}1",
                "role": "teacher",
                "department": department,
                "contact_number": _contact_number(index),
            }
        )

    for index, name in enumerate(ADMIN_ACCOUNT_DATA, start=201):
        users.append(
            {
                "name": f"{_format_name(name)} Admin",
                "email": f"admin.{name}@institution.edu",
                "password": f"admin-{name}1",
                "role": "admin",
                "department": "Administration",
                "contact_number": _contact_number(index),
            }
        )

    for index, (name, email, password) in enumerate(PLACEMENT_ACCOUNT_DATA, start=301):
        users.append(
            {
                "name": name,
                "email": email,
                "password": password,
                "role": "placement",
                "department": "Placement Cell",
                "contact_number": _contact_number(index),
            }
        )

    for index, (name, email, password) in enumerate(SCHOLARSHIP_ACCOUNT_DATA, start=401):
        users.append(
            {
                "name": name,
                "email": email,
                "password": password,
                "role": "scholarship",
                "department": "Scholarship Cell",
                "contact_number": _contact_number(index),
            }
        )

    return users


SEED_USERS = _build_seed_users()

LOGIN_DEMO_USERS = [
    {"role": "student", "email": "student.2025ce001@institution.edu", "password": "stu-2025ce001"},
    {"role": "teacher", "email": "teacher.meera@institution.edu", "password": "teach-meera1"},
    {"role": "admin", "email": "admin.aarav@institution.edu", "password": "admin-aarav1"},
    {"role": "placement", "email": "placement.kabir@institution.edu", "password": "place-kabir1"},
    {"role": "scholarship", "email": "scholarship.neha@institution.edu", "password": "schol-neha1"},
]

SEED_DOCUMENTS = [
    {
        "title": "10th Marksheet",
        "category": "Academic",
        "file_name": "10th-marksheet.pdf",
        "file_type": "PDF",
        "description": "Secondary school marksheet for educational record verification.",
        "status": "Approved",
        "owner_email": "student.2025ce001@institution.edu",
        "department": "Computer Engineering",
        "remarks": "Verified and matched with admission records.",
    },
    {
        "title": "12th Marksheet",
        "category": "Academic",
        "file_name": "12th-marksheet.pdf",
        "file_type": "PDF",
        "description": "Higher secondary marksheet required for student profile completion.",
        "status": "Pending",
        "owner_email": "student.2025ce001@institution.edu",
        "department": "Computer Engineering",
        "remarks": "Upload a clearer scan with visible board stamp.",
    },
    {
        "title": "Leaving Certificate",
        "category": "Academic",
        "file_name": "leaving-certificate.pdf",
        "file_type": "PDF",
        "description": "Leaving certificate for previous institution transfer record.",
        "status": "Approved",
        "owner_email": "student.2025ce001@institution.edu",
        "department": "Computer Engineering",
        "remarks": "Accepted by the admin office.",
    },
    {
        "title": "Semester 5 Marksheet",
        "category": "Academic",
        "file_name": "semester-5-marksheet.pdf",
        "file_type": "PDF",
        "description": "Semester marksheet with SGPA, subject grades and academic stamp.",
        "status": "Approved",
        "owner_email": "student.2024ce011@institution.edu",
        "department": "Computer Engineering",
        "remarks": "Verified by academic office.",
    },
    {
        "title": "Aadhaar Card",
        "category": "ID Proof",
        "file_name": "aadhaar-card.pdf",
        "file_type": "PDF",
        "description": "Government identity document uploaded for verification and record linking.",
        "status": "Approved",
        "owner_email": "student.2025ce001@institution.edu",
        "department": "Computer Engineering",
        "remarks": "Identity proof accepted.",
    },
    {
        "title": "College ID Card",
        "category": "ID Proof",
        "file_name": "college-id-card.png",
        "file_type": "PNG",
        "description": "Current college identity card for campus verification.",
        "status": "Approved",
        "owner_email": "student.2025ce001@institution.edu",
        "department": "Computer Engineering",
        "remarks": "Card image verified successfully.",
    },
    {
        "title": "PAN Card",
        "category": "ID Proof",
        "file_name": "pan-card.pdf",
        "file_type": "PDF",
        "description": "PAN card used for scholarship and financial verification.",
        "status": "Pending",
        "owner_email": "student.2024it016@institution.edu",
        "department": "Scholarship Cell",
        "remarks": "Please upload the front side in better resolution.",
    },
    {
        "title": "Placement Resume",
        "category": "Placement",
        "file_name": "riya-placement-resume.pdf",
        "file_type": "PDF",
        "description": "Resume for campus placement drives with projects, skills and internships.",
        "status": "Pending",
        "owner_email": "student.2024ce011@institution.edu",
        "department": "Placement Cell",
        "remarks": "Awaiting placement cell review.",
    },
    {
        "title": "GitHub Profile Link",
        "category": "Placement",
        "file_name": "GitHub Profile Link",
        "file_type": "LINK",
        "description": "GitHub profile link to showcase repositories and coding work.",
        "status": "Approved",
        "owner_email": "student.2024ce011@institution.edu",
        "department": "Placement Cell",
        "remarks": "Profile reviewed and accepted by placement mentor.",
        "file_path_override": "https://github.com/riya-patel-dev",
    },
    {
        "title": "LinkedIn Profile Link",
        "category": "Placement",
        "file_name": "LinkedIn Profile Link",
        "file_type": "LINK",
        "description": "LinkedIn profile link for placement communication and recruiter outreach.",
        "status": "Pending",
        "owner_email": "student.2024ce011@institution.edu",
        "department": "Placement Cell",
        "remarks": "Please add headline, skills and latest projects before final review.",
        "file_path_override": "https://www.linkedin.com/in/riya-patel-dev",
    },
    {
        "title": "Portfolio / Other Professional Link",
        "category": "Placement",
        "file_name": "Portfolio Link",
        "file_type": "LINK",
        "description": "Portfolio or other professional link for placement evaluation.",
        "status": "Pending",
        "owner_email": "student.2024ce011@institution.edu",
        "department": "Placement Cell",
        "remarks": "Portfolio can be added with project screenshots and contact section.",
        "file_path_override": "https://riya-patel-portfolio.example.com",
    },
    {
        "title": "Placement Offer Letter",
        "category": "Placement",
        "file_name": "placement-offer-letter.pdf",
        "file_type": "PDF",
        "description": "Internship or placement offer letter for placement cell record.",
        "status": "Pending",
        "owner_email": "student.2024ce011@institution.edu",
        "department": "Placement Cell",
        "remarks": "Add the company seal and signed first page.",
    },
    {
        "title": "Scholarship Form",
        "category": "Scholarship",
        "file_name": "scholarship-form-2026.pdf",
        "file_type": "PDF",
        "description": "Scholarship application form with family income and supporting details.",
        "status": "Pending",
        "owner_email": "student.2024it016@institution.edu",
        "department": "Scholarship Cell",
        "remarks": "Fee receipt still under verification.",
    },
    {
        "title": "Fee Receipt",
        "category": "Finance",
        "file_name": "fee-receipt.jpg",
        "file_type": "JPG",
        "description": "Latest paid fee receipt for scholarship and audit purposes.",
        "status": "Approved",
        "owner_email": "student.2024it016@institution.edu",
        "department": "Scholarship Cell",
        "remarks": "Payment proof confirmed.",
    },
    {
        "title": "Department Report",
        "category": "Department",
        "file_name": "department-report-cse-april.pdf",
        "file_type": "PDF",
        "description": "Monthly department report covering student readiness and pending records.",
        "status": "Approved",
        "owner_email": "teacher.meera@institution.edu",
        "department": "Computer Engineering",
        "remarks": "Shared with admin dashboard.",
    },
]


def ensure_seed_data(app):
    with app.app_context():
        db.create_all()
        ensure_workbench_tables()
        reset_workbench_sync_cache()

        for data in SEED_DEPARTMENTS:
            department = Department.query.filter_by(name=data["name"]).first()
            if not department:
                department = Department(name=data["name"])
                db.session.add(department)
            department.category = data["category"]
            department.contact_email = data["contact_email"]
            department.contact_number = data["contact_number"]
        db.session.commit()

        for data in SEED_USERS:
            dept = Department.query.filter_by(name=data["department"]).first()
            user = User.query.filter_by(email=data["email"]).first()
            if not user:
                user = User(email=data["email"])
                db.session.add(user)
            user.name = data["name"]
            user.role = data["role"]
            user.prn = data.get("prn")
            user.contact_number = data.get("contact_number")
            user.department = dept
            user.set_password(data["password"])
            db.session.flush()
            sync_workbench_user(user)
        db.session.commit()

        upload_root = Path(app.config["UPLOAD_FOLDER"])
        upload_root.mkdir(parents=True, exist_ok=True)

        for data in SEED_DOCUMENTS:
            owner = User.query.filter_by(email=data["owner_email"]).first()
            dept = Department.query.filter_by(name=data["department"]).first()
            if not owner or not dept:
                continue

            file_path = upload_root / data["file_name"]
            if data["file_type"] != "LINK" and not file_path.exists():
                file_path.write_text(
                    "\n".join(
                        [
                            data["title"],
                            f"Owner: {owner.name}",
                            f"Department: {dept.name}",
                            f"Description: {data['description']}",
                        ]
                    ),
                    encoding="utf-8",
                )

            document = Document.query.filter_by(owner_id=owner.id, title=data["title"]).first()
            if not document:
                document = Document(title=data["title"], owner=owner)
                db.session.add(document)

            document.category = data["category"]
            document.file_name = data["file_name"]
            document.file_type = data["file_type"]
            document.file_path = data.get("file_path_override", str(file_path))
            document.description = data["description"]
            document.status = data["status"]
            document.remarks = data["remarks"]
            document.department = dept
        db.session.commit()
