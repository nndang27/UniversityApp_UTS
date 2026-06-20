"""
cliApp/core/db.py
=================
OWNER: Person 1

Persistence layer for CLIUniApp.
All reads from and writes to students.data go through this class.
The file is stored in the current working directory (run from University2/).
"""

import json
from pathlib import Path
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .models import Student

# Name of the shared data file (relative to the working directory)
DATA_FILENAME = "students.data"


class Database:
    """
    Static helper class that handles all file I/O for student records.

    students.data stores a JSON array of student objects.
    Call Database.initialise() once at application start-up to guarantee
    the file exists before any other operation is attempted.
    """

    @staticmethod
    def _file_path() -> Path:
        """
        Return the Path object pointing to students.data.

        Input:  (none)
        Output: Path("students.data") — relative to the process working directory
        """
        return Path(DATA_FILENAME)

    @staticmethod
    def initialise() -> None:
        """
        Ensure students.data exists on disk.
        Creates an empty JSON array file if the file is not already present.
        Should be called once when the application starts.

        Input:  (none)
        Output: None  (students.data is created if it was missing)
        """
        target = Database._file_path()
        if not target.exists():
            target.write_text("[]", encoding="utf-8")

    @staticmethod
    def fetch_all() -> List["Student"]:
        """
        Read every student record from students.data and return them as objects.

        Input:  (none)
        Output: list of Student instances; empty list when the file is empty or corrupt
        Side effects: calls initialise() to create the file if it is missing
        """
        from .models import Student

        Database.initialise()
        raw = Database._file_path().read_text(encoding="utf-8")
        try:
            records = json.loads(raw)
            if not isinstance(records, list):
                records = []
        except json.JSONDecodeError:
            records = []
        return [Student.deserialise(r) for r in records]

    @staticmethod
    def persist_all(students: List["Student"]) -> None:
        """
        Overwrite students.data with the current list of students.
        This replaces the entire file contents on every call.

        Input:  students -- full list of Student objects to write to disk
        Output: None  (students.data is updated)
        """
        payload = [s.serialise() for s in students]
        Database._file_path().write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )

    @staticmethod
    def wipe() -> None:
        """
        Erase all student records from students.data.
        After this call the file exists but contains an empty JSON array "[]".

        Input:  (none)
        Output: None  (students.data now contains "[]")
        """
        Database._file_path().write_text("[]", encoding="utf-8")
