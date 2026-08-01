"""Базовый класс страницы — плавно прокручиваемая область в стиле Zapret2."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QFrame, QSizePolicy, QVBoxLayout, QWidget

from qfluentwidgets import (BodyLabel, SmoothScrollArea, StrongBodyLabel,
                            TitleLabel)

from ui.i18n import t


class BasePage(SmoothScrollArea):
    """Страница с заголовком, подзаголовком и прокручиваемым контентом.

    Заголовки задаются ключами перевода и обновляются методом
    apply_language(language). Скролл контента — плавный (анимированный),
    как в Zapret2.
    """

    def __init__(self, title_key, subtitle_key='', parent=None):
        super().__init__(parent)
        self._lang = 'ru'
        self._title_key = title_key
        self._subtitle_key = subtitle_key
        self._section_labels = []

        self.setWidgetResizable(True)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.setFrameShape(QFrame.Shape.NoFrame)
        self.setStyleSheet("QScrollArea { background-color: transparent; border: none; }")
        self.enableTransparentBackground()

        self.content = QWidget(self)
        self.content.setStyleSheet("background-color: transparent;")
        self.content.setMinimumWidth(0)
        self.content.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        self.setWidget(self.content)

        self.vBoxLayout = QVBoxLayout(self.content)
        self.vBoxLayout.setContentsMargins(36, 28, 36, 32)
        self.vBoxLayout.setSpacing(16)
        self.vBoxLayout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.title_label = TitleLabel(t(self._lang, title_key))
        self.title_label.setObjectName('pageTitle')
        self.vBoxLayout.addWidget(self.title_label)

        if subtitle_key:
            self.subtitle_label = BodyLabel(t(self._lang, subtitle_key))
            self.subtitle_label.setWordWrap(True)
            self.subtitle_label.setMinimumWidth(0)
            self.subtitle_label.setSizePolicy(
                QSizePolicy.Policy.Ignored, QSizePolicy.Policy.Preferred)
            self.vBoxLayout.addWidget(self.subtitle_label)
        else:
            self.subtitle_label = None

    # ------------------------------------------------------------ помощники
    def add_widget(self, widget, stretch=0):
        self.vBoxLayout.addWidget(widget, stretch)

    def add_spacing(self, height=16):
        self.vBoxLayout.addSpacing(height)

    def add_section_title(self, key):
        label = StrongBodyLabel(t(self._lang, key))
        label.setProperty("tone", "primary")
        self._section_labels.append((label, key))
        self.vBoxLayout.addWidget(label)
        return label

    def apply_language(self, language):
        """Обновляет тексты базовых элементов страницы."""
        self._lang = language or 'ru'
        if self._title_key:
            self.title_label.setText(t(self._lang, self._title_key))
        if self.subtitle_label is not None and self._subtitle_key:
            self.subtitle_label.setText(t(self._lang, self._subtitle_key))
        for label, key in self._section_labels:
            label.setText(t(self._lang, key))
