"""
cliApp/cli/ui.py
================
OWNER: Person 1

Terminal I/O helpers for CLIUniApp.
All printing and input collection goes through display() and prompt()
so that indentation and colour are applied consistently across every menu.
"""

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
    """
    Print an indented message to the terminal, optionally coloured.

    Input:
        level   -- current menu depth (controls leading whitespace)
        message -- text to print
        colour  -- optional ANSI colour code (e.g. RED, GREEN); defaults to no colour
    Output:
        None  (prints one line to stdout)
    """
    line = _indent(level) + message
    if colour:
        print(f"{colour}{line}{RESET}")
    else:
        print(line)


def prompt(level: int, message: str, colour: str = "") -> str:
    """
    Display an indented prompt, wait for user input, and return the trimmed result.

    Input:
        level   -- current menu depth (controls leading whitespace)
        message -- prompt text shown before the cursor
        colour  -- optional ANSI colour code for the prompt text
    Output:
        The string the user typed, with leading and trailing whitespace removed.
    """
    text = _indent(level) + message
    if colour:
        text = f"{colour}{text}{RESET}"
    return input(text).strip()
