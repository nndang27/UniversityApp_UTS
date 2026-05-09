
import random
from typing import List


def new_student_id(existing: List[str]) -> str:

    while True:
        candidate = f"{random.randint(1, 999_999):06d}"
        if candidate not in existing:
            return candidate


def new_subject_id(existing: List[str]) -> str:

    while True:
        candidate = f"{random.randint(1, 999):03d}"
        if candidate not in existing:
            return candidate
