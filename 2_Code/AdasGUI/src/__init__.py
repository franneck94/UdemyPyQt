import json
from typing import Any
from typing import Dict

import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QTableWidget
from PyQt6.QtWidgets import QTableWidgetItem
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)

        # Set up the main window
        self.setWindowTitle("ADAS Log Data")
        self.setGeometry(100, 100, 800, 600)

        # Create a central widget
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        # Create a vertical layout
        layout = QVBoxLayout(central_widget)

        open_file_button = QPushButton("Open File")
        open_file_button.clicked.connect(self.open_file)
        layout.addWidget(open_file_button)

        # Create the lane plot
        self.lane_plot = pg.PlotWidget()
        layout.addWidget(self.lane_plot)

        # Set up lane plot properties
        self.lane_plot.showGrid(x=True, y=True)
        self.lane_plot.setAspectLocked(lock=True, ratio=1)
        self.lane_plot.setLabel('left', text='Rel. LatDist. (m)')
        self.lane_plot.setLabel('bottom', text='Rel. LongDist. (m)')

        # Dummy data
        lanes_data = [(-2, 2), (-1, 1), (0, 0), (1, -1), (2, -2)]
        ego_vehicle_data = (0, 0)

        # Plot lanes
        for i in range(len(lanes_data) - 1):
            x_points = np.linspace(-100, 100, 1000)
            y_points = np.linspace(lanes_data[i][1], lanes_data[i + 1][1], 1000)
            self.lane_plot.plot(x_points, y_points, pen=pg.mkPen('w', width=1))

        # Plot ego vehicle
        ego_vehicle = pg.ScatterPlotItem(
            pos=[ego_vehicle_data],
            size=10,
            pen=pg.mkPen(None),
            brush=pg.mkBrush(255, 255, 255),
        )
        self.lane_plot.addItem(ego_vehicle)

        # Create the table widget
        self.table_widget = QTableWidget(central_widget)
        self.table_widget.setColumnCount(6)
        self.table_widget.setHorizontalHeaderLabels(
            ["ID", "Type", "Lane", "Long. Dist.", "Lat. Dist.", "Speed"]
        )
        # Customize the table and add data
        self.customize_table()
        layout.addWidget(self.table_widget)

        button_layout = QHBoxLayout()

        self.replay_button = QPushButton("Replay")
        self.replay_button.clicked.connect(self.replay)
        button_layout.addWidget(self.replay_button)

        self.play_button = QPushButton("Play")
        self.play_button.clicked.connect(self.play)
        button_layout.addWidget(self.play_button)

        self.stop_button = QPushButton("Stop")
        self.stop_button.clicked.connect(self.stop)
        button_layout.addWidget(self.stop_button)

        layout.addLayout(button_layout)

    def open_file(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Log File", "", "Log Files (*.log);;All Files (*)"
        )
        if file_name:
            print(f"File selected: {file_name}")

    def customize_table(self):
        # Add data to the table
        self.table_widget.setRowCount(10)

        # Sample data
        data = [
            [1, "Car", "Left", 10.0, 5.0, 25.0],
            [2, "Truck", "Center", 20.0, 10.0, 15.0],
            # Add more data here
        ]

        for row, rowData in enumerate(data):
            for col, cellData in enumerate(rowData):
                self.table_widget.setItem(
                    row, col, QTableWidgetItem(str(cellData))
                )

        self.table_widget.resizeColumnsToContents()
        self.table_widget.resizeRowsToContents()
        self.table_widget.horizontalHeader().setStretchLastSection(True)
        self.table_widget.setSelectionMode(
            QTableWidget.SelectionMode.NoSelection
        )
        self.table_widget.setFocusPolicy(Qt.FocusPolicy.NoFocus)

    def replay(self):
        print("Replay pressed")
        # Add your replay logic here

    def play(self):
        print("Play pressed")
        # Add your play logic here

    def stop(self):
        print("Stop pressed")
        # Add your stop logic here

    @staticmethod
    def read_json_data(
        ego_vehicle_file: str, vehicle_data_file: str
    ) -> Dict[str, Dict[str, Any]]:
        with open(ego_vehicle_file, "r") as file_object:
            ego_data = json.load(file_object)

        with open(vehicle_data_file, "r") as file_object:
            vehicle_data = json.load(file_object)

        return {"ego_vehicle": ego_data, "vehicles": vehicle_data}
