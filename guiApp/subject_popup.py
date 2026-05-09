
import tkinter as tk
from tkinter import ttk


class SubjectPopup(tk.Toplevel):
    """Read-only modal detail view for one enrolled subject."""

    def __init__(self, parent, subject: dict) -> None:
        super().__init__(parent)
        self.title("Subject Details")
        self.resizable(False, False)
        self.configure(padx=24, pady=24)
        self.transient(parent)
        self.grab_set()

        subj_id = subject.get("id", "?")
        mark    = subject.get("mark", "-")
        grade   = subject.get("grade", "-")

        tk.Label(
            self,
            text=f"subject-{subj_id}",
            font=("Arial", 16, "bold"),
        ).pack(pady=(0, 12))

        tk.Label(self, text=f"mark:  {mark}",  font=("Arial", 13)).pack(anchor="w")
        tk.Label(self, text=f"grade: {grade}", font=("Arial", 13)).pack(anchor="w", pady=(4, 16))

        ttk.Button(self, text="Close", width=10, command=self.destroy).pack()

        self.bind("<Escape>", lambda e: self.destroy())
        self.wait_visibility()
        self.focus_set()
