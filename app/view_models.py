from collections import Counter
from datetime import date

from app.models import Department, Document, User
from app.profile_utils import build_profile_image_url, get_initials

DEPARTMENT_COLORS = {
    "Civil Engineering": "dept-blue",
    "Computer Engineering": "dept-blue",
    "AIML": "dept-blue",
    "Computer Engineering Regional": "dept-blue",
    "ENTC": "dept-blue",
    "Information Technology": "dept-blue",
    "Mechanical Engineering": "dept-blue",
    "Placement Cell": "dept-gold",
    "Scholarship Cell": "dept-green",
    "Administration": "dept-neutral",
}

CELL_ROLE_CONFIG = {
    "placement": {
        "title": "Placement Cell",
        "department": "Placement Cell",
        "categories": {"Placement"},
        "note": "Placement cell reviews only placement-specific student documents.",
    },
    "scholarship": {
        "title": "Scholarship Cell",
        "department": "Scholarship Cell",
        "categories": {"Scholarship", "Finance"},
        "note": "Scholarship cell reviews only scholarship and finance-related student documents.",
    },
}

BASE_STUDENT_DOCUMENT_CATALOG = [
    {
        "key": "tenth_marksheet",
        "name": "10th Marksheet",
        "about": "Secondary school marksheet used for academic identity and record matching.",
        "department": "Computer Engineering",
        "category": "Academic",
    },
    {
        "key": "twelfth_marksheet",
        "name": "12th Marksheet",
        "about": "Higher secondary marksheet required for admissions and placement documentation.",
        "department": "Computer Engineering",
        "category": "Academic",
    },
    {
        "key": "leaving_certificate",
        "name": "Leaving Certificate",
        "about": "Transfer or leaving certificate for institutional record verification.",
        "department": "Computer Engineering",
        "category": "Academic",
    },
    {
        "key": "semester_5_marksheet",
        "name": "Semester 5 Marksheet",
        "about": "Academic semester result used for verification and placement eligibility.",
        "department": "Computer Engineering",
        "category": "Academic",
    },
    {
        "key": "college_id",
        "name": "College ID Card",
        "about": "Official college identity card for campus and exam record validation.",
        "department": "Computer Engineering",
        "category": "ID Proof",
    },
    {
        "key": "aadhaar_card",
        "name": "Aadhaar Card",
        "about": "Government identity proof required for official student verification.",
        "department": "Computer Engineering",
        "category": "ID Proof",
    },
    {
        "key": "pan_card",
        "name": "PAN Card",
        "about": "Permanent account number card for scholarship and financial records.",
        "department": "Scholarship Cell",
        "category": "ID Proof",
    },
    {
        "key": "placement_resume",
        "name": "Placement Resume",
        "about": "Resume for internships and campus placement opportunities.",
        "department": "Placement Cell",
        "category": "Placement",
        "input_kind": "file",
    },
    {
        "key": "github_profile",
        "name": "GitHub Profile Link",
        "about": "GitHub profile link to showcase projects, repositories and coding activity.",
        "department": "Placement Cell",
        "category": "Placement",
        "input_kind": "link",
    },
    {
        "key": "linkedin_profile",
        "name": "LinkedIn Profile Link",
        "about": "LinkedIn profile link for placement networking and recruiter visibility.",
        "department": "Placement Cell",
        "category": "Placement",
        "input_kind": "link",
    },
    {
        "key": "portfolio_link",
        "name": "Portfolio / Other Professional Link",
        "about": "Portfolio, coding profile or any other professional placement link.",
        "department": "Placement Cell",
        "category": "Placement",
        "input_kind": "link",
    },
    {
        "key": "offer_letter",
        "name": "Placement Offer Letter",
        "about": "Offer or internship selection letter for placement cell documentation.",
        "department": "Placement Cell",
        "category": "Placement",
        "input_kind": "file",
    },
    {
        "key": "scholarship_form",
        "name": "Scholarship Form",
        "about": "Scholarship application form and support documents for financial aid.",
        "department": "Scholarship Cell",
        "category": "Scholarship",
    },
    {
        "key": "fee_receipt",
        "name": "Fee Receipt",
        "about": "Fee payment proof required for scholarship and finance verification.",
        "department": "Scholarship Cell",
        "category": "Finance",
    },
    {
        "key": "bonafide_certificate",
        "name": "Bonafide Certificate",
        "about": "Official bonafide certificate used for academic and scholarship records.",
        "department": "Computer Engineering",
        "category": "Academic",
    },
]

