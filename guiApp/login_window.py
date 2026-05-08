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

_ERROR_MESSAGES = {
    "empty":           "Email and password must not be empty.",
    "invalid_email":   "Invalid email format.\nUse: firstname.lastname@university.com",
    "no_such_student": "Student does not exist.",
    "bad_password":    "Incorrect password.",
}


class LoginWindow(tk.Tk):
    """Root Tk window — the starting point of GUIUniApp."""

    def __init__(self, db: DatabaseManager) -> None:
        super().__init__()
        self.db = db
        self.title("GUIUniApp - Login")
        self.geometry("600x300")
        self.resizable(False, False)
        self.configure(padx=30, pady=30)

        # Email row
        tk.Label(self, text="Email:", font=("Arial", 12), anchor="w").pack(fill="x")
        self.email_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.email_var, width=50).pack(fill="x", pady=(2, 12))

        # Password row
        tk.Label(self, text="Password:", font=("Arial", 12), anchor="w").pack(fill="x")
        self.pw_var = tk.StringVar()
        ttk.Entry(self, textvariable=self.pw_var, show="*", width=50).pack(fill="x", pady=(2, 20))

        # Buttons
        btn_frame = tk.Frame(self)
        btn_frame.pack()
        ttk.Button(btn_frame, text="Login", width=12, command=self._handle_login).pack(side="left", padx=8)
        ttk.Button(btn_frame, text="Exit",  width=12, command=self.destroy).pack(side="left", padx=8)

        self.bind("<Return>", lambda e: self._handle_login())
        self._enrol_win = None

    # -----------------------------------------------------------------------
    # Event handlers
    # -----------------------------------------------------------------------

    def _handle_login(self) -> None:
        email = self.email_var.get().strip()
        pw    = self.pw_var.get().strip()
        ok, code = self.db.authenticate(email, pw)
        if not ok:
            msg = _ERROR_MESSAGES.get(code, "An unexpected error occurred.")
            ExceptionWindow(self, msg)
            return
        self.withdraw()
        self._enrol_win = EnrolmentWindow(self, self.db, email, on_back=self._on_back)

    def _on_back(self) -> None:
        self.deiconify()
