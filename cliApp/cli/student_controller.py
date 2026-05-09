

from typing import Optional

from .ui import display, prompt, CYAN, GREEN, YELLOW, RED, SUBMENU_JUMP
from ..core.db import Database
from ..core.models import Student
from ..core.util import new_student_id
from ..core.validation import is_valid_email, is_valid_password, name_from_email
from .enrolment_controller import run_course_menu


# ---------------------------------------------------------------------------
# Registration
# ---------------------------------------------------------------------------

def _register(level: int) -> None:

    display(level, "Student Sign Up", GREEN)

    while True:
        email    = prompt(level, "Email: ")
        password = prompt(level, "Password: ")

        if not is_valid_email(email) or not is_valid_password(password):
            display(level, "Incorrect email or password format", RED)
            continue

        display(level, "email and password formats acceptable", YELLOW)

        all_students = Database.fetch_all()
        already_exists = any(s.email.lower() == email.lower() for s in all_students)
        if already_exists:
            display(level, f"Student {name_from_email(email)} already exists", RED)
            return

        full_name = name_from_email(email)
        display(level, f"Enrolling student {full_name}", YELLOW)

        taken_ids  = [s.student_id for s in all_students]
        student_id = new_student_id(taken_ids)
        new_student = Student(student_id, full_name, email, password)
        all_students.append(new_student)
        Database.persist_all(all_students)
        return


# ---------------------------------------------------------------------------
# Login
# ---------------------------------------------------------------------------

def _login(level: int) -> Optional[Student]:

    display(level, "Student Sign In", GREEN)

    while True:
        email    = prompt(level, "Email: ")
        password = prompt(level, "Password: ")

        if not is_valid_email(email) or not is_valid_password(password):
            display(level, "Incorrect email or password format", RED)
            continue

        display(level, "email and password formats acceptable", YELLOW)

        all_students = Database.fetch_all()
        matched = next(
            (s for s in all_students if s.email.lower() == email.lower()), None
        )

        if matched is None:
            display(level, "Student does not exist", RED)
            return None

        if matched.password != password:
            display(level, "Password incorrect", RED)
            return None

        return matched


# ---------------------------------------------------------------------------
# Student menu
# ---------------------------------------------------------------------------

def run_student_menu(level: int) -> None:

    while True:
        choice = prompt(
            level,
            "Student System (l)ogin, (r)egister, or (x) to exit: ",
            CYAN,
        ).lower()

        if choice == "r":
            _register(level)
        elif choice == "l":
            student = _login(level)
            if student is not None:
                run_course_menu(level + SUBMENU_JUMP, student)
        elif choice == "x":
            return
        else:
            display(level, "Invalid option. Please enter l, r, or x.", RED)
