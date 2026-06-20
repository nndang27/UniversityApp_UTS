"""
cliApp/cli/student_controller.py
=================================
OWNER: Person 1

Student System menu and authentication logic for CLIUniApp.
Handles student registration, login, and the student menu loop.
After a successful login the student is handed off to the Subject
Enrolment System (enrolment_controller.py — owned by Person 2).

Marking criteria covered here (9 marks):
    - register saves data to file                   [2 marks]
    - login reads data from file                    [2 marks]
    - regex validation for email and password       [2 marks]
    - error handling                                [2 marks]
    - I/O matches sample                            [1 mark]
"""

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
    """
    Handle the new-student registration flow.

    Input:
        level -- current terminal indentation depth
    Output:
        None.
        On success: a new Student record is written to students.data and a
                    confirmation message is displayed.
        On failure: an error message is displayed and the function returns
                    without creating a record.

    Flow:
        1. Prompt for email and password.
        2. Validate both against the regex patterns (EMAIL_PATTERN, PASSWORD_PATTERN).
           If either fails → display error and re-prompt.
        3. Load all students; check whether this email is already registered.
           If duplicate → display error and return.
        4. Derive display name from email via name_from_email().
        5. Generate a unique student ID and create a Student object.
        6. Append to the student list and persist to file.
    """
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
    """
    Handle the student login flow.

    Input:
        level -- current terminal indentation depth
    Output:
        The matching Student object on successful login.
        None if login fails for any reason (invalid format, unknown student,
        or wrong password).  An appropriate message is displayed in each case.

    Flow:
        1. Prompt for email and password.
        2. Validate format; if invalid → display error and re-prompt.
        3. Load all students; search by email (case-insensitive).
           If not found → display error and return None.
        4. Compare password; if wrong → display error and return None.
        5. Return the matching Student object.
    """
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
    """
    Student System menu loop.

    Input:
        level -- current terminal indentation depth
    Output:
        None  (returns to the University menu when the user enters X)

    Menu options:
        l  →  login flow; on success, opens Subject Enrolment System
        r  →  registration flow
        x  →  return to University menu
        *  →  display invalid-option error and repeat
    """
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
