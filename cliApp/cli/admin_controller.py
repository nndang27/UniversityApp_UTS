"""
cliApp/cli/admin_controller.py
================================
OWNER: Person 3  —  Admin System  (15 marks)

This file contains the Admin System menu and all admin operations.
Admins do NOT need to log in — they access the menu directly from
the University menu.

Marking criteria you are responsible for (15 marks total):
    - Show all students                         [1 mark]
    - Group students by grade                   [2 marks]
    - Partition students into PASS / FAIL       [2 marks]
    - Remove a student by ID                    [2 marks]
    - Clear the database (all students)         [2 marks]
    - Read / write to students.data             [3 marks]
    - Error handling                            [2 marks]
    - I/O matches sample output                 [1 mark]

DO NOT modify any file outside this file.
All imports you will need are already listed below.
"""

from .ui import display, prompt, CYAN, YELLOW, RED
from ..core.db import Database
from ..core.models import Student, compute_grade


# ---------------------------------------------------------------------------
# Admin menu  (called by university_menu.py)
# ---------------------------------------------------------------------------

def run_admin_menu(level: int) -> None:
    """
    PURPOSE:
        Admin System menu loop.
        Stays open until the admin chooses (x) to return to the University menu.
        Each option delegates to one of the helper functions defined below.

    INPUT:
        level -- int, current terminal indentation depth

    OUTPUT:
        None.  Returns to run_university_menu() when the user enters x.

    MENU OPTIONS TO HANDLE:
        c  →  call clear_database(level)
        g  →  call group_by_grade(level)
        p  →  call partition_pass_fail(level)
        r  →  call remove_student(level)
        s  →  call show_students(level)
        x  →  return  (exit back to University menu)
        *  →  display an "Invalid option" message and loop again

    HINT:
        Use prompt(level, "...", CYAN) to read the user's choice.
    """
    # TODO: implement the admin menu loop
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
    """
    PURPOSE:
        Display every registered student currently stored in students.data.

    INPUT:
        level -- int, current terminal indentation depth

    OUTPUT:
        None.
        Prints a heading "Student List" followed by one line per student.
        Format per student (match sample I/O exactly):
            <name> :: <student_id> --> Email: <email>
        Example:
            John Smith :: 042817 --> Email: john.smith@university.com
        If students.data contains no records, print (with extra indentation):
            <Nothing to Display>

    STEPS TO IMPLEMENT:
        1. Call Database.fetch_all() to get the list of Student objects.
        2. If the list is empty:
               display(level + 2, "<Nothing to Display>") and return.
        3. display(level, "Student List", YELLOW) as a heading.
        4. Iterate and display each student in the required format.
    """
       # TODO: implement student listing
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
    """
    PURPOSE:
        Group all students by their overall grade (derived from their average mark)
        and print each non-empty group.

    INPUT:
        level -- int, current terminal indentation depth

    OUTPUT:
        None.
        Prints one line per non-empty grade bucket in the order: Z, P, C, D, HD.
        Students with no enrolled subjects are placed in a separate "N/A" bucket.
        If there are no students at all, print "<Nothing to Display>" (extra indent).

        Format per bucket (match sample I/O exactly):
            <GRADE> --> [<entry>, <entry>, ...]
        Format per entry inside the brackets:
            <name> :: <student_id> --> GRADE: <G> - MARK: <avg:.2f>
        Example line:
            C --> [John Smith :: 042817 --> GRADE: C - MARK: 68.50]

    STEPS TO IMPLEMENT:
        1. Call Database.fetch_all().
        2. If empty → display "<Nothing to Display>" (level + 2) and return.
        3. Create a dict:
               buckets = {"N/A": [], "Z": [], "P": [], "C": [], "D": [], "HD": []}
        4. For each student:
               avg = student.average_mark()
               if avg is None  → append student's entry string to buckets["N/A"]
               else:
                   grade = compute_grade(round(avg))
                   avg_str = f"{avg:.2f}"
                   entry = f"{student.name} :: {student.student_id} --> GRADE: {grade} - MARK: {avg_str}"
                   append entry to buckets[grade]
        5. Print the "N/A" bucket only if non-empty.
        6. Print Z, P, C, D, HD buckets in that order, only if non-empty.
    """
    # TODO: implement grade grouping
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
    """
    PURPOSE:
        Partition all students into PASS (average mark >= 50) or FAIL (< 50),
        with a third N/A group for students who have no enrolled subjects.
        Always print all three groups, even when empty.

    INPUT:
        level -- int, current terminal indentation depth

    OUTPUT:
        None.
        Always prints exactly three lines (match sample I/O exactly):
            N/A  -->[<entries>]
            FAIL -->[<entries>]
            PASS -->[<entries>]
        Format per entry:
            <name> :: <student_id> --> GRADE: <G> - MARK: <avg:.2f>
        Example (non-empty PASS, empty others):
            N/A  -->[]
            FAIL -->[]
            PASS -->[John Smith :: 042817 --> GRADE: C - MARK: 68.50]

    STEPS TO IMPLEMENT:
        1. Call Database.fetch_all().
        2. Create buckets:
               buckets = {"N/A": [], "FAIL": [], "PASS": []}
        3. For each student:
               avg = student.average_mark()
               if avg is None → "N/A"
               elif avg >= 50 → "PASS"
               else           → "FAIL"
               Build entry string: f"{name} :: {id} --> GRADE: {grade} - MARK: {avg:.2f}"
               (For N/A entries you may omit GRADE/MARK or use a placeholder.)
        4. Print all three buckets in order: N/A, FAIL, PASS.
               Whether empty or not, every bucket must appear.

    HINT:
        Build the comma-separated list with ", ".join(buckets["PASS"]) etc.
    """
    # TODO: implement pass/fail partition
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
    """
    PURPOSE:
        Remove a single student from students.data by their 6-digit student ID.

    INPUT:
        level -- int, current terminal indentation depth

    OUTPUT:
        None.
        Success path:
            - Student is removed from the list and students.data is updated.
            - Display a confirmation, e.g.:
                  "Removing Student 042817 Account"
        Failure path (ID not found):
            - Display an error message and return without changing the file.

    STEPS TO IMPLEMENT:
        1. Use prompt(level, "Remove by ID: ") to get the ID string.
        2. Call Database.fetch_all().
        3. Search for a student whose student_id matches the entered string.
        4. If not found → display error (e.g. "Student <id> does not exist") and return.
        5. Remove that student from the list.
        6. Call Database.persist_all(updated_list) to save.
        7. Display a confirmation message.
    """
    # TODO: implement student removal
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
    """
    PURPOSE:
        Erase every student record from students.data after admin confirmation.

    INPUT:
        level -- int, current terminal indentation depth

    OUTPUT:
        None.
        If confirmed (Y): calls Database.wipe(), displays a success message.
        If declined (N):  returns immediately without any changes.

    STEPS TO IMPLEMENT:
        1. Display "Clearing students database" as a heading.
        2. Use prompt() to ask:
               "Are you sure you want to clear the database (Y)ES/(N)O: "
        3. Strip and upper-case the input.
        4. If the answer is "Y":
               Database.wipe()
               display a success message (e.g. "Student data cleared")
        5. Otherwise: return without making changes.
    """
    # TODO: implement database clearing
    answer = prompt(level, "Clear database? Y/N: ", CYAN)

    if answer.upper() == "Y":
        Database.persist_all([])
        display(level, "Students data cleared", YELLOW)
    else:
        display(level, "Clear cancelled", RED)
