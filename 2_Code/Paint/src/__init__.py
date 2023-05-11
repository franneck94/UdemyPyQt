from PyQt6.QtCore import QEvent
from PyQt6.QtCore import QPoint
from PyQt6.QtCore import QRect
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QIcon
from PyQt6.QtGui import QImage
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QColorDialog
from PyQt6.QtWidgets import QFileDialog
from PyQt6.QtWidgets import QHBoxLayout
from PyQt6.QtWidgets import QLabel
from PyQt6.QtWidgets import QMainWindow
from PyQt6.QtWidgets import QPushButton
from PyQt6.QtWidgets import QSlider
from PyQt6.QtWidgets import QVBoxLayout
from PyQt6.QtWidgets import QWidget


class PaintCanvas(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(1200, 500)
        self.image = QImage(self.size(), QImage.Format.Format_ARGB32)
        self.image.fill(Qt.GlobalColor.white)
        self.drawing = False
        self.brush_color = QColor(0, 0, 0)
        self.brush_size = 3
        self.last_point = QPoint()

        self.selection_start = QPoint()
        self.selection_end = QPoint()
        self.selecting = False
        self.filling = False
        self.selected_area = QRect()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drawing = True
            self.last_point = event.position().toPoint()

        if event.button() == Qt.MouseButton.LeftButton and self.selecting:
            self.selection_start = event.position().toPoint()
            self.selected_area = QRect()

        if event.button() == Qt.MouseButton.LeftButton and self.filling:
            self.fill_rectangle(event.position().toPoint())

    def mouseMoveEvent(self, event):
        if event.buttons() & Qt.MouseButton.LeftButton and self.drawing:
            painter = QPainter(self.image)
            painter.setPen(
                QPen(
                    self.brush_color,
                    self.brush_size,
                    Qt.PenStyle.SolidLine,
                    Qt.PenCapStyle.RoundCap,
                    Qt.PenJoinStyle.RoundJoin,
                )
            )
            painter.drawLine(self.last_point, event.position().toPoint())
            self.last_point = event.position().toPoint()
            self.update()
        if event.buttons() & Qt.MouseButton.LeftButton and self.selecting:
            self.selection_end = event.position().toPoint()
            self.selected_area = QRect(self.selection_start, self.selection_end)
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and self.selecting:
            self.selection_end = event.position().toPoint()
            self.selected_area = QRect(self.selection_start, self.selection_end)
            self.selecting = False
            self.update()

    def paintEvent(self, event):
        canvas_painter = QPainter(self)
        canvas_painter.drawImage(self.rect(), self.image, self.rect())

        if not self.selected_area.isNull():
            canvas_painter.setPen(
                QPen(Qt.GlobalColor.gray, 1, Qt.PenStyle.DashLine)
            )
            canvas_painter.drawRect(self.selected_area)

    def select_rectangle(self):
        self.selecting = not self.selecting

    def fill_rectangle(self, point):
        if self.selected_area.isNull():
            return

        painter = QPainter(self.image)
        painter.fillRect(self.selected_area, self.brush_color)
        self.update()


class WindowClass(QMainWindow):
    def __init__(self):
        super().__init__()
        self.resize(1280, 720)

        self.canvas = PaintCanvas()
        self.setCentralWidget(self.canvas)

        self.cpick_button = QPushButton("Choose")
        self.cpick_button.clicked.connect(self.selected_pick)
        self.red_button = QPushButton("Red")
        self.red_button.clicked.connect(self.selected_red)
        self.green_button = QPushButton("Green")
        self.green_button.clicked.connect(self.selected_green)
        self.blue_button = QPushButton("Blue")
        self.blue_button.clicked.connect(self.selected_blue)
        self.white_button = QPushButton("White")
        self.white_button.clicked.connect(self.selected_white)

        self.colors = {
            QColor(255, 0, 0).getRgb(): self.red_button,
            QColor(0, 255, 0).getRgb(): self.green_button,
            QColor(0, 0, 255).getRgb(): self.blue_button,
            QColor(255, 255, 255).getRgb(): self.white_button,
        }
        self.selected_color = QColor(0, 0, 0)

        clear_button = QPushButton("Clear")
        clear_button.clicked.connect(self.clear_canvas)

        save_button = QPushButton("Save")
        save_button.clicked.connect(self.save_image)

        load_button = QPushButton("Load")
        load_button.clicked.connect(self.load_image)

        brush_size_slider = QSlider(Qt.Orientation.Horizontal)
        brush_size_slider.setRange(1, 10)
        brush_size_slider.setValue(3)
        brush_size_slider.valueChanged.connect(self.set_brush_size)

        brush_size_label = QLabel()
        brush_size_label.setNum(brush_size_slider.value())
        brush_size_slider.valueChanged.connect(brush_size_label.setNum)

        cpick_buttons_layout = QHBoxLayout()
        cpick_buttons_layout.addWidget(self.red_button)
        cpick_buttons_layout.addWidget(self.green_button)
        cpick_buttons_layout.addWidget(self.blue_button)
        cpick_buttons_layout.addWidget(self.white_button)
        cpick_buttons_layout.addWidget(self.cpick_button)

        action_buttons_layout = QHBoxLayout()
        action_buttons_layout.addWidget(clear_button)
        action_buttons_layout.addWidget(save_button)
        action_buttons_layout.addWidget(load_button)

        slider_layout = QHBoxLayout()
        slider_layout.addWidget(QLabel("Brush size:"))
        slider_layout.addWidget(brush_size_slider)
        slider_layout.addWidget(brush_size_label)

        main_layout = QVBoxLayout()
        main_layout.addLayout(cpick_buttons_layout)
        main_layout.addLayout(action_buttons_layout)
        main_layout.addLayout(slider_layout)

        select_rectangle_button = QPushButton()
        select_rectangle_button.setText("Select")
        select_rectangle_button.setIcon(QIcon("media/select.png"))
        select_rectangle_button.clicked.connect(self.canvas.select_rectangle)

        fill_rectangle_button = QPushButton()
        fill_rectangle_button.setText("Fill")
        fill_rectangle_button.setIcon(QIcon("media/fill.png"))
        fill_rectangle_button.clicked.connect(self.canvas.fill_rectangle)

        rectangle_buttons_layout = QHBoxLayout()
        rectangle_buttons_layout.addWidget(select_rectangle_button)
        rectangle_buttons_layout.addWidget(fill_rectangle_button)

        main_layout.addLayout(rectangle_buttons_layout)

        container = QWidget()
        container.setLayout(main_layout)
        self.setMenuWidget(container)

    def keyPressEvent(self, event) -> None:
        if (
            event.key() == Qt.Key.Key_S
            and event.modifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            self.save_image()
        elif (
            event.key() == Qt.Key.Key_L
            and event.modifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            self.load_image()
        elif (
            event.key() == Qt.Key.Key_R
            and event.modifiers() & Qt.KeyboardModifier.ControlModifier
        ):
            self.clear_canvas()

    def selected_red(self):
        color = QColor(255, 0, 0)
        self.selected_color = color
        self.set_brush_color(color)

    def selected_green(self):
        color = QColor(0, 255, 0)
        self.selected_color = color
        self.set_brush_color(color)

    def selected_blue(self):
        color = QColor(0, 0, 255)
        self.selected_color = color
        self.set_brush_color(color)

    def selected_white(self):
        color = QColor(255, 255, 255)
        self.selected_color = color
        self.set_brush_color(color)

    def update_cpick_buttons(
        self,
    ):  # Add a new method to update the color buttons
        for k_color, v_button in self.colors.items():
            if k_color == self.canvas.brush_color.getRgb():
                v_button.setStyleSheet("background-color: orange")
            else:
                v_button.setStyleSheet("")

    def clear_canvas(self):
        self.canvas.image.fill(Qt.GlobalColor.white)
        self.canvas.update()

    def set_brush_size(self, value):
        self.canvas.brush_size = value

    def set_brush_color(self, color):
        self.canvas.brush_color = color
        self.update_cpick_buttons()

    def selected_pick(self):
        color = QColorDialog.getColor()
        if color.isValid():
            self.set_brush_color(color)
        self.selected_color = color

    def save_image(self):
        file_name, _ = QFileDialog.getSaveFileName(
            self, "Save Image", "", "Images (*.png *.xpm *.jpg)"
        )
        if file_name:
            self.canvas.image.save(file_name)

    def load_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self, "Open Image", "", "Images (*.png *.xpm *.jpg)"
        )
        if file_name:
            self.canvas.image = QImage(file_name)
            self.canvas.update()
