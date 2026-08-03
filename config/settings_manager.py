"""Загрузка и сохранение настроек прицела."""

import json
import os
import sys


def app_base_dir():
    """Папка, в которой живут настройки и иконка: рядом с exe (сборка)
    или в корне проекта (запуск из исходников)."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class SettingsManager:
    """Управляет файлом настроек crosshair_settings.json.

    Файл сохраняется рядом с exe (куда бы пользователь ни установил
    программу), поэтому настройки не зависят от текущей папки запуска.
    """

    DEFAULTS = {
        'size': 30,
        'color': '#00FF00',
        'opacity': 100,
        'thickness': 2,
        'gap': 5,
        'dot': True,
        'dot_size': 3,
        'outline': 0,
        'selected_processes': [],
        'theme': 'system',
        'language': 'ru',
        'follow_crosshair_accent': True,
        'follow_windows_accent': False,
        'show_on_startup': False,
        'mica': True,
        'launch_with_windows': False,
        'window_width': 880,
        'window_height': 640,
        'hotkeys': {
            'toggle': 'Ctrl+Shift+C',
            'save': 'Ctrl+Shift+S',
            'reset': 'Ctrl+Shift+R',
        },
    }

    def __init__(self, path=None):
        if path is None:
            path = os.path.join(app_base_dir(), "crosshair_settings.json")
        self.path = path

    def load(self):
        """Возвращает настройки, дополняя недостающие значениями по умолчанию."""
        if not os.path.exists(self.path):
            return dict(self.DEFAULTS)
        try:
            with open(self.path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            merged = dict(self.DEFAULTS)
            merged.update({k: v for k, v in data.items() if k in merged})
            return merged
        except Exception:
            return dict(self.DEFAULTS)

    def save(self, data):
        """Сохраняет настройки в JSON-файл."""
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)

    @classmethod
    def reset(cls):
        """Возвращает настройки по умолчанию."""
        return dict(cls.DEFAULTS)
