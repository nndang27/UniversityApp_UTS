"""
cliApp/core/models.py
=====================
OWNER: Person 1

Core data model classes for CLIUniApp.
Defines Subject, Student, and the grade computation function.
These classes are imported by ALL other modules — do not change
the public interface (field names, method signatures, return types).
"""

from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Grade mapping
# ---------------------------------------------------------------------------

def compute_grade(mark: int) -> str:
    """
    Convert a numeric mark to a single letter grade.

    Input:
        mark  -- integer, expected range 25..100
    Output:
        "HD"  if mark >= 85
        "D"   if mark >= 75
        "C"   if mark >= 65
        "P"   if mark >= 50
        "Z"   if mark <  50
    """
    boundaries = [(85, "HD"), (75, "D"), (65, "C"), (50, "P")]
    for floor, letter in boundaries:
        if mark >= floor:
            return letter
    return "Z"


# ---------------------------------------------------------------------------
# Subject
# ---------------------------------------------------------------------------

class Subject:
    """
    Represents a single enrolled subject.

    Fields:
        subject_id  -- 3-digit zero-padded string, e.g. "042"
        mark        -- integer 25..100 (assigned randomly on enrolment)
        grade       -- letter grade derived from mark via compute_grade()
    """

    def __init__(self, subject_id: str, mark: int, grade: str) -> None:
        self.subject_id = subject_id
        self.mark = mark
        self.grade = grade

    def serialise(self) -> Dict:
        """
        Convert this Subject to a plain dict suitable for JSON storage.

        Input:  (none — uses own fields)
        Output: dict with keys "id", "mark", "grade"
        """
        return {"id": self.subject_id, "mark": self.mark, "grade": self.grade}

    @classmethod
    def deserialise(cls, data: Dict) -> "Subject":
        """
        Rebuild a Subject from a stored dict.

        Input:  data -- dict with keys "id", "mark", "grade"
        Output: Subject instance
        """
        return cls(str(data["id"]), int(data["mark"]), str(data["grade"]))


# ---------------------------------------------------------------------------
# Student
# ---------------------------------------------------------------------------

class Student:
    """
    Represents a registered university student.

    Fields:
        student_id  -- 6-digit zero-padded string, e.g. "042817"
        name        -- display name, e.g. "John Smith"
        email       -- university email, e.g. "john.smith@university.com"
        password    -- plain-text password (validated against PASSWORD_PATTERN)
        subjects    -- list of Subject objects (max MAX_SUBJECTS)

    Class constant:
        MAX_SUBJECTS = 4
    """

    MAX_SUBJECTS = 4

    def __init__(
        self,
        student_id: str,
        name: str,
        email: str,
        password: str,
        subjects: Optional[List[Subject]] = None,
    ) -> None:
        self.student_id = student_id
        self.name = name
        self.email = email
        self.password = password
        self.subjects: List[Subject] = subjects if subjects is not None else []

    # ------------------------------------------------------------------
    # Enrolment helpers
    # ------------------------------------------------------------------

    def at_capacity(self) -> bool:
        """
        Check whether the student has reached the maximum number of subjects.

        Input:  (none — checks own subjects list)
        Output: True when len(subjects) >= MAX_SUBJECTS, False otherwise
        """
        return len(self.subjects) >= self.MAX_SUBJECTS

    def find_subject(self, subject_id: str) -> Optional[Subject]:
        """
        Look up an enrolled subject by its ID.

        Input:  subject_id -- 3-digit string to search for
        Output: matching Subject object, or None if not found
        """
        for sub in self.subjects:
            if sub.subject_id == subject_id:
                return sub
        return None

    def drop_subject(self, subject_id: str) -> bool:
        """
        Remove an enrolled subject from this student's list.

        Input:  subject_id -- ID of the subject to remove
        Output: True if the subject was found and removed, False otherwise
                (does NOT persist to file — caller must call Database.persist_all)
        """
        for index, sub in enumerate(self.subjects):
            if sub.subject_id == subject_id:
                del self.subjects[index]
                return True
        return False

    def average_mark(self) -> Optional[float]:
        """
        Compute the mean mark across all enrolled subjects.

        Input:  (none — uses own subjects list)
        Output: float average, or None if no subjects are enrolled yet
        """
        if not self.subjects:
            return None
        return sum(sub.mark for sub in self.subjects) / len(self.subjects)

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def serialise(self) -> Dict:
        """
        Convert this Student (and all nested Subject objects) to a plain dict
        suitable for JSON storage.

        Input:  (none — uses own fields)
        Output: dict with keys "id", "name", "email", "password", "subjects"
        """
        return {
            "id": self.student_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": [sub.serialise() for sub in self.subjects],
        }

    @classmethod
    def deserialise(cls, data: Dict) -> "Student":
        """
        Rebuild a Student (with all nested subjects) from a stored dict.

        Input:  data -- dict with keys "id", "name", "email", "password", "subjects"
        Output: Student instance with fully populated subjects list
        """
        subjects = [Subject.deserialise(s) for s in data.get("subjects", [])]
        return cls(
            str(data["id"]),
            str(data["name"]),
            str(data["email"]),
            str(data["password"]),
            subjects,
        )
