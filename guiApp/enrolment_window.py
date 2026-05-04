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
    """
    PURPOSE:
        A child Toplevel window for managing subject enrolment.

    WIDGETS TO BUILD:
        - A "←" back button (top-left) → calls self._go_back()
        - A bold "enrolment" title label
        - A frame (self.list_frame) that holds the subject rows, rebuilt
          each time by _refresh_list()
        - An "Enrol" button at the bottom → calls self._enrol_one()
    """

    def __init__(
        self,
        parent: tk.Tk,
        db: DatabaseManager,
        email: str,
        on_back,
    ) -> None:
        """
        PURPOSE:
            Initialise and display the enrolment window.

        INPUT:
            parent  -- the LoginWindow (root Tk window)
            db      -- DatabaseManager instance
            email   -- email address of the currently logged-in student
            on_back -- callback function; call it when the student closes this window
        OUTPUT:
            None  (builds and shows the window)

        STEPS TO IMPLEMENT:
            1. super().__init__(parent)
            2. self.db = db; self.email = email; self.on_back = on_back
            3. self.title("GUIUniApp - Enrolment")
            4. self.geometry("620x420"); self.configure(padx=20, pady=20)
            5. Build the back button, title label, self.list_frame, and Enrol button.
            6. Call self._refresh_list() to populate subjects on first open.
            7. self.protocol("WM_DELETE_WINDOW", self._go_back) so closing the window
               via the OS "×" button also triggers the back callback.
        """
        # TODO: build the enrolment window UI
        pass

    # -----------------------------------------------------------------------
    # Subject list
    # -----------------------------------------------------------------------

    def _refresh_list(self) -> None:
        """
        PURPOSE:
            Rebuild the displayed subject list using the latest data from the database.
            Called once on construction and again after every enrol/delete action.

        INPUT:  None  OUTPUT: None

        STEPS TO IMPLEMENT:
            1. Destroy all existing child widgets inside self.list_frame.
            2. student = self.db.get_student(self.email)
            3. subjects = student.get("subjects", [])
            4. For each subject dict in subjects, create a row frame containing:
                   a. A button labelled "Subject-<id>"
                      → command = lambda subj=subject: self._open_subject(subj)
                   b. A small delete button labelled "🗑"
                      → command = lambda sid=subject["id"]: self._remove_subject(sid)
            5. If subjects is empty, display a "No subjects enrolled" label.

        HINT:
            Use a lambda with a default argument (subj=subject) to capture
            the current subject in the loop, e.g.:
                command=lambda subj=s: self._open_subject(subj)
        """
        # TODO: rebuild the subject list display
        pass

    # -----------------------------------------------------------------------
    # Actions
    # -----------------------------------------------------------------------

    def _enrol_one(self) -> None:
        """
        PURPOSE:
            Called when the "Enrol" button is pressed.
            Asks the database to add a new random subject.
            Refreshes the list on success.
            Opens ExceptionWindow if the student is already at the 4-subject limit.

        INPUT:  None  OUTPUT: None

        STEPS TO IMPLEMENT:
            1. try:
                   self.db.enrol_new_subject(self.email)
                   self._refresh_list()
               except ValueError as err:
                   if str(err) == "limit_reached":
                       ExceptionWindow(self, "You can only enrol in a maximum of 4 subjects.")
                   else:
                       ExceptionWindow(self, "An error occurred while enrolling.")
        """
        # TODO: implement enrol button handler with exception handling
        pass

    def _remove_subject(self, subject_id: str) -> None:
        """
        PURPOSE:
            Delete the specified subject from the student's enrolment list
            and refresh the displayed list.

        INPUT:
            subject_id -- 3-digit ID string of the subject to remove
        OUTPUT:
            None

        STEPS TO IMPLEMENT:
            1. self.db.delete_subject(self.email, subject_id)
            2. self._refresh_list()
        """
        # TODO: implement delete button handler
        pass

    def _open_subject(self, subject: dict) -> None:
        """
        PURPOSE:
            Open a SubjectPopup modal window showing the subject's details.

        INPUT:
            subject -- dict with keys "id", "mark", "grade"
        OUTPUT:
            None  (opens a new Toplevel window)

        STEPS TO IMPLEMENT:
            1. SubjectPopup(self, subject)
        """
        # TODO: open the subject detail popup
        pass

    def _go_back(self) -> None:
        """
        PURPOSE:
            Close this window and restore the login window by invoking on_back.

        INPUT:  None  OUTPUT: None

        STEPS TO IMPLEMENT:
            1. self.destroy()
            2. if callable(self.on_back): self.on_back()
        """
        # TODO: destroy window and invoke the back callback
        pass