TEACHER_DOCUMENT_CATALOG = [
    {
        "key": "student_records",
        "name": "Student Records",
        "about": "Academic student records and class-wise documentation maintained by faculty.",
        "department": "Computer Engineering",
        "category": "Academic",
        "input_kind": "file",
    },
    {
        "key": "attendance_sheet",
        "name": "Attendance Sheet",
        "about": "Attendance register or consolidated monthly attendance upload.",
        "department": "Computer Engineering",
        "category": "Academic",
        "input_kind": "file",
    },
    {
        "key": "department_report",
        "name": "Department Report",
        "about": "Department summary report for admin and academic office review.",
        "department": "Computer Engineering",
        "category": "Department",
        "input_kind": "file",
    },
    {
        "key": "placement_letter",
        "name": "Placement Letter",
        "about": "Placement update, offer consolidation, or drive-related document.",
        "department": "Placement Cell",
        "category": "Placement",
        "input_kind": "file",
    },
    {
        "key": "scholarship_approval",
        "name": "Scholarship Approval Letter",
        "about": "Scholarship approval or recommendation file for student cases.",
        "department": "Scholarship Cell",
        "category": "Scholarship",
        "input_kind": "file",
    },
    {
        "key": "noc_certificate",
        "name": "NOC / Certificate",
        "about": "No-objection certificate or official teaching-side approval document.",
        "department": "Computer Engineering",
        "category": "Official",
        "input_kind": "file",
    },
]


