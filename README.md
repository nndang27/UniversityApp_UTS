# University Management System

A Python command-line and GUI application for managing university student enrolments.

---

## Quick Start

### Requirements
- Python 3.9 or above (with tkinter for GUI — on macOS run `brew install python-tk@3.11` if needed)
- No external packages required (standard library only)

### Run CLI
```bash
cd University2
python3 -m cliApp.app
```

### Run GUI
```bash
cd University2
python3 -m guiApp.app
```

---

## How to Register and Login (CLI)

**Register**
1. At the University menu enter `S` → Student menu
2. Enter `r` → Register
3. Enter email in the format `firstname.lastname@university.com`
4. Enter a password that follows these rules:
   - Starts with one **uppercase** letter
   - Has **at least 5 letters** in total
   - Ends with **3 or more digits**
   - Example: `Ngocd271` ✅ &nbsp;&nbsp; `Dang271` ❌ (only 4 letters)

**Login**
1. Enter `l` → Login
2. Enter the same email and password used during registration

---

## Project Structure

```
University2/
├── students.data              ← shared data file (auto-created on first run)
│
├── cliApp/
│   ├── app.py                 ← CLI entry point
│   ├── core/
│   │   ├── models.py          ← Student and Subject classes, grade logic
│   │   ├── db.py              ← reads and writes students.data
│   │   ├── validation.py      ← email and password regex patterns
│   │   └── util.py            ← random ID generators
│   └── cli/
│       ├── ui.py              ← display() and prompt() helpers (colour, indent)
│       ├── university_menu.py ← top-level menu (A/S/X)
│       ├── student_controller.py  ← register, login, student menu
│       ├── enrolment_controller.py  ← enrol/remove/show subjects, change password
│       └── admin_controller.py    ← show/group/partition/remove/clear students
│
└── guiApp/
    ├── app.py                 ← GUI entry point
    ├── database_manager.py    ← GUI persistence (reads/writes same students.data)
    ├── login_window.py        ← Window 1: login form
    ├── enrolment_window.py    ← Window 2: enrolment list
    ├── subject_popup.py       ← Window 3: subject detail
    └── exception_window.py    ← Window 4: error notifications
```

**students.data** stores all student records as JSON. Both CLI and GUI share this file, so a student registered via CLI can log in via GUI and vice versa.

---

## Work Division

### Person 1 — Foundation + University System + Student System (13 marks)

**Status: DONE** — these files are already implemented and must not be modified.

| File | Purpose |
|------|---------|
| `cliApp/core/models.py` | `Student`, `Subject`, `compute_grade()` |
| `cliApp/core/db.py` | `Database.initialise()`, `fetch_all()`, `persist_all()`, `wipe()` |
| `cliApp/core/validation.py` | `EMAIL_PATTERN`, `PASSWORD_PATTERN`, `is_valid_email()`, `is_valid_password()`, `name_from_email()` |
| `cliApp/core/util.py` | `new_student_id()`, `new_subject_id()` |
| `cliApp/cli/ui.py` | `display()`, `prompt()`, colour constants, `SUBMENU_JUMP` |
| `cliApp/cli/university_menu.py` | `run_university_menu()` |
| `cliApp/cli/student_controller.py` | `_register()`, `_login()`, `run_student_menu()` |
| `cliApp/app.py` | entry point |

**Assignment requirements covered:**
- University menu options `(A)` Admin, `(S)` Student, `(X)` Exit
- Student can navigate to student menu and admin menu
- Student register: validates email + password against regex, checks no duplicate, saves to `students.data`
- Student login: reads from `students.data`, verifies credentials
- Regex applied to both login and register

**Tips for project showcases:**
- Demo flow: launch app → enter `A` then `X` → enter `S` → show the system responds correctly to each option → browse back and forth a few times to demonstrate the navigation mark
- Explain `EMAIL_PATTERN` and `PASSWORD_PATTERN` regex constants in `validation.py` — why they are constants, what each part of the pattern means
- Explain `Student.serialise()` / `Student.deserialise()` in `models.py` — how objects are converted to/from JSON for file storage
- Explain `Database.initialise()` in `db.py` — why the file is created automatically if missing
- Be ready to answer: *"What happens if a student tries to register with an email that already exists?"* (answered in `_register()`)
- Be ready to answer: *"What is the purpose of `name_from_email()`?"* — derives display name from email so we never ask the user to type their name separately

