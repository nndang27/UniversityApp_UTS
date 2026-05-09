

from .ui import display, prompt, CYAN, YELLOW, RED, SUBMENU_JUMP
from ..core.db import Database
from .student_controller import run_student_menu
from .admin_controller import run_admin_menu


def run_university_menu() -> None:

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
