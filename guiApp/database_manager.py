
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

    if mark >= 85:
        return "HD"
    if mark >= 75:
        return "D"
    if mark >= 65:
        return "C"
    if mark >= 50:
        return "P"
    return "Z"


# ---------------------------------------------------------------------------
# DatabaseManager class
# ---------------------------------------------------------------------------

class DatabaseManager:

    def __init__(self, data_path: Optional[str] = None) -> None:
        if data_path is not None:
            self.path = data_path
        else:
            pkg_dir      = os.path.dirname(os.path.abspath(__file__))
            project_root = os.path.dirname(pkg_dir)
            self.path    = os.path.join(project_root, "students.data")
        self._ensure_file()

    # -----------------------------------------------------------------------
    # Public API
    # -----------------------------------------------------------------------

    def authenticate(self, email: str, password: str) -> Tuple[bool, str]:

        email    = email.strip()
        password = password.strip()
        if not email or not password:
            return (False, "empty")
        if not _EMAIL_PATTERN.match(email):
            return (False, "invalid_email")
        students = self._read()
        match = next((s for s in students if s.get("email") == email), None)
        if match is None:
            return (False, "no_such_student")
        if match["password"] != password:
            return (False, "bad_password")
        return (True, "")

    def get_student(self, email: str) -> Dict:

        students = self._read()
        match = next((s for s in students if s.get("email") == email), None)
        if match is None:
            raise KeyError("Student not found")
        match.setdefault("subjects", [])
        return match

    def enrol_new_subject(self, email: str) -> Dict:

        student  = self.get_student(email)
        subjects = student.setdefault("subjects", [])
        if len(subjects) >= 4:
            raise ValueError("limit_reached")
        existing_ids = {s["id"] for s in subjects}
        while True:
            new_id = f"{random.randint(1, 999):03d}"
            if new_id not in existing_ids:
                break
        mark        = random.randint(25, 100)
        grade       = _compute_grade(mark)
        new_subject = {"id": new_id, "mark": mark, "grade": grade}
        subjects.append(new_subject)
        self.save_student(student)
        return new_subject

    def delete_subject(self, email: str, subject_id) -> None:

        student        = self.get_student(email)
        sid            = str(subject_id).zfill(3)
        original_count = len(student["subjects"])
        student["subjects"] = [
            s for s in student["subjects"]
            if str(s.get("id")).zfill(3) != sid
        ]
        if len(student["subjects"]) != original_count:
            self.save_student(student)

    def save_student(self, student: Dict) -> None:

        students = self._read()
        for i, s in enumerate(students):
            if s["email"] == student["email"]:
                students[i] = student
                self._write(students)
                return
        students.append(student)
        self._write(students)

    # -----------------------------------------------------------------------
    # Private helpers
    # -----------------------------------------------------------------------

    def _ensure_file(self) -> None:
        """Create students.data with an empty JSON array if it does not exist."""
        if not os.path.exists(self.path):
            with open(self.path, "w") as f:
                f.write("[]")

    def _read(self) -> List[Dict]:
        """Read students.data and return the list of student dicts."""
        try:
            with open(self.path, "r") as f:
                return json.load(f)
        except Exception:
            return []

    def _write(self, students: List[Dict]) -> None:
        """Overwrite students.data with the given list (pretty-printed JSON)."""
        with open(self.path, "w") as f:
            json.dump(students, f, indent=2)
