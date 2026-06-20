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
    """
    PURPOSE:
        Entry point for GUIUniApp.
        Creates a DatabaseManager, opens the LoginWindow (root Tk window),
        and hands control to the Tkinter event loop.

    INPUT:  None
    OUTPUT: None  (blocks until all GUI windows are closed)

    STEPS TO IMPLEMENT:
        1. db  = DatabaseManager()
        2. app = LoginWindow(db)
        3. app.mainloop()
    """
    # TODO: implement main() — create DatabaseManager, LoginWindow, call mainloop()
    pass


if __name__ == "__main__":
    main()
