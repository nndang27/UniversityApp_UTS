
from typing import Dict, List, Optional


# ---------------------------------------------------------------------------
# Grade mapping
# ---------------------------------------------------------------------------

def compute_grade(mark: int) -> str:

    boundaries = [(85, "HD"), (75, "D"), (65, "C"), (50, "P")]
    for floor, letter in boundaries:
        if mark >= floor:
            return letter
    return "Z"


# ---------------------------------------------------------------------------
# Subject
# ---------------------------------------------------------------------------

class Subject:

    def __init__(self, subject_id: str, mark: int, grade: str) -> None:
        self.subject_id = subject_id
        self.mark = mark
        self.grade = grade

    def serialise(self) -> Dict:

        return {"id": self.subject_id, "mark": self.mark, "grade": self.grade}

    @classmethod
    def deserialise(cls, data: Dict) -> "Subject":

        return cls(str(data["id"]), int(data["mark"]), str(data["grade"]))


# ---------------------------------------------------------------------------
# Student
# ---------------------------------------------------------------------------

class Student:

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

        return len(self.subjects) >= self.MAX_SUBJECTS

    def find_subject(self, subject_id: str) -> Optional[Subject]:

        for sub in self.subjects:
            if sub.subject_id == subject_id:
                return sub
        return None

    def drop_subject(self, subject_id: str) -> bool:

        for index, sub in enumerate(self.subjects):
            if sub.subject_id == subject_id:
                del self.subjects[index]
                return True
        return False

    def average_mark(self) -> Optional[float]:

        if not self.subjects:
            return None
        return sum(sub.mark for sub in self.subjects) / len(self.subjects)

    # ------------------------------------------------------------------
    # Serialisation
    # ------------------------------------------------------------------

    def serialise(self) -> Dict:

        return {
            "id": self.student_id,
            "name": self.name,
            "email": self.email,
            "password": self.password,
            "subjects": [sub.serialise() for sub in self.subjects],
        }

    @classmethod
    def deserialise(cls, data: Dict) -> "Student":

        subjects = [Subject.deserialise(s) for s in data.get("subjects", [])]
        return cls(
            str(data["id"]),
            str(data["name"]),
            str(data["email"]),
            str(data["password"]),
            subjects,
        )
