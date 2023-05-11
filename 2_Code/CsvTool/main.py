import sys

from PyQt6.QtWidgets import QApplication

from src import WindowClass


def main():
    app = QApplication(sys.argv)
    main_window = WindowClass()
    main_window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
