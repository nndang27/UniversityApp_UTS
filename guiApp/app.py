"""
guiApp/app.py
=============
OWNER: Person 4  —  GUI entry point

PURPOSE:
    Bootstrap GUIUniApp: create the database manager, open the login window,
    and start the Tkinter event loop.

HOW TO RUN (from the University2/ directory):
    python3 -m guiApp.app
"""

from .database_manager import DatabaseManager
from .login_window import LoginWindow


def main() -> None:
    db  = DatabaseManager()
    app = LoginWindow(db)
    app.mainloop()


if __name__ == "__main__":
    main()
