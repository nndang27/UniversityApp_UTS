"""
cliApp/cli/university_menu.py
=============================
OWNER: Person 1

Top-level University System menu for CLIUniApp.
This is the first menu the user sees after launching the application.

Marking criteria covered here (4 marks):
    - (A) navigates to Admin subsystem          [1 mark]
    - (S) navigates to Student subsystem        [1 mark]
    - browsing back and forth between them      [1 mark]
    - I/O wording and indentation match sample  [1 mark]
"""

from .ui import display, prompt, CYAN, YELLOW, RED, SUBMENU_JUMP
from ..core.db import Database
from .student_controller import run_student_menu
from .admin_controller import run_admin_menu


def run_university_menu() -> None:
    """
    Entry point for the CLIUniApp interactive session.

    Initialises the database file, then loops presenting the University System
    menu until the user chooses to exit.

    Input:  (none — called directly from cliApp/app.py)
    Output: None  (prints menus to stdout, returns when user enters X)

    Menu options:
        A  →  open the Admin subsystem
        S  →  open the Student subsystem
        X  →  print "Thank You" and exit
        *  →  print an error and repeat the prompt
    """
    Database.initialise()
    level = 0

    while True:
        choice = prompt(
            level,
            "University System (A)dmin, (S)tudent, or X to exit: ",
            CYAN,
        ).lower()

        if choice == "a":
            run_admin_menu(level + SUBMENU_JUMP)
        elif choice == "s":
            run_student_menu(level + SUBMENU_JUMP)
        elif choice == "x":
            display(level, "Thank You", YELLOW)
            return
        else:
            display(level, "Invalid option. Please enter A, S, or X.", RED)
