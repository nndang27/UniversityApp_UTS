"""
cliApp/core/validation.py
=========================
OWNER: Person 1

Credential validation for CLIUniApp.
Defines regex constants and helper functions used by both the Student System
(register / login) and the Subject Enrolment System (change password).
"""

import re

# ---------------------------------------------------------------------------
# Regex constants  (must be applied to BOTH register and login)
# ---------------------------------------------------------------------------

# Valid email format: firstname.lastname@university.com
# Both parts before the '@' must contain only letters separated by a single dot.
EMAIL_PATTERN = re.compile(r"^[A-Za-z]+\.[A-Za-z]+@university\.com$")

# Valid password rules:
#   (1) First character must be uppercase  [A-Z]
#   (2) Followed by at least 4 more letters (upper or lower)  [A-Za-z]{4,}
#       → total >= 5 letters at the start
#   (3) Ends with 3 or more digits  \d{3,}
PASSWORD_PATTERN = re.compile(r"^[A-Z][A-Za-z]{4,}\d{3,}$")


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------

def is_valid_email(email: str) -> bool:
    """
    Check whether an email address matches the university format.

    Input:  email -- string entered by the user (not pre-stripped)
    Output: True  if the email fully matches EMAIL_PATTERN
            False otherwise

    Valid example:   john.smith@university.com
    Invalid examples:
        john.smith@university      (missing .com)
        johnsmith@university.com   (no dot separator)
        john.smith@gmail.com       (wrong domain)
    """
    return bool(EMAIL_PATTERN.match(email.strip()))


def is_valid_password(password: str) -> bool:
    """
    Check whether a password satisfies all three strength rules.

    Input:  password -- string entered by the user
    Output: True  if the password fully matches PASSWORD_PATTERN
            False otherwise

    Valid example:   Hello123
    Invalid examples:
        hello123   (lowercase start)
        Hello12    (only 2 trailing digits)
        Helo123    (only 4 letters total, need >= 5)
    """
    return bool(PASSWORD_PATTERN.match(password))


def name_from_email(email: str) -> str:
    """
    Derive a human-readable display name from a university email address.

    Input:  email -- a university email, e.g. "john.smith@university.com"
    Output: capitalised "Firstname Lastname", e.g. "John Smith"
            Falls back to capitalising the local part when no dot is present.

    Examples:
        "john.smith@university.com"  →  "John Smith"
        "alice@university.com"       →  "Alice"
    """
    local = email.strip().split("@")[0]
    parts = local.split(".", 1)
    if len(parts) == 2:
        return f"{parts[0].capitalize()} {parts[1].capitalize()}"
    return local.capitalize()
