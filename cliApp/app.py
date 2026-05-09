
from .cli.university_menu import run_university_menu
from .cli.ui import display, YELLOW


if __name__ == "__main__":
    try:
        run_university_menu()
    except KeyboardInterrupt:
        print()
        display(0, "Session interrupted. Thank You.", YELLOW)