def build_student_document_catalog(user):
    catalog = list(BASE_STUDENT_DOCUMENT_CATALOG)
    study_year = get_study_year(user)

    year_result_docs = []
    if study_year >= 1:
        year_result_docs.extend(
            [
                {
                    "key": "first_year_marksheet",
                    "name": "First Year Marksheet",
                    "about": "Combined first year BTech marksheet for academic verification.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
                {
                    "key": "semester_1_marksheet",
                    "name": "Semester 1 Marksheet",
                    "about": "Semester 1 result for first year BTech academic record.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
                {
                    "key": "semester_2_marksheet",
                    "name": "Semester 2 Marksheet",
                    "about": "Semester 2 result for first year BTech academic record.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
            ]
        )
    if study_year >= 2:
        year_result_docs.extend(
            [
                {
                    "key": "second_year_marksheet",
                    "name": "Second Year Marksheet",
                    "about": "Combined second year BTech marksheet for academic continuity.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
                {
                    "key": "semester_3_marksheet",
                    "name": "Semester 3 Marksheet",
                    "about": "Semester 3 result for second year BTech record tracking.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
                {
                    "key": "semester_4_marksheet",
                    "name": "Semester 4 Marksheet",
                    "about": "Semester 4 result for second year BTech verification.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
            ]
        )
    if study_year >= 3:
        year_result_docs.extend(
            [
                {
                    "key": "third_year_marksheet",
                    "name": "Third Year Marksheet",
                    "about": "Combined third year BTech marksheet for placement and scholarship review.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
                {
                    "key": "semester_5_marksheet",
                    "name": "Semester 5 Marksheet",
                    "about": "Academic semester result used for verification and placement eligibility.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
                {
                    "key": "semester_6_marksheet",
                    "name": "Semester 6 Marksheet",
                    "about": "Semester 6 result for third year BTech academic verification.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
            ]
        )
    if study_year >= 4:
        year_result_docs.extend(
            [
                {
                    "key": "fourth_year_marksheet",
                    "name": "Fourth Year Marksheet",
                    "about": "Final year BTech marksheet set for graduation and placement records.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
                {
                    "key": "semester_7_marksheet",
                    "name": "Semester 7 Marksheet",
                    "about": "Semester 7 result for final year progress tracking.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
                {
                    "key": "semester_8_marksheet",
                    "name": "Semester 8 Marksheet",
                    "about": "Semester 8 result for final BTech completion records.",
                    "department": "Computer Engineering",
                    "category": "Academic",
                },
            ]
        )

    existing_names = {item["name"] for item in catalog}
    for item in year_result_docs:
        if item["name"] not in existing_names:
            catalog.append(item)
            existing_names.add(item["name"])

    return catalog


def serialize_document(document):
    department_name = document.department.name if document.department else "General"
    role_name = document.owner.role if document.owner else ""
    return {
        "id": f"DOC-{document.id:04d}",
        "raw_id": document.id,
        "name": document.title,
        "about": document.description or document.remarks or "No description added.",
        "message": document.remarks or "No changes requested.",
        "value": document.file_path if (document.file_type or "").upper() == "LINK" else "",
        "owner": document.owner.name if document.owner else "Unknown",
        "owner_email": document.owner.email if document.owner else "",
        "role": role_name,
        "role_label": _role_label(role_name),
        "department": department_name,
        "department_class": DEPARTMENT_COLORS.get(department_name, "dept-neutral"),
        "category": document.category,
        "status": document.status,
        "submitted_on": document.created_at.strftime("%d %b %Y"),
        "file_name": document.file_name,
        "file_type": document.file_type or "File",
        "input_kind": "link" if (document.file_type or "").upper() == "LINK" else "file",
        "review_needed": document.status in {"Pending", "Changes Requested"},
    }


def build_student_dashboard(user):
    documents = Document.query.filter_by(owner_id=user.id).order_by(Document.created_at.desc()).all()
    document_map = {doc.title: doc for doc in documents}
    serialized = []

    for preset in build_student_document_catalog(user):
        existing = document_map.get(preset["name"])
        if existing:
            item = serialize_document(existing)
            item["preset_key"] = preset["key"]
            item["uploaded"] = True
            item["input_kind"] = preset.get("input_kind", item.get("input_kind", "file"))
        else:
            item = {
                "id": "-",
                "raw_id": None,
                "name": preset["name"],
                "about": preset["about"],
                "owner": user.name,
                "owner_email": user.email,
                "role": user.role,
                "role_label": _role_label(user.role),
                "department": preset["department"],
                "department_class": DEPARTMENT_COLORS.get(preset["department"], "dept-neutral"),
                "category": preset["category"],
                "status": "Not Uploaded",
                "message": "Upload this document to start verification.",
                "value": "",
                "submitted_on": "-",
                "file_name": "",
                "file_type": "",
                "preset_key": preset["key"],
                "uploaded": False,
                "input_kind": preset.get("input_kind", "file"),
            }
        serialized.append(item)

    counts = Counter(doc["status"] for doc in serialized if doc["uploaded"])
    notification = "All major records are complete."
    if counts.get("Pending"):
        notification = f"You have {counts['Pending']} document(s) waiting for review."
    elif any(not doc["uploaded"] for doc in serialized):
        notification = "Some required documents are still not uploaded."

    grouped_documents = {
        "academic": [doc for doc in serialized if doc["category"] in {"Academic", "ID Proof"}],
        "placement": [doc for doc in serialized if doc["category"] == "Placement"],
        "scholarship": [doc for doc in serialized if doc["category"] in {"Scholarship", "Finance"}],
    }

    return {
        "student": {
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "role": _role_label(user.role),
            "prn": user.prn or "Not assigned",
            "department": user.department.name if user.department else "Not assigned",
            "contact_number": user.contact_number or "Not added",
            "study_year": get_study_year_label(user),
            "status": "Placement Ready" if counts.get("Approved", 0) >= 3 else "Profile in Progress",
            "profile_image": build_profile_image_url(user.profile_image),
            "avatar_initials": get_initials(user.name),
        },
        "notification": notification,
        "notifications": build_student_notifications(serialized),
        "documents": serialized,
        "document_groups": grouped_documents,
    }


def build_admin_payload():
    documents = Document.query.order_by(Document.created_at.desc()).all()
    users = User.query.order_by(User.role.asc(), User.name.asc()).all()
    departments = Department.query.order_by(Department.name.asc()).all()
    serialized = [serialize_document(doc) for doc in documents]
    student_documents = [doc for doc in serialized if doc["role"] == "student"]
    teacher_documents = [doc for doc in serialized if doc["role"] == "teacher"]
    placement_documents = [doc for doc in serialized if doc["category"] == "Placement"]
    scholarship_documents = [doc for doc in serialized if doc["category"] in {"Scholarship", "Finance"}]
    dept_summaries = _department_summaries(departments, serialized)
    return {
        "stats": [
            {"label": "Total Users", "value": User.query.count(), "detail": "All active accounts"},
            {"label": "Documents", "value": len(serialized), "detail": "Uploaded in database"},
            {"label": "Pending", "value": sum(1 for item in serialized if item["status"] == "Pending"), "detail": "Need review"},
            {"label": "Departments", "value": len(departments), "detail": "Colour-coded views"},
        ],
        "documents": serialized,
        "student_documents": student_documents,
        "teacher_documents": teacher_documents,
        "placement_documents": placement_documents,
        "scholarship_documents": scholarship_documents,
        "student_review_groups": group_documents_by_owner(student_documents),
        "teacher_review_groups": group_documents_by_owner(teacher_documents),
        "users": users,
        "departments": dept_summaries,
        "activity": [
            f"{sum(1 for item in serialized if item['status'] == 'Pending')} documents are waiting for action.",
            f"{sum(1 for user in users if user.role == 'student')} student accounts are active in the database.",
            f"{sum(1 for user in users if user.role == 'placement')} placement cell account(s) are active.",
            f"{sum(1 for user in users if user.role == 'scholarship')} scholarship cell account(s) are active.",
        ],
    }


def build_teacher_payload(user):
    teacher_documents = Document.query.filter_by(owner_id=user.id).order_by(Document.created_at.desc()).all()
    serialized_teacher_docs = build_role_catalog_rows(user, teacher_documents, TEACHER_DOCUMENT_CATALOG)
    students = User.query.filter_by(role="student").order_by(User.name.asc()).all()
    student_documents = (
        Document.query.join(User, Document.owner_id == User.id)
        .filter(User.role == "student")
        .order_by(Document.updated_at.desc())
        .all()
    )
    serialized_student_docs = [serialize_document(doc) for doc in student_documents]
    return {
        "teacher": user,
        "documents": serialized_teacher_docs,
        "student_documents": serialized_student_docs,
        "students": [
            {
                "name": student.name,
                "prn": student.prn or "Not assigned",
                "department": student.department.name if student.department else "Not assigned",
                "email": student.email,
                "status": "Ready" if student.documents else "No documents yet",
                "study_year": get_study_year_label(student),
                "profile_image": build_profile_image_url(student.profile_image),
                "avatar_initials": get_initials(student.name),
            }
            for student in students
        ],
        "departments": _department_summaries(Department.query.order_by(Department.name.asc()).all(), serialized_student_docs),
        "activity": [
            "Teacher records are synced from the database.",
            f"{len(serialized_teacher_docs)} teacher-side preset rows are available for upload.",
            f"{len(students)} students can be monitored from this panel.",
        ],
        "notifications": [doc["message"] for doc in serialized_student_docs if doc["message"] and doc["message"] != "No changes requested."][:4],
    }


def build_cell_payload(user):
    config = CELL_ROLE_CONFIG[user.role]
    categories = config["categories"]
    documents = (
        Document.query.join(User, Document.owner_id == User.id)
        .filter(User.role == "student", Document.category.in_(categories))
        .order_by(Document.updated_at.desc())
        .all()
    )
    serialized_docs = [serialize_document(doc) for doc in documents]
    students = User.query.filter_by(role="student").order_by(User.name.asc()).all()
    student_cards = [
        {
            "name": student.name,
            "prn": student.prn or "Not assigned",
            "department": student.department.name if student.department else "Not assigned",
            "email": student.email,
            "status": "Shared" if any(doc["owner_email"] == student.email for doc in serialized_docs) else "No matching documents",
            "study_year": get_study_year_label(student),
            "profile_image": build_profile_image_url(student.profile_image),
            "avatar_initials": get_initials(student.name),
        }
        for student in students
    ]
    return {
        "cell_user": user,
        "cell_title": config["title"],
        "documents": serialized_docs,
        "document_groups": group_documents_by_owner(serialized_docs),
        "students": student_cards,
        "stats": [
            {"label": "Students", "value": len(student_cards), "detail": "Visible across connected database"},
            {"label": "Filtered Docs", "value": len(serialized_docs), "detail": ", ".join(sorted(categories))},
            {"label": "Pending", "value": sum(1 for doc in serialized_docs if doc["status"] == "Pending"), "detail": "Need cell review"},
            {"label": "Approved", "value": sum(1 for doc in serialized_docs if doc["status"] == "Approved"), "detail": "Already verified"},
        ],
        "activity": [
            config["note"],
            f"{len(serialized_docs)} student document(s) match the {config['title']} filter.",
            f"{sum(1 for doc in serialized_docs if doc['status'] == 'Pending')} document(s) are currently pending.",
        ],
    }


def group_users(users):
    return {
        "students": [_serialize_user_directory_row(user) for user in users if user.role == "student"],
        "teachers": [_serialize_user_directory_row(user) for user in users if user.role == "teacher"],
        "admin": [_serialize_user_directory_row(user) for user in users if user.role == "admin"],
        "placement": [_serialize_user_directory_row(user) for user in users if user.role == "placement"],
        "scholarship": [_serialize_user_directory_row(user) for user in users if user.role == "scholarship"],
    }


def _department_summaries(departments, serialized_documents):
    summary = []
    theme_map = {
        "Civil Engineering": "berry",
        "Computer Engineering": "berry",
        "AIML": "berry",
        "Computer Engineering Regional": "berry",
        "ENTC": "berry",
        "Information Technology": "berry",
        "Mechanical Engineering": "berry",
        "Placement Cell": "sunrise",
        "Scholarship Cell": "aqua",
        "Administration": "berry",
    }
    for dept in departments:
        docs = [doc for doc in serialized_documents if doc["department"] == dept.name]
        summary.append(
            {
                "name": dept.name,
                "lead": dept.contact_email,
                "pending": sum(1 for doc in docs if doc["status"] == "Pending"),
                "approved": sum(1 for doc in docs if doc["status"] == "Approved"),
                "theme": theme_map.get(dept.name, "berry"),
            }
        )
    return summary


def build_role_catalog_rows(user, existing_documents, catalog):
    document_map = {doc.title: doc for doc in existing_documents}
    rows = []
    for preset in catalog:
        existing = document_map.get(preset["name"])
        if existing:
            item = serialize_document(existing)
            item["preset_key"] = preset["key"]
            item["uploaded"] = True
            item["input_kind"] = preset.get("input_kind", item.get("input_kind", "file"))
        else:
            item = {
                "id": "-",
                "raw_id": None,
                "name": preset["name"],
                "about": preset["about"],
                "message": "Upload this document to share it with admin and departments.",
                "value": "",
                "owner": user.name,
                "owner_email": user.email,
                "role": user.role,
                "role_label": _role_label(user.role),
                "department": preset["department"],
                "department_class": DEPARTMENT_COLORS.get(preset["department"], "dept-neutral"),
                "category": preset["category"],
                "status": "Not Uploaded",
                "submitted_on": "-",
                "file_name": "",
                "file_type": "",
                "preset_key": preset["key"],
                "uploaded": False,
                "input_kind": preset.get("input_kind", "file"),
                "review_needed": True,
            }
        rows.append(item)
    return rows


def build_student_notifications(serialized_docs):
    notifications = [doc["message"] for doc in serialized_docs if doc["message"] and doc["message"] != "No changes requested."]
    if not notifications:
        notifications.append("No new teacher/admin review messages right now.")
    return notifications[:5]


def group_documents_by_owner(documents):
    grouped = {}
    for doc in documents:
        owner_key = doc["owner_email"] or doc["owner"]
        if owner_key not in grouped:
            grouped[owner_key] = {
                "name": doc["owner"],
                "email": doc["owner_email"] or "No email available",
                "role": doc["role_label"],
                "department": doc["department"],
                "department_class": doc["department_class"],
                "documents": [],
            }
        grouped[owner_key]["documents"].append(doc)

    groups = list(grouped.values())
    for group in groups:
        docs = group["documents"]
        group["document_count"] = len(docs)
        group["pending_count"] = sum(1 for doc in docs if doc["status"] in {"Pending", "Changes Requested"})
        group["approved_count"] = sum(1 for doc in docs if doc["status"] == "Approved")
        group["latest_message"] = next(
            (doc["message"] for doc in docs if doc["message"] and doc["message"] != "No changes requested."),
            "No review notes yet.",
        )
        group["needs_attention"] = group["pending_count"] > 0

    groups.sort(key=lambda item: (-item["needs_attention"], item["name"]))
    return groups


def _serialize_user_directory_row(user):
    return {
        "name": user.name,
        "prn": user.prn or "Not assigned",
        "department": user.department.name if user.department else "Not assigned",
        "status": "Active",
        "email": user.email,
        "role": _role_label(user.role),
    }


def _role_label(role):
    return {
        "admin": "Admin",
        "teacher": "Teacher",
        "student": "Student",
        "placement": "Placement Cell",
        "scholarship": "Scholarship Cell",
    }.get(role, role.title() if role else "User")


def get_study_year(user):
    prn = user.prn or ""
    admission_year = _extract_admission_year(prn)

    if admission_year is None:
        return 1

    current_year = date.today().year
    study_year = current_year - admission_year
    return max(1, min(study_year, 4))


def get_study_year_label(user):
    labels = {
        1: "1st Year BTech",
        2: "2nd Year BTech",
        3: "3rd Year BTech",
        4: "4th Year BTech",
    }
    return labels.get(get_study_year(user), "BTech")


def _extract_admission_year(prn):
    if not prn:
        return None

    normalized = str(prn).strip().upper()
    if len(normalized) >= 4 and normalized[:4].isdigit():
        return int(normalized[:4])

    if len(normalized) >= 3 and normalized[1:3].isdigit():
        return 2000 + int(normalized[1:3])

    return None
