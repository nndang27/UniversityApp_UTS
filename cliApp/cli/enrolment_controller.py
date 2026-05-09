
import random

from .ui import display, prompt, CYAN, YELLOW, RED
from ..core.db import Database
from ..core.models import Student, Subject, compute_grade
from ..core.util import new_subject_id
from ..core.validation import is_valid_password


# ---------------------------------------------------------------------------
# Course menu  (called by student_controller.py after login)
# ---------------------------------------------------------------------------

def run_course_menu(level: int, student: Student) -> None:

    while True:
        choice = prompt(level, "Course Menu (c/e/r/s/x): ", CYAN).strip().lower()

        if choice == "c":
            change_password(level + 1, student)
        elif choice == "e":
            enrol_subject(level + 1, student)
        elif choice == "r":
            remove_subject(level + 1, student)
        elif choice == "s":
            show_subjects(level + 1, student)
        elif choice == "x":
            return
        else:
            display(level + 1, "Invalid option", RED)


# ---------------------------------------------------------------------------
# Enrol in a new subject
# ---------------------------------------------------------------------------

def enrol_subject(level: int, student: Student) -> None:

    if student.at_capacity():
        display(level, "Students are allowed to enrol in 4 subjects only", RED)
        return

    taken = [sub.subject_id for sub in student.subjects]

    sid = new_subject_id(taken)
    mark = random.randint(25, 100)
    grade = compute_grade(mark)

    new_sub = Subject(sid, mark, grade)
    student.subjects.append(new_sub)

    all_students = Database.fetch_all()

    for s in all_students:
        if s.student_id == student.student_id:
            s.subjects = student.subjects
            break

    Database.persist_all(all_students)

    display(level, f"Enrolling in Subject-{sid}", YELLOW)
    display(level, f"You are now enrolled in {len(student.subjects)} out of 4 subjects", YELLOW)


# ---------------------------------------------------------------------------
# Show enrolled subjects
# ---------------------------------------------------------------------------

def show_subjects(level: int, student: Student) -> None:

    if not student.subjects:
        display(level, "No subjects enrolled yet", RED)
        return

    for sub in student.subjects:
        display(level, f"[Subject::{sub.subject_id} -- mark = {sub.mark} -- grade = {sub.grade}]")


# ---------------------------------------------------------------------------
# Remove a subject
# ---------------------------------------------------------------------------

def remove_subject(level: int, student: Student) -> None:

    entered_id = prompt(level, "Remove Subject by ID: ", CYAN).strip()

    subject = student.find_subject(entered_id)

    if subject is None:
        display(level, f"Subject-{entered_id} not found", RED)
        return

    student.drop_subject(entered_id)

    all_students = Database.fetch_all()

    for s in all_students:
        if s.student_id == student.student_id:
            s.subjects = student.subjects
            break

    Database.persist_all(all_students)

    display(level, f"Dropping Subject-{entered_id}", YELLOW)
    display(level, f"You are now enrolled in {len(student.subjects)} out of 4 subjects", YELLOW)


# ---------------------------------------------------------------------------
# Change password
# ---------------------------------------------------------------------------

def change_password(level: int, student: Student) -> None:

    display(level, "Updating Password", YELLOW)

    while True:
        new_pw = prompt(level, "New Password: ", CYAN)

        if not is_valid_password(new_pw):
            display(level, "Invalid password format", RED)
            continue

        break

    while True:
        confirm_pw = prompt(level, "Confirm Password: ", CYAN)

        if confirm_pw != new_pw:
            display(level, "Password confirmation does not match", RED)
            continue

        break

    all_students = Database.fetch_all()

    for s in all_students:
        if s.student_id == student.student_id:
            s.password = new_pw
            break

    Database.persist_all(all_students)

    student.password = new_pw

    display(level, "Password updated successfully", YELLOW)