---

### Person 2 — Subject Enrolment System (15 marks)

**File to implement: `cliApp/cli/enrolment_controller.py`**

| Function | What to implement |
|----------|-------------------|
| `run_course_menu(level, student)` | Menu loop `(c/e/r/s/x)` for logged-in student |
| `enrol_subject(level, student)` | Add 1 new subject; max 4 total; random mark 25–100; compute grade; save to file |
| `show_subjects(level, student)` | Print all enrolled subjects with mark and grade |
| `remove_subject(level, student)` | Ask for subject ID, remove it, save to file |
| `change_password(level, student)` | Validate new password format, confirm, save to file |

**Assignment requirements to satisfy:**
- A student can enrol in a **maximum of 4 subjects** — error if already at 4
- On enrol: subject gets a **random mark between 25 and 100**
- Grade is computed from mark: Z (<50), P (50–64), C (65–74), D (75–84), HD (≥85)
- Enrolment is **tracked and persisted** in `students.data`
- Student can **remove a subject by its ID**
- Student can **change their password** (reusing current password is allowed)
- **Read/write** subject and student data to/from file after every change
- Handle errors: subject not found, already at limit, invalid password format
- Output wording and indentation must match the sample I/O in the PDF

**How to persist changes (pattern to follow):**
```python
all_students = Database.fetch_all()
for s in all_students:
    if s.student_id == student.student_id:
        s.subjects = student.subjects   # or s.password = new_pw
        break
Database.persist_all(all_students)
```

**Tips for project showcases:**
- Demo all 5 options in order: enrol a subject → show it with mark+grade → enrol until 4 → try a 5th (show the error) → remove one → change password
- Explain `enrol_subject()`: how `new_subject_id()` generates a unique 3-digit ID, how `random.randint(25, 100)` gets the mark, and how `compute_grade()` maps it
- Explain the **dual update pattern** — why you must update both the in-memory `student` object AND reload+persist via `Database` so the file stays in sync
- Explain `student.at_capacity()` in `models.py` — how the max-4 rule is enforced
- Be ready to answer: *"What happens if a student enters an ID that doesn't exist when removing a subject?"* (handled with error message + early return)
- Be ready to answer: *"Can a student reuse their current password when changing it?"* — yes, the spec explicitly allows it; no special check needed

---

### Person 3 — Admin System (15 marks)

**File to implement: `cliApp/cli/admin_controller.py`**

| Function | What to implement |
|----------|-------------------|
| `run_admin_menu(level)` | Menu loop `(c/g/p/r/s/x)` — no login required |
| `show_students(level)` | Print all students; `<Nothing to Display>` if empty |
| `group_by_grade(level)` | Group by grade (Z/P/C/D/HD/N/A); only print non-empty groups |
| `partition_pass_fail(level)` | Split into PASS (avg ≥ 50) / FAIL / N/A; always print all 3 groups |
| `remove_student(level)` | Ask for student ID, remove from file |
| `clear_database(level)` | Ask Y/N confirmation, then wipe `students.data` |

**Assignment requirements to satisfy:**
- Admins access the system **without logging in**
- Show all students (read from file)
- Group students by grade: use `student.average_mark()` → `compute_grade(round(avg))`
- Partition PASS / FAIL: average mark **≥ 50 = PASS**, < 50 = FAIL; students with no subjects = N/A
- Remove student by student ID (update file)
- Clear all records from `students.data`
- **Read/write** all operations go through `Database.fetch_all()` / `Database.persist_all()`
- Handle errors: student ID not found, empty database
- Output wording and indentation must match the sample I/O in the PDF

**Useful model methods already available:**
```python
student.average_mark()     # returns float or None if no subjects
compute_grade(round(avg))  # returns "Z"/"P"/"C"/"D"/"HD"
```

