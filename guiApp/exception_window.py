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
        super().__init__(parent)
        self.title("Error")
        self.resizable(False, False)
        self.configure(padx=28, pady=28)
        self.transient(parent)
        self.grab_set()

        tk.Label(
            self,
            text="⚠  " + message,
            font=("Arial", 13),
            justify="left",
            wraplength=340,
        ).pack(anchor="w")

        tk.Frame(self, height=16).pack()

        ttk.Button(self, text="OK", width=10, command=self.destroy).pack()

        self.bind("<Return>", lambda e: self.destroy())
        self.bind("<Escape>", lambda e: self.destroy())
        self.wait_visibility()
        self.focus_set()
