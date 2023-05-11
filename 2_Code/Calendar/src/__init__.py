import json

from PyQt6.QtCore import QDate
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCalendarWidget
from PyQt6.QtWidgets import QDialog
from PyQt6.QtWidgets import QGridLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QListWidget
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class Meeting:
    def __init__(self, name):
        self.name = name


class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()

        self.meetings: dict[QDate, list[Meeting]] = {}

        self.setWindowTitle("Calendar Tool")

        self.central_widget = QVBoxLayout()
        self.central_widget.addWidget(QLabel("Select a date:"))

        self.meeting_list_label = QLabel("Meetings on the selected date:")
        self.central_widget.addWidget(self.meeting_list_label)

        self.meeting_list_widget = QListWidget()
        self.central_widget.addWidget(self.meeting_list_widget)

        self.calendar = QCalendarWidget()
        self.central_widget.addWidget(self.calendar)
        self.selected_date = self.calendar.selectedDate()
        self.update_date_label()

        self.add_meeting_button = QPushButton("Add Meeting")
        self.central_widget.addWidget(self.add_meeting_button)
        self.add_meeting_button.clicked.connect(self.add_meeting_dialog)

        self.calendar.selectionChanged.connect(self.update_date_label)

        central_widget_container = QWidget()
        central_widget_container.setLayout(self.central_widget)
        self.setCentralWidget(central_widget_container)

        self.load_meetings()

    def update_date_label(self):
        self.selected_date = self.calendar.selectedDate()
        self.meeting_list_label.setText(
            f"Meetings on {self.selected_date.toString(Qt.DateFormat.ISODate)}:"
        )

        self.meeting_list_widget.clear()
        if self.selected_date in self.meetings:
            for meeting in self.meetings[self.selected_date]:
                self.meeting_list_widget.addItem(meeting.name)

    def add_meeting_dialog(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Add Meeting")

        grid_layout = QGridLayout()

        grid_layout.addWidget(QLabel("Meeting Name:"), 0, 0)

        meeting_name_edit = QLineEdit()
        grid_layout.addWidget(meeting_name_edit, 0, 1)

        save_button = QPushButton("Save")
        grid_layout.addWidget(save_button, 1, 0)
        save_button.clicked.connect(
            lambda: self.add_meeting(meeting_name_edit.text(), dialog)
        )

        cancel_button = QPushButton("Cancel")
        grid_layout.addWidget(cancel_button, 1, 1)
        cancel_button.clicked.connect(dialog.reject)

        dialog.setLayout(grid_layout)
        dialog.exec()

    def add_meeting(self, meeting_name: str, dialog: QDialog):
        if self.selected_date not in self.meetings:
            self.meetings[self.selected_date] = []

        self.meetings[self.selected_date].append(Meeting(meeting_name))
        self.update_date_label()
        dialog.accept()

    def save_meetings(self, filename: str = "meetings.json"):
        with open(filename, "w") as f:
            meetings_ = {
                WindowClass.serialize_date(k): [vi.name for vi in v]
                for k, v in self.meetings.items()
            }
            json.dump(meetings_, f)

    def load_meetings(self, filename: str = "meetings.json"):
        try:
            with open(filename, "r") as f:
                meetings_ = json.load(f)
                self.meetings = {
                    WindowClass.deserialize_date(k): [Meeting(vi) for vi in v]
                    for k, v in meetings_.items()
                }
        except FileNotFoundError:
            self.meetings = {}
        except json.decoder.JSONDecodeError:
            self.meetings = {}

    @staticmethod
    def serialize_date(obj):
        if isinstance(obj, QDate):
            return f"{obj.day()}.{obj.month()}.{obj.year()}"
        return obj

    @staticmethod
    def deserialize_date(obj):
        obj = obj.split(".")
        return QDate(int(obj[2]), int(obj[1]), int(obj[0]))

    def closeEvent(self, event):
        self.save_meetings()
        event.accept()
