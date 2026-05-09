
from .database_manager import DatabaseManager
from .login_window import LoginWindow


def main() -> None:
    db  = DatabaseManager()
    app = LoginWindow(db)
    app.mainloop()


if __name__ == "__main__":
    main()
