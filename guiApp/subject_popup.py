"""
guiApp/subject_popup.py
========================
OWNER: Person 4  —  Window 3: Subject Detail Popup  (2 marks)

PURPOSE:
    A modal Toplevel window that shows the details of a single enrolled subject:
    subject ID, mark, and grade.
    Blocks all interaction with the EnrolmentWindow until the user closes it.

MARKING CRITERIA (2 marks):
    - Enrolled subjects with their marks and grades are displayed
"""

import tkinter as tk
from tkinter import ttk


class SubjectPopup(tk.Toplevel):
    """
    PURPOSE:
        Read-only modal detail view for one enrolled subject.

    WIDGETS TO BUILD:
        - A bold title label showing the subject ID, e.g. "subject-042"
        - A label showing the mark,  e.g. "mark: 73"
        - A label showing the grade, e.g. "grade: C"
        - A "Close" button → self.destroy()
    """

    def __init__(self, parent, subject: dict) -> None:
        """
        PURPOSE:
            Build and display the subject detail popup as a blocking modal.

        INPUT:
            parent  -- the EnrolmentWindow (the Toplevel that owns this popup)
            subject -- dict with keys "id", "mark", "grade"
        OUTPUT:
            None  (builds and shows the popup; blocks parent until dismissed)

        STEPS TO IMPLEMENT:
            1. super().__init__(parent)
            2. self.title("Subject Details")
            3. self.resizable(False, False)
            4. self.configure(padx=24, pady=24)
            5. self.transient(parent)   — keep popup above the parent window
            6. self.grab_set()          — block interaction with the parent
            7. Read subject data:
                   subj_id = subject.get("id", "?")
                   mark    = subject.get("mark", "-")
                   grade   = subject.get("grade", "-")
            8. Add a bold title label: f"subject-{subj_id}"  (large font)
            9. Add a label: f"mark: {mark}"
            10. Add a label: f"grade: {grade}"
            11. Add a "Close" ttk.Button → command=self.destroy
            12. self.bind("<Escape>", lambda e: self.destroy())
            13. self.wait_visibility()
            14. self.focus_set()
        """
        # TODO: build the subject detail popup UI
        pass
