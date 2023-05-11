from pathlib import Path

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QTextCharFormat
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSizePolicy
from PyQt6.QtWidgets import QTextEdit
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 720)

        self.setWindowTitle('File Diff Tool')

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        file_path_layout = QHBoxLayout()

        self.left_path_button = QPushButton("Select Left File")
        self.left_path_button.clicked.connect(self.select_left_file)
        self.right_path_button = QPushButton("Select Right File")
        self.right_path_button.clicked.connect(self.select_right_file)

        file_path_layout.addWidget(self.left_path_button)
        file_path_layout.setStretchFactor(self.left_path_button, 1)
        file_path_layout.addWidget(self.right_path_button)
        file_path_layout.setStretchFactor(self.right_path_button, 1)

        self.left_file_label = QLabel()
        self.right_file_label = QLabel()
        file_path_layout.addWidget(self.left_file_label)
        file_path_layout.addWidget(self.right_file_label)

        main_layout.addLayout(file_path_layout)

        self.compare_button = QPushButton("Compare")
        self.compare_button.clicked.connect(self.compare)
        main_layout.addWidget(self.compare_button)

        self.file_info_layout = QHBoxLayout()

        self.left_file_label = QLabel()
        self.left_file_label.setText("None")
        self.right_file_label = QLabel()
        self.right_file_label.setText("None")

        self.file_info_layout.addWidget(self.left_file_label)
        self.file_info_layout.addWidget(self.right_file_label)

        main_layout.addLayout(self.file_info_layout)

        self.diff_layout = QHBoxLayout()

        self.left_text = QTextEdit()
        self.left_text.setReadOnly(True)
        self.left_text.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.right_text = QTextEdit()
        self.right_text.setReadOnly(True)
        self.right_text.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )

        self.diff_layout.addWidget(self.left_text)
        self.diff_layout.addWidget(self.right_text)
        self.connect_scrollbars()

        main_layout.addLayout(self.diff_layout)

        self.diff_count_label = QLabel()
        main_layout.addWidget(self.diff_count_label)

        self.left_file_path = ""
        self.right_file_path = ""

    def connect_scrollbars(self):
        left_scrollbar = self.left_text.verticalScrollBar()
        right_scrollbar = self.right_text.verticalScrollBar()

        left_scrollbar.valueChanged.connect(right_scrollbar.setValue)
        right_scrollbar.valueChanged.connect(left_scrollbar.setValue)

    def load_file_content(self, file_path):
        if not file_path:
            return []

        content = []
        with open(file_path, "r") as f:
            for line in f:
                content.append(line.strip())

        return content

    def select_left_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Left File", "", "All Files (*)"
        )
        if file_path:
            self.left_file_path = file_path
            self.left_file_label.setText(f"Left: {Path(file_path).name}")

    def select_right_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select Right File", "", "All Files (*)"
        )
        if file_path:
            self.right_file_path = file_path
            self.right_file_label.setText(f"Right: {Path(file_path).name}")

    def compare(self):
        left_content = self.load_file_content(self.left_file_path)
        right_content = self.load_file_content(self.right_file_path)

        max_num_lines = max(len(left_content), len(right_content))

        left_diff = []
        right_diff = []
        diff_count = 0

        for i in range(max_num_lines):
            left_line = left_content[i] if i < len(left_content) else "EMPTY"
            right_line = right_content[i] if i < len(right_content) else "EMPTY"

            if left_line != right_line:
                left_diff.append((left_line, True))
                right_diff.append((right_line, True))
                diff_count += 1
            else:
                left_diff.append((left_line, False))
                right_diff.append((right_line, False))

        self.display_diff(self.left_text, left_diff)
        self.display_diff(self.right_text, right_diff)

        self.diff_count_label.setText(f"Number of diff lines: {diff_count}")
        self.diff_count_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

    def display_diff(self, text_edit, diff_data):
        text_edit.clear()
        cursor = text_edit.textCursor()

        format_normal = QTextCharFormat()
        format_diff = QTextCharFormat()
        format_diff.setForeground(QColor("red"))

        for line, is_diff in diff_data:
            if is_diff:
                cursor.setCharFormat(format_diff)
            else:
                cursor.setCharFormat(format_normal)
            cursor.insertText(line + "\n")
