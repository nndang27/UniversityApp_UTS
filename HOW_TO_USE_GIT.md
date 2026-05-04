# Git Workflow Guide

---

## Branch Assignment

| Branch | Owner |
|--------|-------|
| `main` | Person 1 — do not push here |
| `feature/student-enrolment` | Person 2 |
| `feature/admin` | Person 3 |
| `feature/gui` | Person 4 |

---

## Do I need a token to push?

**Yes — GitHub requires a Personal Access Token (PAT) when pushing via HTTPS.**
GitHub no longer accepts your account password for `git push`.

Each person creates their own token (free, takes 2 minutes):

```
github.com → Profile photo → Settings
→ Developer settings → Personal access tokens → Tokens (classic)
→ Generate new token (classic)
   ✅ repo  (tick this scope)
   Expiration: 90 days (or No expiration for convenience)
→ Copy the token — save it somewhere, you only see it once
```

When `git push` asks for a password, **paste the token** (not your GitHub password).

> **Tip:** Run this once so Git remembers your token and stops asking:
> ```bash
> git config --global credential.helper store
> ```
> After the first successful push, credentials are saved automatically.

---

## First-time Setup

### 1 — Accept the collaborator invite

Person 1 will add you as a collaborator on GitHub.
Check your email for the invite link and accept it — **you cannot push without this step**.

### 2 — Clone the repo

```bash
git clone https://github.com/<person1-username>/University2.git
cd University2
```

### 3 — Switch to your branch

```bash
# Person 2
git checkout feature/student-enrolment

# Person 3
git checkout feature/admin

# Person 4
git checkout feature/gui
```

---

## Daily Workflow

### Save and push your work

```bash
git add .
git commit -m "Brief description of what you did"
git push
```

Do this regularly — at least after finishing each function.

### Get the latest version of your branch

```bash
git pull
```

Run this whenever you sit down to work, especially if you switched computers.

---

## Rules

- **Only work on your own branch.** Never commit to `main`.
- **Do not edit files owned by another person** (see `README.md` for ownership).
- **Write clear commit messages**, e.g. `"Implement enrol_subject"` not `"update"`.

---

## Quick Reference

| Task | Command |
|------|---------|
| Check current branch | `git branch` |
| See what changed | `git status` |
| Save and push | `git add . && git commit -m "message" && git push` |
| Get latest from remote | `git pull` |
| Switch branch | `git checkout <branch-name>` |
| See commit history | `git log --oneline` |
