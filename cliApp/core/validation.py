
import re

# ---------------------------------------------------------------------------
# Regex constants  (must be applied to BOTH register and login)
# ---------------------------------------------------------------------------

# Valid email format: firstname.lastname@university.com
# Both parts before the '@' must contain only letters separated by a single dot.
EMAIL_PATTERN = re.compile(r"^[A-Za-z]+\.[A-Za-z]+@university\.com$")
# EMAIL_PATTERN = re.compile(r"^[a-zA-Z0-9._%+-]+@university\.com$")
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

    return bool(EMAIL_PATTERN.match(email.strip()))


def is_valid_password(password: str) -> bool:

    return bool(PASSWORD_PATTERN.match(password))


def name_from_email(email: str) -> str:

    local = email.strip().split("@")[0]
    parts = local.split(".", 1)
    if len(parts) == 2:
        return f"{parts[0].capitalize()} {parts[1].capitalize()}"
    return local.capitalize()
