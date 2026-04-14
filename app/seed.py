from pathlib import Path

from app import db
from app.models import Department, Document, User
from app.workbench_sync import ensure_workbench_tables, prune_workbench_users, reset_workbench_sync_cache, sync_workbench_user

DEFAULT_STUDENT_PASSWORD = "PCCOE@123"
DEFAULT_STAFF_PASSWORD = "Staff@123"

ACADEMIC_DEPARTMENTS = [
    {"name": "Civil Engineering", "code": "A", "contact_email": "civil@pccoepune.org"},
    {"name": "Computer Engineering", "code": "B", "contact_email": "comp@pccoepune.org"},
    {"name": "AIML", "code": "C", "contact_email": "aiml@pccoepune.org"},
    {"name": "Computer Engineering Regional", "code": "D", "contact_email": "comp.regional@pccoepune.org"},
    {"name": "ENTC", "code": "E", "contact_email": "entc@pccoepune.org"},
    {"name": "Information Technology", "code": "F", "contact_email": "it@pccoepune.org"},
    {"name": "Mechanical Engineering", "code": "G", "contact_email": "mech@pccoepune.org"},
]

STUDENT_FIRST_NAMES = [
    "Kanak", "Aarohi", "Vivaan", "Ishita", "Parth", "Nehal", "Pranav", "Diya", "Saket", "Anvi",
    "Kunal", "Riya", "Aditya", "Sneha", "Rahul", "Aman", "Sharvari", "Tanmay", "Mitali", "Yash",
]

STUDENT_LAST_NAMES = [
    "Kushwaha", "Patil", "Shah", "Nair", "Jadhav", "More", "Joshi", "Sharma", "Verma", "Gupta",
    "Patwardhan", "Pawar", "Deshmukh", "Shinde", "Kulkarni", "Desai", "Bhosale", "Khanna", "Sawant",
    "Mane", "Naidu",
]

TEACHER_FIRST_NAMES = [
    "Meera", "Kabir", "Anjali", "Rohan", "Nisha", "Arpit", "Sonal", "Vikram", "Neha", "Rahul",
    "Priya", "Abhay", "Pooja", "Samir", "Kiran", "Monal", "Deepak", "Shruti", "Amit", "Rutuja",
]

TEACHER_LAST_NAMES = [
    "Singh", "Jain", "Patil", "Deshmukh", "Kulkarni", "Shah", "Verma", "More", "Joshi", "Pawar",
    "Nair", "Gupta", "Shinde", "Patwardhan", "Bhosale", "Chavan", "Kale", "Mane", "Jadhav",
    "Sawant", "Apte",
]

ADMIN_ACCOUNT_DATA = [
    "Aarav Sharma",
    "Riya Patel",
    "Aditya Nair",
    "Sneha Deshmukh",
    "Rohit Verma",
    "Poonam Shinde",
    "Kanika Apte",
    "Vishal Kulkarni",
    "Devansh Rao",
    "Simran Kapoor",
]

PLACEMENT_ACCOUNT_DATA = [
    ("Kabir Malhotra", "kabir.malhotra@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Sonal Tambe", "sonal.tambe@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Rahul Chitre", "rahul.chitre@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Priya Deshmukh", "priya.deshmukh@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Amit Ranade", "amit.ranade@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Neha Pansare", "neha.pansare@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Rohan Pawar", "rohan.pawar@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Anjali Rane", "anjali.rane@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Deepak Khedkar", "deepak.khedkar@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Shruti Sathe", "shruti.sathe@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Vikas Nimbalkar", "vikas.nimbalkar@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Pallavi Mokashi", "pallavi.mokashi@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Kiran Naik", "kiran.naik@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Manish Bendre", "manish.bendre@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Tanvi Bhujbal", "tanvi.bhujbal@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Komal Bhise", "komal.bhise@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Ajay Dhamale", "ajay.dhamale@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Snehal Chavan", "snehal.chavan@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Tejas Bhosale", "tejas.bhosale@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Yash Suryawanshi", "yash.suryawanshi@pccoepune.org", DEFAULT_STAFF_PASSWORD),
]

