"""
cliApp/cli/enrolment_controller.py
===================================
OWNER: Person 2  —  Subject Enrolment System  (15 marks)

This file contains the Subject Enrolment System menu and all operations
a logged-in student can perform on their subject list.

Marking criteria you are responsible for (15 marks total):
    - Enrol in a subject (max 4)                [2 marks]
    - Enrolment is tracked and persisted        [2 marks]
    - Remove a subject by its ID                [2 marks]
    - Show enrolled subjects                    [1 mark]
    - Change password                           [2 marks]
    - Read / write to students.data             [3 marks]
    - Error handling                            [2 marks]
    - I/O matches sample output                 [1 mark]

DO NOT modify any file outside this file.
All imports you will need are already listed below.
"""

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
    """
    PURPOSE:
        Main loop for the Subject Enrolment System.
        Stays open until the student chooses (x) to go back to the Student menu.
        Each option delegates to one of the helper functions defined below.

    INPUT:
        level   -- int, current terminal indentation depth (use this when calling
                   display() and prompt() so indentation stays consistent)
        student -- Student object representing the currently logged-in student;
                   keep this object up-to-date in memory as well as in the file

    OUTPUT:
        None.  Returns to run_student_menu() when the user enters x.

    MENU OPTIONS TO HANDLE:
        c  →  call change_password(level, student)
        e  →  call enrol_subject(level, student)
        r  →  call remove_subject(level, student)
        s  →  call show_subjects(level, student)
        x  →  return  (exit back to Student menu)
        *  →  display an "Invalid option" message and loop again

    HINT:
        Use prompt(level, "...", CYAN) to read the user's choice,
        and display(level, "...", RED) for invalid-input errors.
    """
    # TODO: implement the course menu loop
    while True:
        choice = prompt(level, "Student Course Menu (c/e/r/s/x): ", CYAN).strip().lower()

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
    """
    PURPOSE:
        Enrol the logged-in student in one new randomly generated subject.
        Enforces the 4-subject maximum and persists the change to students.data.

    INPUT:
        level   -- int, current terminal indentation depth
        student -- Student object (in-memory); its .subjects list reflects the
                   current enrolments

    OUTPUT:
        None.
        Success path:
            - A new Subject is appended to student.subjects (in-memory).
            - students.data is updated so the change is permanent.
            - A confirmation line is displayed, e.g.:
                  "Enrolling in Subject-042"
            - A count line is displayed, e.g.:
                  "You are now enrolled in 3 out of 4 subjects"
        Failure path (already at the limit):
            - Display an error message and return immediately without
              making any changes.

    STEPS TO IMPLEMENT:
        1. Check student.at_capacity().
               If True  → display an error ("Students are allowed to enrol in
                           4 subjects only") and return.
        2. Collect the IDs already held by this student:
               taken = [sub.subject_id for sub in student.subjects]
        3. Generate a new unique subject ID:
               sid = new_subject_id(taken)
        4. Generate a random mark (int):
               mark = random.randint(25, 100)
        5. Compute the grade:
               grade = compute_grade(mark)
        6. Build a Subject object:
               new_sub = Subject(sid, mark, grade)
        7. Append new_sub to student.subjects  (in-memory update).
        8. Persist the change:
               - all_students = Database.fetch_all()
               - Find the student whose student_id matches student.student_id
               - Replace its subjects list with student.subjects
               - Database.persist_all(all_students)
        9. Display the confirmation and count messages.
    """
    # TODO: implement subject enrolment
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

    display(level, f"Enrolling in Subject-{int(sid):03d}", YELLOW)
    display(level, f"You are now enrolled in {len(student.subjects)} out of 4 subjects", YELLOW)


# ---------------------------------------------------------------------------
# Show enrolled subjects
# ---------------------------------------------------------------------------