**Tips for project showcases:**
- Demo all 6 options: show students → group by grade → partition pass/fail → remove one student → clear all (add a few test students first so the demo is not empty)
- Explain `group_by_grade()`: how `average_mark()` returns `None` for students with no subjects (they go into N/A bucket), and how you only print non-empty buckets
- Explain `partition_pass_fail()`: the threshold is **average ≥ 50 = PASS**; always print all 3 groups even if empty
- Explain that `Database.fetch_all()` is called fresh at the start of every admin function — this guarantees the latest data from file is used (important if CLI and GUI are used together)
- Be ready to answer: *"What happens when you try to remove a student ID that doesn't exist?"* (error message + no file change)
- Be ready to answer: *"Why does the admin not need to log in?"* — spec states admins pre-exist in the system; there is no admin registration or credential check

---

### Person 4 — GUIUniApp (7 marks)

**All files are in `guiApp/` — implement every `# TODO` comment.**

| File | Window | What to implement |
|------|--------|-------------------|
| `guiApp/app.py` | — | `main()`: create `DatabaseManager`, open `LoginWindow`, call `mainloop()` |
| `guiApp/database_manager.py` | — | All methods in `DatabaseManager` (authenticate, get_student, enrol_new_subject, delete_subject, save_student, _read, _write, _ensure_file) |
| `guiApp/login_window.py` | Window 1 | Build the login form UI; `_handle_login()` calls `db.authenticate()` and opens `EnrolmentWindow` on success |
| `guiApp/enrolment_window.py` | Window 2 | Subject list with enrol + delete buttons; `_enrol_one()` calls `db.enrol_new_subject()` |
| `guiApp/subject_popup.py` | Window 3 | Modal popup showing subject ID, mark, grade |
| `guiApp/exception_window.py` | Window 4 | Modal error popup — replaces all `messagebox.showerror()` calls |

**Assignment requirements to satisfy:**
- Login window reads registered students from **`students.data`** (same file as CLI)
- After login, student is taken to enrolment window
- Student can enrol in a **maximum of 4 subjects**
- Subject window shows **mark and grade** for each enrolled subject
- Handle all exceptions with `ExceptionWindow` (not `messagebox`):
  - Empty email or password field
  - Email does not match `firstname.lastname@university.com` format
  - Student does not exist
  - Wrong password
  - Attempting to enrol beyond 4 subjects
- **At least 4 separate windows** are required (Login, Enrolment, Subject, Exception)

**Important — path for `students.data`:**
```python
# In DatabaseManager.__init__:
pkg_dir      = os.path.dirname(os.path.abspath(__file__))  # guiApp/ folder
project_root = os.path.dirname(pkg_dir)                    # University2/ folder
self.path    = os.path.join(project_root, "students.data")
```
This ensures the GUI reads the same file as the CLI.

**Tips for project showcases:**
- Demo flow: open GUI → try empty login (ExceptionWindow appears) → try wrong email format (ExceptionWindow) → try wrong password (ExceptionWindow) → login successfully → enrol subjects → click a subject to see SubjectPopup → try to enrol a 5th (ExceptionWindow) → delete a subject → go back
- Make sure all 4 windows appear on screen during the demo — markers check this explicitly
- Explain `DatabaseManager.authenticate()`: the order of checks matters — empty → invalid format → not found → wrong password; explain why email format is validated **before** querying the file
- Explain `ExceptionWindow` as a custom `tk.Toplevel` class with `grab_set()` — why this is better than `messagebox` (it is a proper window, satisfies the "4 windows" requirement, and the style is consistent)
- Explain `_refresh_list()` in `EnrolmentWindow` — why the list is rebuilt from the database on every change instead of just appending a widget
- Be ready to answer: *"How does the GUI share data with the CLI?"* — both read/write the same `students.data` file; `DatabaseManager` resolves the absolute path to `University2/students.data`
- Be ready to answer: *"What is `grab_set()` and `transient()` in SubjectPopup / ExceptionWindow?"* — `transient` keeps the popup above its parent; `grab_set` blocks interaction with the parent until the popup is closed

---

## Integration Checklist (everyone checks before submitting)

- [ ] Register via CLI → can log in via GUI (same `students.data`)
- [ ] CLI output wording and indentation match the PDF sample I/O (pages 4–7)
- [ ] GUI has 4 separate windows; exception cases use `ExceptionWindow`
- [ ] Run: `python3 -m cliApp.app` from `University2/`
- [ ] Run: `python3 -m guiApp.app` from `University2/`
