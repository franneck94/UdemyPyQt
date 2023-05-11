from PyQt6.QtGui import QAction
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QMenu
from PyQt6.QtWidgets import QMenuBar
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()

        # Set up the main window
        self.setWindowTitle("Hello, World!")
        self.setGeometry(100, 100, 400, 300)

        # Create a central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        # Create menu bar
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        # Add menu and actions
        file_menu = QMenu("File", self)
        menu_bar.addMenu(file_menu)

        exit_action = QAction("Exit", self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        # Create QLineEdit for text input
        self.text_input = QLineEdit()
        layout.addWidget(self.text_input)

        # Create QTextEdit for text output
        self.text_output = QTextEdit()
        self.text_output.setReadOnly(True)
        layout.addWidget(self.text_output)

        # Create a QPushButton for submitting text
        button = QPushButton("Submit")
        button.clicked.connect(self.on_button_click)
        layout.addWidget(button)

    def on_button_click(self):
        text = self.text_input.text()
        self.text_output.append(f'You typed: {text}')
        self.text_input.clear()
