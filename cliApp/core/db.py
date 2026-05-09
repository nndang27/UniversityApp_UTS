
import json
from pathlib import Path
from typing import TYPE_CHECKING, List

if TYPE_CHECKING:
    from .models import Student

# Name of the shared data file (relative to the working directory)
DATA_FILENAME = "students.data"


class Database:

    @staticmethod
    def _file_path() -> Path:
 
        return Path(DATA_FILENAME)

    @staticmethod
    def initialise() -> None:

        target = Database._file_path()
        if not target.exists():
            target.write_text("[]", encoding="utf-8")

    @staticmethod
    def fetch_all() -> List["Student"]:
 
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
 
        payload = [s.serialise() for s in students]
        Database._file_path().write_text(
            json.dumps(payload, indent=2), encoding="utf-8"
        )

    @staticmethod
    def wipe() -> None:

        Database._file_path().write_text("[]", encoding="utf-8")
