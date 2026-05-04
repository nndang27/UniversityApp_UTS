"""
cliApp/core/util.py
===================
OWNER: Person 1

Utility functions for generating unique random IDs.
Used when registering students and enrolling in subjects.
"""

import random
from typing import List


def new_student_id(existing: List[str]) -> str:
    """
    Generate a unique 6-digit student ID not already in use.

    Input:
        existing -- list of student ID strings currently stored in students.data
    Output:
        A zero-padded 6-digit string in the range "000001" .. "999999"
        that does not appear in the existing list.

    Behaviour: picks randomly and retries on collision (collisions are rare
    given the large ID space vs typical student counts).

    Example:
        new_student_id(["000042", "183771"])  →  "395610"  (some unique value)
    """
    while True:
        candidate = f"{random.randint(1, 999_999):06d}"
        if candidate not in existing:
            return candidate


def new_subject_id(existing: List[str]) -> str:
    """
    Generate a unique 3-digit subject ID not already enrolled by this student.

    Input:
        existing -- list of subject ID strings already in the student's subjects list
    Output:
        A zero-padded 3-digit string in the range "001" .. "999"
        that does not appear in the existing list.

    Behaviour: picks randomly and retries on collision.

    Example:
        new_subject_id(["042", "117"])  →  "583"  (some unique value)
    """
    while True:
        candidate = f"{random.randint(1, 999):03d}"
        if candidate not in existing:
            return candidate
