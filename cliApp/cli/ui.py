
from typing import Optional

# ---------------------------------------------------------------------------
# ANSI colour codes
# ---------------------------------------------------------------------------

CYAN   = "\033[96m"   # menu prompts
GREEN  = "\033[92m"   # success / section headings
YELLOW = "\033[93m"   # informational messages
RED    = "\033[91m"   # errors and warnings
RESET  = "\033[0m"    # revert to default terminal colour

# ---------------------------------------------------------------------------
# Indentation settings
# ---------------------------------------------------------------------------

# Number of space characters added per depth level
SPACES_PER_LEVEL = 2

# How many depth levels to increase when entering a sub-menu.
# At 2 spaces per level this means sub-menus indent by 8 spaces.
SUBMENU_JUMP = 4


# ---------------------------------------------------------------------------
# Internal helper
# ---------------------------------------------------------------------------

def _indent(level: int) -> str:
    """
    Build the leading-whitespace string for the given depth level.

    Input:  level -- non-negative integer representing menu depth
    Output: string of (SPACES_PER_LEVEL * level) space characters
    """
    return " " * (SPACES_PER_LEVEL * level)


# ---------------------------------------------------------------------------
# Public I/O functions
# ---------------------------------------------------------------------------

def display(level: int, message: str, colour: str = "") -> None:

    line = _indent(level) + message
    if colour:
        print(f"{colour}{line}{RESET}")
    else:
        print(line)


def prompt(level: int, message: str, colour: str = "") -> str:

    text = _indent(level) + message
    if colour:
        text = f"{colour}{text}{RESET}"
    return input(text).strip()