def show_subjects(level: int, student: Student) -> None:
    """
    PURPOSE:
        Display all subjects currently enrolled by the student, each with
        its subject ID, mark, and grade.

    INPUT:
        level   -- int, current terminal indentation depth
        student -- Student object whose .subjects list will be displayed

    OUTPUT:
        None.
        Prints one line per subject in the format (match sample I/O exactly):
            [Subject::<id> -- mark = <mark> -- grade = <grade>]
        If the student has no subjects enrolled, print a message such as:
            "No subjects enrolled yet"

    STEPS TO IMPLEMENT:
        1. Check if student.subjects is empty.
               If empty → display a "no subjects" message and return.
        2. Iterate over student.subjects.
        3. For each Subject object, call display() with the formatted string.

    HINT:
        The format string should look like:
            f"[Subject::{sub.subject_id} -- mark = {sub.mark} -- grade = {sub.grade}]"
    """
    # TODO: implement subject listing
    display(level, f"Showing {len(student.subjects)} subjects", YELLOW)

    for sub in student.subjects:
        display(level, f"[ Subject::{int(sub.subject_id):03d} -- mark = {sub.mark} -- grade = {sub.grade:>3} ]")


# ---------------------------------------------------------------------------
# Remove a subject
# ---------------------------------------------------------------------------

def remove_subject(level: int, student: Student) -> None:
    """
    PURPOSE:
        Let the student remove one enrolled subject by entering its 3-digit ID.
        The updated enrolment list is persisted to students.data.

    INPUT:
        level   -- int, current terminal indentation depth
        student -- Student object; its .subjects list will be modified on success

    OUTPUT:
        None.
        Success path:
            - The subject is removed from student.subjects (in-memory).
            - students.data is updated.
            - A confirmation line is displayed, e.g.:
                  "Dropping Subject-042"
            - A count line is displayed, e.g.:
                  "You are now enrolled in 2 out of 4 subjects"
        Failure path (ID not found):
            - Display an error message and return without making changes.

    STEPS TO IMPLEMENT:
        1. Use prompt(level, "Remove Subject by ID: ") to get the subject ID.
        2. Call student.find_subject(entered_id) to verify it exists.
               If None → display an error and return.
        3. Call student.drop_subject(entered_id)  (modifies in-memory list).
        4. Persist:
               - all_students = Database.fetch_all()
               - Find this student by student_id
               - Replace its subjects with student.subjects
               - Database.persist_all(all_students)
        5. Display the confirmation and updated count.
    """
    # TODO: implement subject removal
    entered_id = prompt(level, "Remove Subject by ID: ", CYAN).strip()

    subject = student.find_subject(entered_id)

    if subject is None:
        display(level, f"Subject-{int(entered_id):03d} not found", RED)
        return

    student.drop_subject(entered_id)

    all_students = Database.fetch_all()

    for s in all_students:
        if s.student_id == student.student_id:
            s.subjects = student.subjects
            break

    Database.persist_all(all_students)

    display(level, f"Dropping Subject-{int(entered_id):03d}", YELLOW)
    display(level, f"You are now enrolled in {len(student.subjects)} out of 4 subjects", YELLOW)


# ---------------------------------------------------------------------------
# Change password
# ---------------------------------------------------------------------------

def change_password(level: int, student: Student) -> None:
    """
    PURPOSE:
        Allow the logged-in student to set a new account password.
        The new password is validated with the same regex used at registration.
        The student must confirm the new password by typing it a second time.
        Reusing the current password is allowed (no special check required).
        The change is written to students.data.

    INPUT:
        level   -- int, current terminal indentation depth
        student -- Student object whose .password will be updated on success

    OUTPUT:
        None.
        On success: student.password is updated in-memory AND in students.data.
        On format failure: display an error and re-prompt for a new password.
        On confirmation mismatch: display an error and re-prompt confirmation only.

    STEPS TO IMPLEMENT:
        1. Display "Updating Password" (or similar heading).
        2. Loop A — get a valid new password:
               a. prompt(level, "New Password: ") to read new_pw
               b. is_valid_password(new_pw) → if False, display error, continue loop A
               c. Break out of loop A once a valid password is entered.
        3. Loop B — confirm the password:
               a. prompt(level, "Confirm Password: ") to read confirmation
               b. If confirmation != new_pw → display error, continue loop B
               c. Once they match, proceed.
        4. Persist:
               - all_students = Database.fetch_all()
               - Find student by student_id, set s.password = new_pw
               - Database.persist_all(all_students)
        5. Update in-memory: student.password = new_pw
        6. Display a success message.
    """
    # TODO: implement password change
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
            display(level, "Password does not match - try again", RED)
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