SCHOLARSHIP_ACCOUNT_DATA = [
    ("Neha Karmarkar", "neha.karmarkar@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Priya Gokhale", "priya.gokhale@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Aditi Dongre", "aditi.dongre@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Rohan Thombre", "rohan.thombre@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Sonal Bhadane", "sonal.bhadane@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Deepak Lagad", "deepak.lagad@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Shruti Karale", "shruti.karale@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Aman Darade", "aman.darade@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Pallavi Thorat", "pallavi.thorat@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Rakesh Chorge", "rakesh.chorge@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Snehal Hole", "snehal.hole@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Komal Madne", "komal.madne@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Tejas Khaire", "tejas.khaire@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Yash Gedam", "yash.gedam@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Kunal Pethkar", "kunal.pethkar@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Megha Raut", "megha.raut@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Tanvi Ingle", "tanvi.ingle@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Vikas Nale", "vikas.nale@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Anjali Khese", "anjali.khese@pccoepune.org", DEFAULT_STAFF_PASSWORD),
    ("Akash Kharat", "akash.kharat@pccoepune.org", DEFAULT_STAFF_PASSWORD),
]

SEED_DEPARTMENTS = [
    *[
        {
            "name": department["name"],
            "category": "Academic",
            "contact_email": department["contact_email"],
            "contact_number": f"98765432{index:02d}",
        }
        for index, department in enumerate(ACADEMIC_DEPARTMENTS, start=10)
    ],
    {
        "name": "Placement Cell",
        "category": "Placement",
        "contact_email": "placement@pccoepune.org",
        "contact_number": "9820012345",
    },
    {
        "name": "Scholarship Cell",
        "category": "Scholarship",
        "contact_email": "scholarship@pccoepune.org",
        "contact_number": "9833301122",
    },
    {
        "name": "Administration",
        "category": "Administrative",
        "contact_email": "admin.office@pccoepune.org",
        "contact_number": "9811101101",
    },
]


def _slugify_name(name):
    return ".".join(part.lower() for part in name.split() if part)


def _contact_number(seed_number):
    return f"98{seed_number:08d}"


def _student_email(first_name, last_name, admission_suffix):
    return f"{first_name.lower()}.{last_name.lower()}{admission_suffix}@pccoepune.org"


def _student_prn(admission_suffix, department_code, serial_number):
    return f"1{admission_suffix}B1{department_code}{serial_number:03d}"


def _student_class_and_year(admission_suffix):
    admission_year = 2000 + int(admission_suffix)
    current_year = 2026
    year_no = max(1, min(current_year - admission_year, 4))
    year_labels = {
        1: ("FY", "1st Year BTech"),
        2: ("SY", "2nd Year BTech"),
        3: ("TY", "3rd Year BTech"),
        4: ("BE", "4th Year BTech"),
    }
    return year_labels[year_no]


def _build_unique_name(index, first_names, last_names):
    first_name = first_names[index % len(first_names)]
    last_name = last_names[index % len(last_names)]
    return first_name, last_name


def _build_student_accounts():
    students = []
    for dept_index, department in enumerate(ACADEMIC_DEPARTMENTS):
        for position in range(20):
            global_index = dept_index * 20 + position
            first_name, last_name = _build_unique_name(global_index, STUDENT_FIRST_NAMES, STUDENT_LAST_NAMES)
            admission_suffix = "24" if position < 10 else "23"
            class_name, current_year = _student_class_and_year(admission_suffix)
            serial_number = 95 + position
            students.append(
                {
                    "name": f"{first_name} {last_name}",
                    "email": _student_email(first_name, last_name, admission_suffix),
                    "password": DEFAULT_STUDENT_PASSWORD,
                    "role": "student",
                    "department": department["name"],
                    "prn": _student_prn(admission_suffix, department["code"], serial_number),
                    "contact_number": _contact_number(global_index + 1),
                    "class_name": class_name,
                    "current_year": current_year,
                }
            )
    return students


def _build_teacher_accounts():
    teachers = []
    for dept_index, department in enumerate(ACADEMIC_DEPARTMENTS):
        for position in range(20):
            global_index = dept_index * 20 + position
            first_name, last_name = _build_unique_name(global_index, TEACHER_FIRST_NAMES, TEACHER_LAST_NAMES)
            full_name = f"{first_name} {last_name}"
            teachers.append(
                {
                    "name": f"Prof. {full_name}",
                    "email": f"{_slugify_name(full_name)}@pccoepune.org",
                    "password": DEFAULT_STAFF_PASSWORD,
                    "role": "teacher",
                    "department": department["name"],
                    "contact_number": _contact_number(101 + global_index),
                }
            )
    return teachers


