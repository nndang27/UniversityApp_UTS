
from .ui import display, prompt, CYAN, YELLOW, RED
from ..core.db import Database
from ..core.models import Student, compute_grade


# ---------------------------------------------------------------------------
# Admin menu  (called by university_menu.py)
# ---------------------------------------------------------------------------

def run_admin_menu(level: int) -> None:

    while True:
        choice = prompt(level, "Admin System (c/g/p/r/s/x): ", CYAN).lower()

        if choice == "c":
            clear_database(level + 1)
        elif choice == "g":
            group_by_grade(level + 1)
        elif choice == "p":
            partition_pass_fail(level + 1)
        elif choice == "r":
            remove_student(level + 1)
        elif choice == "s":
            show_students(level + 1)
        elif choice == "x":
            break
        else:
            display(level + 1, "Invalid option", RED)


# ---------------------------------------------------------------------------
# Show all students
# ---------------------------------------------------------------------------

def show_students(level: int) -> None:

    students = Database.fetch_all()

    if len(students) == 0:
        display(level + 2, "<Nothing to Display>")
        return

    display(level, "Student List", YELLOW)

    for student in students:
        text = f"{student.name} :: {student.student_id} --> Email: {student.email}"
        display(level + 1, text)


# ---------------------------------------------------------------------------
# Group students by grade
# ---------------------------------------------------------------------------

def group_by_grade(level: int) -> None:

    students = Database.fetch_all()

    if len(students) == 0:
        display(level + 2, "<Nothing to Display>")
        return

    groups = {
        "Z": [],
        "P": [],
        "C": [],
        "D": [],
        "HD": [],
        "N/A": []
    }

    for student in students:
        avg = student.average_mark()

        if avg is None:
            groups["N/A"].append(student)
        else:
            grade = compute_grade(round(avg))
            groups[grade].append(student)

    for grade in ["Z", "P", "C", "D", "HD", "N/A"]:
        if len(groups[grade]) > 0:
            display(level, f"{grade} -->", YELLOW)

            for student in groups[grade]:
                text = f"{student.name} :: {student.student_id} --> GRADE: {grade}"
                display(level + 1, text)


# ---------------------------------------------------------------------------
# Partition students into PASS / FAIL
# ---------------------------------------------------------------------------

def partition_pass_fail(level: int) -> None:

    students = Database.fetch_all()

    buckets = {
        "N/A": [],
        "FAIL": [],
        "PASS": []
    }

    for student in students:
        avg = student.average_mark()

        if avg is None:
            buckets["N/A"].append(f"{student.name} :: {student.student_id}")
        elif avg >= 50:
            buckets["PASS"].append(f"{student.name} :: {student.student_id} --> GRADE: PASS")
        else:
            buckets["FAIL"].append(f"{student.name} :: {student.student_id} --> GRADE: FAIL")

    for label in ["N/A", "FAIL", "PASS"]:
        entries = buckets[label]

        if len(entries) == 0:
            display(level, f"{label} --> []", YELLOW)
        else:
            display(level, f"{label} --> [{', '.join(entries)}]", YELLOW)


# ---------------------------------------------------------------------------
# Remove a student by ID
# ---------------------------------------------------------------------------

def remove_student(level: int) -> None:

    students = Database.fetch_all()

    student_id = prompt(level, "Remove by" \
    " ID: ", CYAN)

    found = False
    updated_students = []

    for student in students:
        if student.student_id == student_id:
            found = True
        else:
            updated_students.append(student)

    if found:
        Database.persist_all(updated_students)
        display(level, f"Removing Student {student_id} Account", YELLOW)
    else:
        display(level, f"Student {student_id} does not exist", RED)


# ---------------------------------------------------------------------------
# Clear the database
# ---------------------------------------------------------------------------

def clear_database(level: int) -> None:

    answer = prompt(level, "Clear database? Y/N: ", CYAN)

    if answer.upper() == "Y":
        Database.persist_all([])
        display(level, "Students data cleared", YELLOW)
    else:
        display(level, "Clear cancelled", RED)