"""Кастомные Fluent-виджеты для страниц настройки прицела."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QColor
from PyQt6.QtWidgets import QPushButton

from qfluentwidgets import (BodyLabel, ColorDialog, SettingCard, Slider,
                            ToolTipFilter)

from ui.i18n import t


def _contrast_text(color):
    """Возвращает чёрный или белый текст для читаемости на фоне color."""
    luminance = 0.2126 * color.red() + 0.7152 * color.green() + 0.0722 * color.blue()
    return '#111111' if luminance > 150 else '#FFFFFF'


class SliderSettingCard(SettingCard):
    """Карточка настройки с ползунком и текущим значением справа."""

    valueChanged = pyqtSignal(int)

    def __init__(self, icon, title, content, minimum, maximum, value,
                 suffix='', parent=None):
        super().__init__(icon, title, content, parent)
        self._suffix = suffix

        self.value_label = BodyLabel(str(value) + suffix)
        self.value_label.setFixedWidth(56)
        self.value_label.setAlignment(
            Qt.AlignmentFlag.AlignRight | Qt.AlignmentFlag.AlignVCenter)

        self.slider = Slider(Qt.Orientation.Horizontal)
        self.slider.setRange(minimum, maximum)
        self.slider.setValue(value)
        self.slider.setFixedWidth(200)
        self.slider.valueChanged.connect(self._on_slider_changed)

        self.hBoxLayout.addWidget(self.value_label, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(8)
        self.hBoxLayout.addWidget(self.slider, 0, Qt.AlignmentFlag.AlignRight)

    def _on_slider_changed(self, value):
        self.value_label.setText(str(value) + self._suffix)
        self.valueChanged.emit(value)

    def value(self):
        return self.slider.value()

    def setValue(self, value):
        self.slider.setValue(value)


class ColorSettingCard(SettingCard):
    """Карточка выбора цвета прицела (открывает Fluent ColorDialog)."""

    colorChanged = pyqtSignal(QColor)

    def __init__(self, icon, title, content, color, parent=None):
        super().__init__(icon, title, content, parent)
        self._lang = 'ru'
        self._color = QColor(color)

        self.swatch_button = QPushButton(self._color.name().upper(), self)
        self.swatch_button.setFixedSize(88, 30)
        self.swatch_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.swatch_button.setToolTip(
            t(self._lang, 'crosshair.color.tooltip'))
        self.swatch_button.clicked.connect(self._open_dialog)
        self._apply_swatch(self._color)

        self.hBoxLayout.addWidget(self.swatch_button, 0, Qt.AlignmentFlag.AlignRight)

    def apply_language(self, language):
        self._lang = language or 'ru'
        self.swatch_button.setToolTip(
            t(self._lang, 'crosshair.color.tooltip'))

    def _apply_swatch(self, color):
        text = _contrast_text(color)
        self.swatch_button.setText(color.name().upper())
        self.swatch_button.setStyleSheet(
            f"QPushButton {{"
            f"  background-color: {color.name()};"
            f"  color: {text};"
            f"  border: 1px solid rgba(0, 0, 0, 0.35);"
            f"  border-radius: 7px;"
            f"  font-weight: 600;"
            f"}}"
            f"QPushButton:hover {{"
            f"  border: 1px solid rgba(255, 255, 255, 0.55);"
            f"}}"
        )

    def _open_dialog(self):
        dialog = ColorDialog(self._color,
                             t(self._lang, 'crosshair.color.dialog'),
                             self.window(), False)
        dialog.colorChanged.connect(self._apply_color)
        dialog.exec()

    def _apply_color(self, color):
        self._color = QColor(color)
        self._apply_swatch(self._color)
        self.colorChanged.emit(QColor(self._color))

    def color(self):
        return QColor(self._color)

    def setColor(self, color):
        self._apply_color(color)