STUDENT_ACCOUNT_DATA = _build_student_accounts()
TEACHER_ACCOUNT_DATA = _build_teacher_accounts()


def _find_student_email(department_name, position):
    matching_students = [student for student in STUDENT_ACCOUNT_DATA if student["department"] == department_name]
    return matching_students[position]["email"]


def _build_seed_users():
    users = []

    users.extend(STUDENT_ACCOUNT_DATA)
    users.extend(TEACHER_ACCOUNT_DATA)

    for index, name in enumerate(ADMIN_ACCOUNT_DATA, start=201):
        users.append(
            {
                "name": name,
                "email": f"{_slugify_name(name)}@pccoepune.org",
                "password": DEFAULT_STAFF_PASSWORD,
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


PRIMARY_COMP_STUDENT_EMAIL = _find_student_email("Computer Engineering", 0)
PLACEMENT_SAMPLE_STUDENT_EMAIL = _find_student_email("Computer Engineering", 11)
SCHOLARSHIP_SAMPLE_STUDENT_EMAIL = _find_student_email("Information Technology", 5)

SEED_USERS = _build_seed_users()

LOGIN_DEMO_USERS = [
    {"role": "student", "email": PRIMARY_COMP_STUDENT_EMAIL, "password": DEFAULT_STUDENT_PASSWORD},
    {"role": "teacher", "email": "meera.singh@pccoepune.org", "password": DEFAULT_STAFF_PASSWORD},
    {"role": "admin", "email": "aarav.sharma@pccoepune.org", "password": DEFAULT_STAFF_PASSWORD},
    {"role": "placement", "email": "kabir.malhotra@pccoepune.org", "password": DEFAULT_STAFF_PASSWORD},
    {"role": "scholarship", "email": "neha.karmarkar@pccoepune.org", "password": DEFAULT_STAFF_PASSWORD},
]

SEED_DOCUMENTS = [
    {
        "title": "10th Marksheet",
        "category": "Academic",
        "file_name": "10th-marksheet.pdf",
        "file_type": "PDF",
        "description": "Secondary school marksheet for educational record verification.",
        "status": "Approved",
        "owner_email": PRIMARY_COMP_STUDENT_EMAIL,
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
        "owner_email": PRIMARY_COMP_STUDENT_EMAIL,
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
        "owner_email": PRIMARY_COMP_STUDENT_EMAIL,
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
        "owner_email": PLACEMENT_SAMPLE_STUDENT_EMAIL,
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
        "owner_email": PRIMARY_COMP_STUDENT_EMAIL,
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
        "owner_email": PRIMARY_COMP_STUDENT_EMAIL,
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
        "owner_email": SCHOLARSHIP_SAMPLE_STUDENT_EMAIL,
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
        "owner_email": PLACEMENT_SAMPLE_STUDENT_EMAIL,
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
        "owner_email": PLACEMENT_SAMPLE_STUDENT_EMAIL,
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
        "owner_email": PLACEMENT_SAMPLE_STUDENT_EMAIL,
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
        "owner_email": PLACEMENT_SAMPLE_STUDENT_EMAIL,
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
        "owner_email": PLACEMENT_SAMPLE_STUDENT_EMAIL,
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
        "owner_email": SCHOLARSHIP_SAMPLE_STUDENT_EMAIL,
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
        "owner_email": SCHOLARSHIP_SAMPLE_STUDENT_EMAIL,
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
        "owner_email": "meera.singh@pccoepune.org",
        "department": "Computer Engineering",
        "remarks": "Shared with admin dashboard.",
    },
]


def ensure_seed_data(app):
    with app.app_context():
        db.create_all()
        ensure_workbench_tables()
        reset_workbench_sync_cache()

        seeded_emails = {data["email"] for data in SEED_USERS}
        removable_users = User.query.filter(
            (~User.email.in_(seeded_emails)) | (~User.email.like("%@pccoepune.org"))
        ).all()
        for removable_user in removable_users:
            for document in Document.query.filter_by(owner_id=removable_user.id).all():
                db.session.delete(document)
            db.session.delete(removable_user)
        db.session.commit()
        db.session.expire_all()

        valid_role_emails = {}
        for role in ("student", "teacher", "admin", "placement", "scholarship"):
            valid_role_emails[role] = sorted(
                data["email"] for data in SEED_USERS if data["role"] == role
            )
        prune_workbench_users(valid_role_emails)
        db.session.commit()

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
