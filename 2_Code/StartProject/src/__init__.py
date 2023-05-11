from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMainWindow


class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Hello, World!")
        self.setGeometry(100, 100, 300, 200)

        # Create a QLabel widget to display "Hello, World!"
        label = QLabel("Hello, World!", self)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(label)
