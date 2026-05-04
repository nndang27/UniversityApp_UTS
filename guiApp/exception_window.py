"""
guiApp/exception_window.py
===========================
OWNER: Person 4  —  Window 4: Exception Window  (1 mark)

PURPOSE:
    A dedicated reusable modal error-notification window.
    Used throughout GUIUniApp to inform the user of invalid actions or
    formatting errors — for example:
        - Empty email or password fields
        - Email that does not match the university format
        - Student credentials not found
        - Attempt to enrol in more than 4 subjects

    This is a separate Toplevel class (not messagebox.showerror) in order
    to satisfy the assignment requirement for a 4th distinct GUI window.

MARKING CRITERIA (1 mark):
    - Notifies users of format errors and exceeding the 4-subject limit

USAGE:
    ExceptionWindow(parent_widget, "Your error message here")
"""

import tkinter as tk
from tkinter import ttk


class ExceptionWindow(tk.Toplevel):
    """
    PURPOSE:
        Reusable modal popup for displaying error / exception messages.

    WIDGETS TO BUILD:
        - A "⚠" warning symbol + the error message as a label (larger font)
        - An "OK" button → self.destroy()
    """

    def __init__(self, parent, message: str) -> None:
        """
        PURPOSE:
            Display a modal error-notification popup.

        INPUT:
            parent  -- the window that triggered the error
                       (LoginWindow or EnrolmentWindow)
            message -- human-readable description of the error (string)
        OUTPUT:
            None  (builds and shows the popup; blocks parent until dismissed)

        STEPS TO IMPLEMENT:
            1. super().__init__(parent)
            2. self.title("Error")
            3. self.resizable(False, False)
            4. self.configure(padx=28, pady=28)
            5. self.transient(parent)   — keep above the triggering window
            6. self.grab_set()          — block parent interaction
            7. Add a label with text "⚠  " + message
               Use a medium-large font, e.g. ("Arial", 13)
            8. Add a spacer or padding between the message and button
            9. Add a "OK" ttk.Button with width=10 → command=self.destroy
            10. self.bind("<Return>", lambda e: self.destroy())
            11. self.bind("<Escape>", lambda e: self.destroy())
            12. self.wait_visibility()
            13. self.focus_set()
        """
        # TODO: build the exception window UI
        pass
