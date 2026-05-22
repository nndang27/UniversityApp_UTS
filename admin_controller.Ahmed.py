from .ui import display, prompt, CYAN, YELLOW, RED
from ..core.db import Database
from ..core.models import Student, compute_grade


def run_admin_menu(level: int) -> None:
    while True:
        choice = prompt(level, "Admin System (c/g/p/r/s/x): ", CYAN).strip().lower()

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


def show_students(level: int) -> None:
    students = Database.fetch_all()

    if len(students) == 0:
        display(level + 2, "<Nothing to Display>")
        return

    display(level, "Student List", YELLOW)

    for student in students:
        text = f"{student.name} :: {student.student_id} --> Email: {student.email}"
        display(level + 1, text)


def group_by_grade(level: int) -> None:
    students = Database.fetch_all()

    if len(students) == 0:
        display(level + 2, "<Nothing to Display>")
        return

    groups = {
        "N/A": [],
        "Z": [],
        "P": [],
        "C": [],
        "D": [],
        "HD": []
    }

    for student in students:
        avg = student.average_mark()

        if avg is None:
            entry = f"{student.name} :: {student.student_id} --> GRADE: N/A"
            groups["N/A"].append(entry)
        else:
            grade = compute_grade(round(avg))
            entry = f"{student.name} :: {student.student_id} --> GRADE: {grade} - MARK: {avg:.2f}"
            groups[grade].append(entry)

    for grade in ["N/A", "Z", "P", "C", "D", "HD"]:
        if len(groups[grade]) > 0:
            display(level, f"{grade} --> [{', '.join(groups[grade])}]", YELLOW)


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
            entry = f"{student.name} :: {student.student_id}"
            buckets["N/A"].append(entry)
        else:
            grade = compute_grade(round(avg))
            entry = f"{student.name} :: {student.student_id} --> GRADE: {grade} - MARK: {avg:.2f}"

            if avg >= 50:
                buckets["PASS"].append(entry)
            else:
                buckets["FAIL"].append(entry)

    display(level, f"N/A --> [{', '.join(buckets['N/A'])}]", YELLOW)
    display(level, f"FAIL --> [{', '.join(buckets['FAIL'])}]", YELLOW)
    display(level, f"PASS --> [{', '.join(buckets['PASS'])}]", YELLOW)


def remove_student(level: int) -> None:
    students = Database.fetch_all()

    student_id = prompt(level, "Remove by ID: ", CYAN).strip()

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


def clear_database(level: int) -> None:
    answer = prompt(level, "Clear database? Y/N: ", CYAN).strip().upper()

    if answer == "Y":
        Database.persist_all([])
        display(level, "Students data cleared", YELLOW)
    else:
        display(level, "Clear cancelled", RED)
