import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QCheckBox
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QLineEdit
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1280, 720)

        self.setWindowTitle("Calculator Tool")

        self.function_names = ["sin(x)", "cos(x)", "poly(x)"]
        self.function_colors = {
            "sin(x)": 'r',
            "cos(x)": 'g',
            "poly(x)": 'b',
        }  # red  # green  # blue
        self.selected_functions = set()

        self.init_ui()

    def init_ui(self):
        widget = QWidget()
        self.setCentralWidget(widget)

        layout = QVBoxLayout()
        widget.setLayout(layout)

        checkbox_layout = QHBoxLayout()
        layout.addLayout(checkbox_layout)

        for func_name in self.function_names:
            checkbox = QCheckBox(func_name)
            checkbox.stateChanged.connect(
                lambda state, name=func_name: self.toggle_function(state, name)
            )
            checkbox_layout.addWidget(checkbox)

        # Add input fields for polynomial coefficients
        self.poly_coefficients: list[QLineEdit] = []
        self.poly_layout = QHBoxLayout()
        layout.addLayout(self.poly_layout)

        for i in range(5):
            label = QLabel(f"a{i}:")
            self.poly_layout.addWidget(label)

            line_edit = QLineEdit()
            line_edit.setFixedWidth(30)
            self.poly_layout.addWidget(line_edit)
            line_edit.textChanged.connect(self.update_plot)
            self.poly_coefficients.append(line_edit)

        self.label_full = QLabel(
            "0 * x^4 + " "0 * x^3 + " "0 * x^2 + " "0 * x^1 + " "0"
        )
        self.poly_layout.addWidget(self.label_full)
        self.label_full.setText(self.get_poly_label_text())

        self.plot_widget = pg.PlotWidget()
        layout.addWidget(self.plot_widget)

        # Add label and slider for x_min
        self.x_min_label = QLabel()
        layout.addWidget(self.x_min_label)
        self.x_min_slider = QSlider(Qt.Orientation.Horizontal)
        layout.addWidget(self.x_min_slider)
        self.x_min_slider.setMinimum(-1000)
        self.x_min_slider.setMaximum(0)
        self.x_min_slider.setValue(-100)  # Initial value
        self.x_min_slider.valueChanged.connect(self.update_plot)

        # Add label and slider for x_max
        self.x_max_label = QLabel()
        layout.addWidget(self.x_max_label)
        self.x_max_slider = QSlider(Qt.Orientation.Horizontal)
        layout.addWidget(self.x_max_slider)
        self.x_max_slider.setMinimum(0)
        self.x_max_slider.setMaximum(1000)
        self.x_max_slider.setValue(100)  # Initial value
        self.x_max_slider.valueChanged.connect(self.update_plot)

        # Add label and slider for y range
        self.y_range_label = QLabel()
        layout.addWidget(self.y_range_label)
        self.y_range_slider = QSlider(Qt.Orientation.Horizontal)
        layout.addWidget(self.y_range_slider)
        self.y_range_slider.setMinimum(1)
        self.y_range_slider.setMaximum(50)
        self.y_range_slider.setValue(2)  # Initial value
        self.y_range_slider.valueChanged.connect(self.update_plot)

        self.update_plot()

    def toggle_function(self, state, func_name):
        if state == Qt.CheckState.Checked.value:
            self.selected_functions.add(func_name)
        else:
            self.selected_functions.discard(func_name)
        self.update_plot()

    def get_poly_label_text(self):
        return (
            f"{self.poly_coefficients[4].text()} * x^4 + "
            f"{self.poly_coefficients[3].text()} * x^3 + "
            f"{self.poly_coefficients[2].text()} * x^2 + "
            f"{self.poly_coefficients[1].text()} * x^1 + "
            f"{self.poly_coefficients[0].text()}"
        )

    def evaluate_function(self, function, x):
        if function == "sin(x)":
            return np.sin(x)
        elif function == "cos(x)":
            return np.cos(x)
        elif function == "poly(x)":
            coefficients = [
                float(coeff.text() or "0")
                for coeff in self.poly_coefficients[::-1]
            ]
            return np.polyval(coefficients, x)
        else:
            return 0.0

    def update_plot(self):
        self.label_full.setText(self.get_poly_label_text())
        self.plot_widget.clear()

        x_min = self.x_min_slider.value()
        x_max = self.x_max_slider.value()
        num_points = (abs(x_max) + abs(x_min)) * 1_000
        x_step = (abs(x_max) + abs(x_min)) / num_points

        # Update x_min and x_max labels
        self.x_min_label.setText(f"X min: {x_min}")
        self.x_max_label.setText(f"X max: {x_max}")

        xs = np.arange(x_min, x_max, step=x_step)

        y_values = []

        for function in self.selected_functions:
            ys = self.evaluate_function(function, xs)
            y_values.append(ys)
            self.plot_widget.plot(
                xs, ys, name=function, pen=self.function_colors[function]
            )

        if y_values:
            y_min = -self.y_range_slider.value()
            y_max = self.y_range_slider.value()

            # Update y range label
            self.y_range_label.setText(f"Y range: {y_min} to {y_max}")

            self.plot_widget.setYRange(y_min, y_max)
            self.plot_widget.getAxis('bottom').setZValue(
                0
            )  # Position x-axis at y=0
