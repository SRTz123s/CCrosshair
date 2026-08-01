"""Страница «О программе»."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

from qfluentwidgets import (CaptionLabel, CardWidget, FluentIcon,
                            StrongBodyLabel)

from ui.app_icon import resolve_icon_path
from ui.i18n import t
from ui.pages.base_page import BasePage


class AboutPage(BasePage):
    """Информация о приложении."""

    def __init__(self, parent=None):
        super().__init__('about.title', 'about.subtitle', parent)
        self._lang = 'ru'
        self.setObjectName('aboutPage')

        self.add_section_title('about.section.app')
        self.app_card = CardWidget(self.content)
        app_layout = QHBoxLayout(self.app_card)
        app_layout.setContentsMargins(24, 20, 24, 20)
        app_layout.setSpacing(24)

        icon_path = resolve_icon_path()
        if icon_path:
            icon_label = self._make_icon_label(icon_path)
            app_layout.addWidget(icon_label, 0, Qt.AlignmentFlag.AlignTop)

        texts = QVBoxLayout()
        texts.setSpacing(6)
        self.name_label = StrongBodyLabel('Custom Crosshair')
        self.version_label = CaptionLabel(t(self._lang, 'about.version'))
        self.description_label = CaptionLabel(
            t(self._lang, 'about.desc'))
        self.description_label.setWordWrap(True)
        texts.addWidget(self.name_label)
        texts.addWidget(self.version_label)
        texts.addSpacing(4)
        texts.addWidget(self.description_label)
        texts.addStretch()
        app_layout.addLayout(texts, 1)
        self.add_widget(self.app_card)

    def apply_language(self, language):
        super().apply_language(language)
        self._lang = language or 'ru'
        self.version_label.setText(t(self._lang, 'about.version'))
        self.description_label.setText(t(self._lang, 'about.desc'))

    def _make_icon_label(self, icon_path):
        from PyQt6.QtGui import QPixmap
        from PyQt6.QtWidgets import QLabel
        pixmap = QPixmap(icon_path)
        pixmap = pixmap.scaled(
            96, 96,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        label = QLabel()
        label.setFixedSize(96, 96)
        label.setPixmap(pixmap)
        return label
