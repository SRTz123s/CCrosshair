"""Точка входа: запуск приложения Custom Crosshair."""

import os
import sys

from PyQt6.QtGui import QIcon
from PyQt6.QtWidgets import QApplication

from config.settings_manager import SettingsManager
from core.qt_fixes import fix_qt_plugins
from core.single_instance import ensure_single_instance
from ui.app_icon import APP_ICON_ICO, APP_ICON_PNG
from ui.main_window import CrosshairFluentWindow
from ui.theme import apply_theme_mode

fix_qt_plugins()

SINGLE_INSTANCE_GUARD = ensure_single_instance()
ICON_CANDIDATES = (APP_ICON_ICO, APP_ICON_PNG)


def main():
    try:
        app = QApplication(sys.argv)
        app.setApplicationName('Custom Crosshair')
        app.setApplicationDisplayName('Custom Crosshair')

        for icon_path in ICON_CANDIDATES:
            if os.path.exists(icon_path):
                app.setWindowIcon(QIcon(icon_path))
                break

        # Тема применяется до создания окна (как в Zapret2), чтобы избежать
        # мигания при запуске.
        settings = SettingsManager()
        apply_theme_mode(settings.load().get('theme', 'system'))

        window = CrosshairFluentWindow()
        window.show()

        sys.exit(app.exec())
    except Exception as exc:
        print(f"Ошибка при запуске: {exc}")
        input("Нажмите Enter для выхода...")


if __name__ == '__main__':
    main()
