"""Живой предпросмотр прицела."""

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QWidget

from core.crosshair_renderer import draw_crosshair


class CrosshairPreview(QWidget):
    """Мини-окно, показывающее текущий вид прицела."""

    def __init__(self, parent=None):
        super().__init__(parent)
        self.params = {
            'size': 30,
            'color': QColor(0, 255, 0),
            'opacity': 1.0,
            'gap': 5,
            'thickness': 2,
            'dot': True,
            'dot_size': 3,
            'outline': 0,
        }
        self.setMinimumSize(150, 150)
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground, True)

    def set_params(self, **kwargs):
        self.params.update(kwargs)
        self.update()

    def paintEvent(self, _event):
        painter = QPainter(self)
        rect = self.rect().adjusted(10, 10, -10, -10)
        center = QPoint(rect.left() + rect.width() // 2,
                        rect.top() + rect.height() // 2)
        draw_crosshair(painter, center, **self.params)
