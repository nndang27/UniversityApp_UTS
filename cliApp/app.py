"""
cliApp/app.py
=============
OWNER: Person 1

CLI entry point for CLIUniApp.

Run from the University2/ directory:
    python3 -m cliApp.app
"""

from .cli.university_menu import run_university_menu
from .cli.ui import display, YELLOW


if __name__ == "__main__":
    try:
        run_university_menu()
    except KeyboardInterrupt:
        print()
        display(0, "Session interrupted. Thank You.", YELLOW)
