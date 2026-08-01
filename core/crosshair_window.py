"""Оверлей прицела, который всегда поверх всех окон."""

from PyQt6.QtCore import QPoint, Qt
from PyQt6.QtGui import QColor, QPainter
from PyQt6.QtWidgets import QApplication, QWidget

from .crosshair_renderer import draw_crosshair
from .windows_api import remove_window_shadow


class CrosshairWindow(QWidget):
    """Прозрачное окно прицела поверх экрана."""

    def __init__(self):
        super().__init__()
        self.setWindowFlags(
            Qt.WindowType.WindowStaysOnTopHint
            | Qt.WindowType.FramelessWindowHint
            | Qt.WindowType.Tool
        )
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        self.setWindowOpacity(1.0)
        self.setStyleSheet("QWidget { background: transparent; }")
        self.setFixedSize(240, 240)

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
        self.visible = False
        try:
            remove_window_shadow(int(self.winId()))
        except Exception:
            pass

    def paintEvent(self, _event):
        painter = QPainter(self)
        draw_crosshair(painter, QPoint(self.width() // 2, self.height() // 2),
                       **self.params)

    def update_crosshair(self, **kwargs):
        """Обновляет параметры прицела и перерисовывает его."""
        fit = ('size' in kwargs or 'thickness' in kwargs
               or 'outline' in kwargs)
        for key, value in kwargs.items():
            if key in self.params:
                self.params[key] = value
        if fit:
            self._fit_window()
        self.update()

    def _fit_window(self):
        """Подгоняет размер окна под большой прицел."""
        outline = self.params.get('outline', 0)
        needed = max(60, self.params['size']
                     + (self.params['thickness'] + 2 * outline) * 2 + 24)
        self.setFixedSize(needed, needed)
        if self.isVisible():
            self.center_on_screen()

    def center_on_screen(self):
        """Ставит центр прицела точно в центр монитора."""
        screen = QApplication.primaryScreen()
        if screen is None:
            return
        geo = screen.geometry()
        self.move(geo.x() + (geo.width() - self.width()) // 2,
                  geo.y() + (geo.height() - self.height()) // 2)

    def show_crosshair(self):
        self.setWindowOpacity(1.0)
        self.show()
        self.center_on_screen()

    def toggle_visibility(self):
        """Включает/выключает прицел, возвращает новое состояние."""
        self.visible = not self.visible
        if self.visible:
            self.show_crosshair()
        else:
            self.hide()
        return self.visible
