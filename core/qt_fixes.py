"""Исправление проблемы с Qt-плагинами (PyQt5 и PyQt6)."""

import os
import sys


def _plugin_candidates():
    candidates = []
    for package_name, subdir in (("PyQt5", "Qt5"), ("PyQt6", "Qt6")):
        try:
            package = __import__(package_name)
        except Exception:
            continue
        candidates.append(os.path.join(os.path.dirname(package.__file__), subdir, 'plugins'))
    return candidates


def fix_qt_plugins():
    """Выставляет QT_PLUGIN_PATH, если плагины не находятся автоматически."""
    candidates = _plugin_candidates()

    candidates += [
        os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins'),
        os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt5', 'plugins'),
        os.path.join(sys.prefix, 'Lib', 'site-packages', 'PyQt6', 'Qt6', 'plugins'),
        os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages', 'PyQt5', 'Qt5', 'plugins'),
        os.path.join(os.path.dirname(sys.executable), 'Lib', 'site-packages', 'PyQt6', 'Qt6', 'plugins'),
    ]

    for path in candidates:
        if path and os.path.exists(path):
            os.environ['QT_PLUGIN_PATH'] = path
            return True

    return False
