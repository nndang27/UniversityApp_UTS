"""
guiApp/login_window.py
=======================
OWNER: Person 4  —  Window 1: Login Window  (2 marks)

PURPOSE:
    The main (root) Tk window of GUIUniApp.
    Displays an email + password form.
    On successful login the window hides itself and opens EnrolmentWindow.
    On any failure it opens ExceptionWindow with an appropriate message.

MARKING CRITERIA (2 marks):
    - Students can log in using credentials stored in students.data
    - After login the enrolment window is shown
"""

import tkinter as tk
from tkinter import ttk

from .database_manager import DatabaseManager
from .enrolment_window import EnrolmentWindow
from .exception_window import ExceptionWindow


class LoginWindow(tk.Tk):
    """
    PURPOSE:
        Root Tk window — the starting point of GUIUniApp.

    WIDGETS TO BUILD inside __init__:
        - Window title: "GUIUniApp - Login"
        - A label "email" and a wide Entry field  (self.email_var = tk.StringVar())
        - A label "password" and an Entry field with hidden characters (show="*")
          (self.pw_var = tk.StringVar())
        - A "Login" button  → calls self._handle_login()
        - An "Exit"  button → calls self.destroy()
        - Optional: bind <Return> key to self._handle_login for keyboard convenience
    """

    def __init__(self, db: DatabaseManager) -> None:
        """
        PURPOSE:
            Set up and display the login window.

        INPUT:
            db -- DatabaseManager instance (created in app.py and injected here)
        OUTPUT:
            None  (window is displayed; call mainloop() after construction)

        STEPS TO IMPLEMENT:
            1. super().__init__()  to initialise Tk
            2. self.db = db
            3. self.title("GUIUniApp - Login")
            4. Set a fixed geometry, e.g. self.geometry("600x300")
            5. self.resizable(False, False)
            6. Add padding: self.configure(padx=30, pady=30)
            7. Create self.email_var = tk.StringVar()
               Add a "email" label and an Entry(textvariable=self.email_var)
            8. Create self.pw_var = tk.StringVar()
               Add a "password" label and Entry(textvariable=self.pw_var, show="*")
            9. Add a ttk.Button(text="Login", command=self._handle_login)
            10. Add a ttk.Button(text="Exit",  command=self.destroy)
            11. Optionally: self.bind("<Return>", lambda e: self._handle_login())
            12. self._enrol_win = None  (placeholder for the EnrolmentWindow reference)
        """
        # TODO: build the login window UI
        pass

    # -----------------------------------------------------------------------
    # Event handlers
    # -----------------------------------------------------------------------

    def _handle_login(self) -> None:
        """
        PURPOSE:
            Called when the Login button is pressed (or Enter is hit).
            Reads credentials, calls db.authenticate(), and acts on the result.

        INPUT:  (none — reads from self.email_var and self.pw_var)
        OUTPUT: None

        STEPS TO IMPLEMENT:
            1. email = self.email_var.get().strip()
               pw    = self.pw_var.get().strip()
            2. ok, code = self.db.authenticate(email, pw)
            3. If not ok → open ExceptionWindow(self, <message>) with the
               message matching the code:
                   "empty"           → "Email and password must not be empty."
                   "invalid_email"   → "Invalid email format.\nUse: firstname.lastname@university.com"
                   "no_such_student" → "Student does not exist."
                   "bad_password"    → "Incorrect password."
                   (default)         → "An unexpected error occurred."
               Then return.
            4. If ok:
               → self.withdraw()  (hide login window)
               → self._enrol_win = EnrolmentWindow(self, self.db, email,
                                                   on_back=self._on_back)
        """
        # TODO: implement login button handler
        pass

    def _on_back(self) -> None:
        """
        PURPOSE:
            Restore the login window when the student navigates back from
            the EnrolmentWindow.

        INPUT:  None  OUTPUT: None

        STEPS TO IMPLEMENT:
            1. self.deiconify()  — un-hide the login window
        """
        # TODO: call self.deiconify()
        pass
