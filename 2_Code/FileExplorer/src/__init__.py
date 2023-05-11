import os
import sys
from pathlib import Path

from PyQt6.QtCore import QDir
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QStandardItem
from PyQt6.QtGui import QStandardItemModel
from PyQt6.QtWidgets import QInputDialog
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QListView
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QMessageBox
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 720)

        self.current_path = Path.cwd()
        self.selected_entry = None

        self.init_ui()

    def init_ui(self):
        widget = QWidget(self)
        self.setCentralWidget(widget)

        vbox = QVBoxLayout(widget)

        go_up_button = QPushButton("Go Up", self)
        go_up_button.clicked.connect(self.go_up)
        vbox.addWidget(go_up_button)

        self.current_dir_label = QLabel(self)
        vbox.addWidget(self.current_dir_label)

        self.file_count_label = QLabel(self)
        vbox.addWidget(self.file_count_label)

        self.file_list = QListView(self)
        self.model = QStandardItemModel()
        self.populate_model()
        self.file_list.setModel(self.model)
        self.file_list.clicked.connect(self.select_entry)
        self.file_list.doubleClicked.connect(self.on_double_click)
        vbox.addWidget(self.file_list)

        self.open_button = QPushButton("Open", self)
        self.open_button.clicked.connect(self.open_file)
        vbox.addWidget(self.open_button)

        self.rename_button = QPushButton("Rename", self)
        self.rename_button.clicked.connect(self.rename_file)
        vbox.addWidget(self.rename_button)

        self.delete_button = QPushButton("Delete", self)
        self.delete_button.clicked.connect(self.delete_file)
        vbox.addWidget(self.delete_button)

        self.update_ui()

    def populate_model(self):
        self.model.clear()
        dir = QDir(str(self.current_path))
        entries = dir.entryInfoList(
            QDir.Filter.NoDotAndDotDot | QDir.Filter.AllEntries
        )

        file_count = 0
        dir_count = 0
        for entry in entries:
            entry_type = "[D]" if entry.isDir() else "[F]"
            item = QStandardItem(entry_type + " " + entry.fileName())
            item.setData(entry.absoluteFilePath(), Qt.ItemDataRole.UserRole)
            self.model.appendRow(item)
            if entry.isDir():
                dir_count += 1
            else:
                file_count += 1

        self.file_count_label.setText(
            f"Files: {file_count} | Directories: {dir_count}"
        )

    def update_ui(self):
        self.current_dir_label.setText(
            f"Current directory: {str(self.current_path)}"
        )
        self.populate_model()

    def go_up(self):
        if self.current_path.parent:
            self.current_path = self.current_path.parent
            self.update_ui()

    def select_entry(self, index):
        self.selected_entry = Path(index.data(Qt.ItemDataRole.UserRole))

    def on_double_click(self, index):
        self.select_entry(index)
        self.open_file()

    def open_file(self):
        if not self.selected_entry:
            return

        if self.selected_entry.is_dir():
            self.current_path = self.selected_entry
            self.update_ui()
            return

        if sys.platform.startswith("win32"):
            os.startfile(self.selected_entry)
        elif sys.platform.startswith("darwin"):
            os.system(f"open \"{self.selected_entry}\"")
        else:
            os.system(f"xdg-open \"{self.selected_entry}\"")

    def rename_file(self):
        if self.selected_entry:
            new_name, ok = QInputDialog.getText(
                self, "Rename File", "New name:", text=self.selected_entry.name
            )
            if ok:
                new_path = self.selected_entry.parent / new_name
                try:
                    self.selected_entry.rename(new_path)
                    self.selected_entry = new_path
                except Exception as e:
                    QMessageBox.warning(
                        self, "Error", f"Error renaming file: {e}"
                    )

    def delete_file(self):
        if self.selected_entry:
            reply = QMessageBox.warning(
                self,
                "Delete File",
                f"Are you sure you want to delete {self.selected_entry.name}?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
            )

            if reply == QMessageBox.StandardButton.Yes:
                try:
                    if self.selected_entry.is_dir():
                        os.rmdir(self.selected_entry)
                    else:
                        os.remove(self.selected_entry)
                    self.selected_entry = None
                except Exception as e:
                    QMessageBox.warning(
                        self, "Error", f"Error deleting file: {e}"
                    )
