from pathlib import Path

from PyQt6.QtCore import QSize
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeySequence
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QShortcut
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QPlainTextEdit
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class TextEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.line_number_area = LineNumberArea(self)

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self.layout.addWidget(self.line_number_area)
        self.plain_text_edit = QPlainTextEdit(self)
        self.layout.addWidget(self.plain_text_edit)

        # Set fixed height and vertical scrollbar policy
        font_metrics = self.plain_text_edit.fontMetrics()
        line_height = font_metrics.height()
        lines_to_show = int(600 / line_height)
        self.plain_text_edit.setFixedHeight(line_height * lines_to_show)
        self.plain_text_edit.setVerticalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAsNeeded
        )
        self.setFixedSize(1200, line_height * lines_to_show)

        self.plain_text_edit.blockCountChanged.connect(
            self.update_line_number_area_width
        )
        self.plain_text_edit.updateRequest.connect(self.update_line_number_area)

    def line_number_area_width(self):
        digits = len(str(max(1, self.plain_text_edit.blockCount())))
        space = (
            3
            + self.plain_text_edit.fontMetrics().horizontalAdvance('9') * digits
        )
        return space

    def update_line_number_area_width(self, _=None):
        self.line_number_area.setFixedWidth(self.line_number_area_width())

    def update_line_number_area(self, rect, dy):
        if dy:
            self.line_number_area.scroll(0, dy)
        else:
            self.line_number_area.update(
                0, rect.y(), self.line_number_area.width(), rect.height()
            )

        if rect.contains(self.plain_text_edit.viewport().rect()):
            self.update_line_number_area_width()

    def line_number_area_paint_event(self, event):
        painter = QPainter(self.line_number_area)
        painter.fillRect(event.rect(), Qt.GlobalColor.lightGray)

        block = self.plain_text_edit.firstVisibleBlock()
        block_number = block.blockNumber()
        top = (
            self.plain_text_edit.blockBoundingGeometry(block)
            .translated(self.plain_text_edit.contentOffset())
            .top()
        )
        bottom = top + self.plain_text_edit.blockBoundingRect(block).height()

        while block.isValid() and top <= event.rect().bottom():
            if block.isVisible() and bottom >= event.rect().top():
                number = str(block_number + 1)
                painter.setPen(Qt.GlobalColor.black)
                painter.drawText(
                    0,
                    int(top),
                    self.line_number_area.width(),
                    self.plain_text_edit.fontMetrics().height(),
                    Qt.AlignmentFlag.AlignRight,
                    number,
                )

            block = block.next()
            top = bottom
            bottom = (
                top + self.plain_text_edit.blockBoundingRect(block).height()
            )
            block_number += 1


class LineNumberArea(QWidget):
    def __init__(self, text_edit: TextEditor):
        super().__init__(text_edit)
        self.text_edit = text_edit

    def sizeHint(self):
        return QSize(self.text_edit.line_number_area_width(), 0)

    def paintEvent(self, event):
        self.text_edit.line_number_area_paint_event(event)


class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)

        self.setWindowTitle("Text Editor")

        # Create the menu bar
        self.menu_bar = self.menuBar()
        self.settings_menu = self.menu_bar.addMenu("Settings")

        # Add font size action to the settings menu
        self.font_size_action = self.settings_menu.addAction("Change Font Size")
        self.font_size_action.triggered.connect(self.change_font_size)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        # Create a horizontal layout for the save and save as buttons
        self.save_layout = QHBoxLayout()
        self.layout.addLayout(self.save_layout)

        self.save_button = QPushButton("Save")
        self.save_button.clicked.connect(self.save_file)
        self.save_layout.addWidget(self.save_button)

        self.save_as_button = QPushButton("Save As")
        self.save_as_button.clicked.connect(self.save_file_as)
        self.save_layout.addWidget(self.save_as_button)

        self.load_button = QPushButton("Load")
        self.load_button.clicked.connect(self.load_file)
        self.layout.addWidget(self.load_button)

        self.text_edit = TextEditor()
        self.layout.addWidget(self.text_edit)

        self.current_file = None
        self.current_file_label = QLabel("No file opened!")
        self.layout.addWidget(self.current_file_label)

        # Set up keyboard shortcuts
        self.save_shortcut = QShortcut(QKeySequence.StandardKey.Save, self)
        self.save_shortcut.activated.connect(self.save_file)

        self.load_shortcut = QShortcut(QKeySequence.StandardKey.Open, self)
        self.load_shortcut.activated.connect(self.load_file)

    def change_font_size(self):
        current_font_size = self.text_edit.plain_text_edit.font().pointSize()
        new_font_size, ok_pressed = QInputDialog.getInt(
            self,
            "Change Font Size",
            "Enter the new font size:",
            current_font_size,
            1,
            100,
            1,
        )

        if ok_pressed:
            font = self.text_edit.plain_text_edit.font()
            font.setPointSize(new_font_size)
            self.text_edit.plain_text_edit.setFont(font)

    def save_file(self, file_name=None):
        if not self.current_file and not file_name:
            options = QFileDialog.Option.ReadOnly
            file_name, _ = QFileDialog.getSaveFileName(
                self,
                "Save File",
                "",
                "All Files (*);;Text Files (*.txt)",
                options=options,
            )
            if file_name:
                self.current_file = file_name
        if file_name or self.current_file:
            with open(file_name or self.current_file, 'w') as f:
                f.write(self.text_edit.plain_text_edit.toPlainText())
            self.update_current_file_label()

    def save_file_as(self):
        options = QFileDialog.Option.ReadOnly
        file_name, _ = QFileDialog.getSaveFileName(
            self,
            "Save File As",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options,
        )
        if file_name:
            self.save_file(file_name)

    def load_file(self):
        options = QFileDialog.Option.ReadOnly
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Load File",
            "",
            "All Files (*);;Text Files (*.txt)",
            options=options,
        )
        if file_name:
            with open(file_name, 'r') as f:
                content = f.read()
            self.text_edit.plain_text_edit.setPlainText(content)
            self.current_file = file_name
            self.update_current_file_label()

    def update_current_file_label(self):
        if self.current_file:
            file_path = Path(self.current_file)
            file_extension = file_path.suffix
            self.current_file_label.setText(
                f"Opened file {self.current_file} | "
                f"File Extension: {file_extension}"
            )
        else:
            self.current_file_label.setText("No file opened!")
