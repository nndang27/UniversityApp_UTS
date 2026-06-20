"""
guiApp/database_manager.py
===========================
OWNER: Person 4  —  GUI persistence layer

PURPOSE:
    Provides all data-access methods needed by the GUI windows.
    Reads and writes the SAME students.data file used by the CLI so that
    students registered via CLIUniApp can log into GUIUniApp and vice versa.

students.data format  (JSON list at root level):
[
  {
    "id":       "042817",
    "name":     "John Smith",
    "email":    "john.smith@university.com",
    "password": "Hello123",
    "subjects": [
      {"id": "042", "mark": 73, "grade": "C"},
      ...
    ]
  },
  ...
]
"""

from __future__ import annotations

import json
import os
import random
import re
from typing import Dict, List, Optional, Tuple

# Email pattern — must match the same rule as the CLI validation
_EMAIL_PATTERN = re.compile(r"^[A-Za-z]+\.[A-Za-z]+@university\.com$")


# ---------------------------------------------------------------------------
# Module-level helper (not part of the class)
# ---------------------------------------------------------------------------

def _compute_grade(mark: int) -> str:
    """
    Convert a numeric mark to a letter grade.

    Input:  mark -- integer 25..100
    Output: "HD" (>=85), "D" (>=75), "C" (>=65), "P" (>=50), "Z" (<50)
    """
    # TODO: implement grade mapping using the same thresholds as the CLI
    # HD >= 85, D >= 75, C >= 65, P >= 50, else Z
    pass


# ---------------------------------------------------------------------------
# DatabaseManager class
# ---------------------------------------------------------------------------

class DatabaseManager:
    """
    Handles all file I/O for GUIUniApp.

    Instantiate once in guiApp/app.py and inject into every window that needs it.
    """

    def __init__(self, data_path: Optional[str] = None) -> None:
        """
        PURPOSE:
            Initialise the manager, resolve the path to students.data,
            and create the file if it does not already exist.

        INPUT:
            data_path -- optional custom path string.
                         Leave as None to use the default:
                         <project_root>/students.data
                         where project_root is the parent folder of guiApp/.
        OUTPUT:
            None  (sets self.path and ensures the file exists)

        STEPS TO IMPLEMENT:
            1. If data_path is not None: self.path = data_path
            2. Otherwise:
                   pkg_dir      = os.path.dirname(os.path.abspath(__file__))
                   project_root = os.path.dirname(pkg_dir)
                   self.path    = os.path.join(project_root, "students.data")
            3. Call self._ensure_file()
        """
        # TODO: resolve self.path and call self._ensure_file()
        pass

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def authenticate(self, email: str, password: str) -> Tuple[bool, str]:
        """
        PURPOSE:
            Validate a student's login credentials against students.data.
            Also validates email format before checking the file.

        INPUT:
            email    -- string from the GUI email entry field
            password -- string from the GUI password entry field (plain-text)

        OUTPUT:
            Tuple (ok: bool, code: str)
            Possible codes:
                ""                → authenticated successfully
                "empty"           → email or password is blank
                "invalid_email"   → email does not match university format
                "no_such_student" → email not found in students.data
                "bad_password"    → email found but password is wrong

        STEPS TO IMPLEMENT:
            1. Strip whitespace from both inputs.
            2. If either is empty → return (False, "empty").
            3. If not _EMAIL_PATTERN.match(email) → return (False, "invalid_email").
            4. Call self._read() to get all student dicts.
            5. Find first dict whose "email" == email (exact match).
            6. If not found → return (False, "no_such_student").
            7. If dict["password"] != password → return (False, "bad_password").
            8. Return (True, "").
        """
        # TODO: implement credential validation
        pass

    def get_student(self, email: str) -> Dict:
        """
        PURPOSE:
            Return the student dict for a given email address.
            Guarantees the "subjects" key is present (defaults to []).

        INPUT:
            email -- email address of an already-authenticated student

        OUTPUT:
            student dict with keys: id, name, email, password, subjects
            Raises KeyError("Student not found") if no match exists.

        STEPS TO IMPLEMENT:
            1. students = self._read()
            2. match = next((s for s in students if s.get("email") == email), None)
            3. If match is None → raise KeyError("Student not found")
            4. match.setdefault("subjects", [])
            5. return match
        """
        # TODO: find and return the student dict
        pass

    def enrol_new_subject(self, email: str) -> Dict:
        """
        PURPOSE:
            Add a brand-new randomly generated subject to the student's list.
            Enforces the 4-subject per-student maximum.

        INPUT:
            email -- email of the logged-in student

        OUTPUT:
            The new subject dict: {"id": "...", "mark": <int>, "grade": "..."}
            Raises ValueError("limit_reached") when the student already has 4 subjects.

        STEPS TO IMPLEMENT:
            1. student = self.get_student(email)
            2. subjects = student.setdefault("subjects", [])
            3. If len(subjects) >= 4 → raise ValueError("limit_reached")
            4. Pick a unique 3-digit string ID not in [s["id"] for s in subjects]
               using random.randint(1, 999); format as f"{n:03d}"; retry on collision.
            5. mark  = random.randint(25, 100)
            6. grade = _compute_grade(mark)
            7. new_subject = {"id": new_id, "mark": mark, "grade": grade}
            8. subjects.append(new_subject)
            9. self.save_student(student)
            10. return new_subject
        """
        # TODO: implement subject enrolment with limit enforcement
        pass

    def delete_subject(self, email: str, subject_id) -> None:
        """
        PURPOSE:
            Remove a subject from the student's list by subject ID.

        INPUT:
            email      -- email of the logged-in student
            subject_id -- the subject's ID value (string or int accepted)

        OUTPUT:
            None.  File is updated only if a matching subject was found.

        STEPS TO IMPLEMENT:
            1. student  = self.get_student(email)
            2. Normalise subject_id: sid = str(subject_id).zfill(3)
            3. original_count = len(student["subjects"])
            4. student["subjects"] = [s for s in student["subjects"]
                                       if str(s.get("id")).zfill(3) != sid]
            5. If count changed → self.save_student(student)
        """
        # TODO: implement subject deletion
        pass

    def save_student(self, student: Dict) -> None:
        """
        PURPOSE:
            Update (or insert) a student dict in students.data.

        INPUT:
            student -- student dict that contains at least the "email" key

        OUTPUT:
            None.  students.data is overwritten with the updated list.

        STEPS TO IMPLEMENT:
            1. students = self._read()
            2. Iterate with enumerate; if s["email"] == student["email"]
               → replace in place and call self._write(students), then return.
            3. If no match found, append and call self._write(students).
        """
        # TODO: implement upsert by email
        pass

    # -----------------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------------

    def _ensure_file(self) -> None:
        """
        Create students.data with an empty JSON array if it does not exist.

        Input:  (none — uses self.path)
        Output: None
        """
        # TODO: if not os.path.exists(self.path): write "[]" to self.path
        pass

    def _read(self) -> List[Dict]:
        """
        Read students.data and return the list of student dicts.
        Returns [] on any read error or malformed JSON.

        Input:  (none — uses self.path)
        Output: list of dicts (may be empty)
        """
        # TODO: open self.path, json.load, return list; return [] on exception
        pass

    def _write(self, students: List[Dict]) -> None:
        """
        Overwrite students.data with the given list (pretty-printed JSON).

        Input:  students -- list of student dicts
        Output: None
        """
        # TODO: json.dump(students, f, indent=2) to self.path
        pass
