import math
from datetime import datetime

from PyQt6.QtCore import QPointF
from PyQt6.QtCore import Qt
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QColor
from PyQt6.QtGui import QPainter
from PyQt6.QtGui import QPen
from PyQt6.QtWidgets import QWidget


class WindowClass(QWidget):
    def __init__(self):
        super().__init__()
        self.circle_radius = 200
        self.offset = math.pi / 2
        self.center = QPointF(self.circle_radius, self.circle_radius)
        self.timer = QTimer()
        self.timer.timeout.connect(self.update)
        self.timer.start(1000)

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        self.draw_circle(painter)
        self.draw_clock_hands(painter)
        self.draw_hours(painter)
        self.draw_minutes(painter)

    def draw_circle(self, painter):
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        painter.drawEllipse(self.center, self.circle_radius, self.circle_radius)

    def draw_clock_hands(self, painter):
        hour_theta, minute_theta, second_theta = self.get_theta()

        self.draw_clock_hand(
            painter, self.circle_radius * 0.95, hour_theta, QColor(255, 0, 0)
        )
        self.draw_clock_hand(
            painter, self.circle_radius * 0.80, minute_theta, QColor(0, 255, 0)
        )
        self.draw_clock_hand(
            painter, self.circle_radius * 0.65, second_theta, QColor(0, 0, 255)
        )

    def draw_clock_hand(self, painter, radius, theta, color):
        pen = QPen(color, 3)
        painter.setPen(pen)
        end_point = QPointF(
            self.center.x() - radius * math.cos(theta),
            self.center.y() - radius * math.sin(theta),
        )
        painter.drawLine(self.center, end_point)

    def draw_hours(self, painter):
        pen = QPen(Qt.GlobalColor.black, 2)
        painter.setPen(pen)
        for hr in range(12):
            theta = (hr * ((2 * math.pi) / 12)) + self.offset
            start_point = QPointF(
                self.center.x() + (self.circle_radius * 0.90 * math.cos(theta)),
                self.center.y() - (self.circle_radius * 0.90 * math.sin(theta)),
            )
            end_point = QPointF(
                self.center.x() + (self.circle_radius * math.cos(theta)),
                self.center.y() - (self.circle_radius * math.sin(theta)),
            )
            painter.drawLine(start_point, end_point)

    def draw_minutes(self, painter):
        pen = QPen(Qt.GlobalColor.black, 1)
        painter.setPen(pen)
        for minute in range(60):
            theta = (minute * ((2.0 * math.pi) / 60.0)) + self.offset
            start_point = QPointF(
                self.center.x() + (self.circle_radius * 0.95 * math.cos(theta)),
                self.center.y() - (self.circle_radius * 0.95 * math.sin(theta)),
            )
            end_point = QPointF(
                self.center.x() + (self.circle_radius * math.cos(theta)),
                self.center.y() - (self.circle_radius * math.sin(theta)),
            )
            painter.drawLine(start_point, end_point)

    def get_theta(self):
        now = datetime.now()
        seconds_frac = now.second
        minutes_frac = now.minute + (seconds_frac / 60.0)
        hours_frac = now.hour + (now.minute / 60.0)

        hour_theta = (hours_frac * ((2.0 * math.pi) / 12.0)) + self.offset
        minute_theta = (minutes_frac * ((2.0 * math.pi) / 60.0)) + self.offset
        second_theta = (seconds_frac * ((2.0 * math.pi) / 60.0)) + self.offset

        return hour_theta, minute_theta, second_theta
