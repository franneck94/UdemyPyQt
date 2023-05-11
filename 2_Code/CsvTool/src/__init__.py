import csv

import PyQt6.QtWidgets
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()
        self.resize(1280, 720)

    def init_ui(self):
        self.setWindowTitle("CSV Editor")

        vbox = QVBoxLayout()

        # Row controls
        row_controls_layout = QHBoxLayout()
        row_controls_label = QLabel("Rows: ")
        row_controls_layout.addWidget(row_controls_label)

        self.row_count_label = QLabel("0")
        row_controls_layout.addWidget(self.row_count_label)

        self.row_slider = QSlider(Qt.Orientation.Horizontal)
        self.row_slider.setMinimum(0)
        self.row_slider.setMaximum(30)
        self.row_slider.valueChanged.connect(self.set_rows)
        row_controls_layout.addWidget(self.row_slider)

        add_row_button = QPushButton("Add Row")
        add_row_button.clicked.connect(self.add_row)
        row_controls_layout.addWidget(add_row_button)

        remove_row_button = QPushButton("Remove Row")
        remove_row_button.clicked.connect(self.remove_row)
        row_controls_layout.addWidget(remove_row_button)

        vbox.addLayout(row_controls_layout)

        # Column controls
        col_controls_layout = QHBoxLayout()
        col_controls_label = QLabel("Cols: ")
        col_controls_layout.addWidget(col_controls_label)

        self.col_count_label = QLabel("0")
        col_controls_layout.addWidget(self.col_count_label)

        self.col_slider = QSlider(Qt.Orientation.Horizontal)
        self.col_slider.setMinimum(0)
        self.col_slider.setMaximum(8)
        self.col_slider.valueChanged.connect(self.set_cols)
        col_controls_layout.addWidget(self.col_slider)

        add_col_button = QPushButton("Add Col")
        add_col_button.clicked.connect(self.add_col)
        col_controls_layout.addWidget(add_col_button)

        remove_col_button = QPushButton("Remove Col")
        remove_col_button.clicked.connect(self.remove_col)
        col_controls_layout.addWidget(remove_col_button)

        vbox.addLayout(col_controls_layout)

        # File controls
        file_controls_layout = QHBoxLayout()

        open_button = QPushButton("Open")
        open_button.clicked.connect(self.open_file)
        file_controls_layout.addWidget(open_button)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_file)
        file_controls_layout.addWidget(save_button)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_content)
        file_controls_layout.addWidget(clear_button)

        vbox.addLayout(file_controls_layout)

        controls_widget = QWidget()
        controls_widget.setLayout(vbox)

        # Table widget
        self.table_widget = QTableWidget()
        self.table_widget.setSizePolicy(
            PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
            PyQt6.QtWidgets.QSizePolicy.Policy.Expanding,
        )

        bottom_layout = QVBoxLayout()
        bottom_layout.addWidget(self.table_widget)
        bottom_layout.setAlignment(Qt.AlignmentFlag.AlignBottom)

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.addWidget(controls_widget)
        main_layout.addLayout(bottom_layout)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)

        self.setCentralWidget(central_widget)

    def set_rows(self, value):
        self.table_widget.setRowCount(value)
        self.row_count_label.setText(str(value))

    def set_cols(self, value):
        self.table_widget.setColumnCount(value)
        self.col_count_label

    def add_row(self):
        row = self.table_widget.rowCount()
        self.table_widget.insertRow(row)
        self.row_slider.setValue(row + 1)
        for col in range(self.table_widget.columnCount()):
            item = QTableWidgetItem("0.0")
            self.table_widget.setItem(row, col, item)

    def remove_row(self):
        row = self.table_widget.rowCount()
        if row > 0:
            self.table_widget.removeRow(row - 1)
        self.row_slider.setValue(row - 1)

    def add_col(self):
        col = self.table_widget.columnCount()
        self.table_widget.insertColumn(col)
        self.col_slider.setValue(col + 1)
        for row in range(self.table_widget.rowCount()):
            item = QTableWidgetItem("0.0")
            self.table_widget.setItem(row, col, item)

    def remove_col(self):
        col = self.table_widget.columnCount()
        if col > 0:
            self.table_widget.removeColumn(col - 1)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open CSV File", "", "CSV Files (*.csv)"
        )
        if file_name:
            self.load_csv(file_name)
            self.row_slider.setValue(self.table_widget.rowCount())
            self.col_slider.setValue(self.table_widget.columnCount())

    def save_file(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save CSV File", "", "CSV Files (*.csv)"
        )
        if file_name:
            self.save_csv(file_name)

    def load_csv(self, file_name):
        with open(file_name, newline='') as csvfile:
            reader = csv.reader(csvfile)
            try:
                header = next(reader)
            except StopIteration:
                return
            self.table_widget.setColumnCount(len(header))
            self.table_widget.setHorizontalHeaderLabels(header)
            self.table_widget.setRowCount(0)

            for row_data in reader:
                row = self.table_widget.rowCount()
                self.table_widget.insertRow(row)

                for col, data in enumerate(row_data):
                    item = QTableWidgetItem(data)
                    self.table_widget.setItem(row, col, item)

    def save_csv(self, file_name):
        with open(file_name, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = [
                self.table_widget.horizontalHeaderItem(col).text()
                if self.table_widget.horizontalHeaderItem(col) is not None
                else ""
                for col in range(self.table_widget.columnCount())
            ]
            writer.writerow(header)

            for row in range(self.table_widget.rowCount()):
                row_data = []
                for col in range(self.table_widget.columnCount()):
                    item = self.table_widget.item(row, col)
                    if item is not None:
                        row_data.append(item.text())
                    else:
                        row_data.append('')
                writer.writerow(row_data)

    def clear_content(self):
        self.table_widget.setColumnCount(0)
        self.table_widget.setRowCount(0)
