"""
guiApp/enrolment_window.py
===========================
OWNER: Person 4  —  Window 2: Enrolment Window  (2 marks)

PURPOSE:
    Shown immediately after a student successfully logs in.
    Lists the student's currently enrolled subjects as clickable rows.
    Provides an "Enrol" button to add a new random subject (max 4 total).
    Each row also has a delete "🗑" button to drop that subject.
    Clicking a subject name opens SubjectPopup (Window 3) for details.
    Trying to enrol beyond 4 subjects opens ExceptionWindow (Window 4).

MARKING CRITERIA (2 marks):
    - Student can enrol in up to 4 subjects
    - Subject list updates correctly in the window
"""

import tkinter as tk
from tkinter import ttk

from .database_manager import DatabaseManager
from .subject_popup import SubjectPopup
from .exception_window import ExceptionWindow


class EnrolmentWindow(tk.Toplevel):
    """A child Toplevel window for managing subject enrolment."""

    def __init__(
        self,
        parent: tk.Tk,
        db: DatabaseManager,
        email: str,
        on_back,
    ) -> None:
        super().__init__(parent)
        self.db      = db
        self.email   = email
        self.on_back = on_back

        self.title("GUIUniApp - Enrolment")
        self.geometry("620x420")
        self.configure(padx=20, pady=20)

        # Top bar: back button + title
        top = tk.Frame(self)
        top.pack(fill="x", pady=(0, 10))
        ttk.Button(top, text="←", width=3, command=self._go_back).pack(side="left")
        tk.Label(top, text="Enrolment", font=("Arial", 16, "bold")).pack(side="left", padx=12)

        # Subject list frame (rebuilt on each change)
        self.list_frame = tk.Frame(self)
        self.list_frame.pack(fill="both", expand=True, pady=8)

        # Enrol button at the bottom
        ttk.Button(self, text="Enrol", width=14, command=self._enrol_one).pack(pady=(8, 0))

        self._refresh_list()
        self.protocol("WM_DELETE_WINDOW", self._go_back)

    # -----------------------------------------------------------------------
    # Subject list
    # -----------------------------------------------------------------------

    def _refresh_list(self) -> None:
        for widget in self.list_frame.winfo_children():
            widget.destroy()

        student  = self.db.get_student(self.email)
        subjects = student.get("subjects", [])

        if not subjects:
            tk.Label(
                self.list_frame,
                text="No subjects enrolled.",
                font=("Arial", 11),
                fg="grey",
            ).pack(anchor="w", padx=4, pady=4)
            return

        for subject in subjects:
            row = tk.Frame(self.list_frame)
            row.pack(fill="x", pady=3)

            ttk.Button(
                row,
                text=f"Subject-{subject['id']}",
                width=20,
                command=lambda subj=subject: self._open_subject(subj),
            ).pack(side="left", padx=(0, 8))

            ttk.Button(
                row,
                text="🗑",
                width=3,
                command=lambda sid=subject["id"]: self._remove_subject(sid),
            ).pack(side="left")

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    def _enrol_one(self) -> None:
        try:
            self.db.enrol_new_subject(self.email)
            self._refresh_list()
        except ValueError as err:
            if str(err) == "limit_reached":
                ExceptionWindow(self, "You can only enrol in a maximum of 4 subjects.")
            else:
                ExceptionWindow(self, "An error occurred while enrolling.")

    def _remove_subject(self, subject_id: str) -> None:
        self.db.delete_subject(self.email, subject_id)
        self._refresh_list()

    def _open_subject(self, subject: dict) -> None:
        SubjectPopup(self, subject)

    def _go_back(self) -> None:
        self.destroy()
        if callable(self.on_back):
            self.on_back()
