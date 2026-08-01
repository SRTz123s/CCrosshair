"""Загрузка и сохранение настроек прицела."""

import json
import os


class SettingsManager:
    """Управляет файлом настроек crosshair_settings.json."""

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
        'hotkeys': {
            'toggle': 'Ctrl+Shift+C',
            'save': 'Ctrl+Shift+S',
            'reset': 'Ctrl+Shift+R',
        },
    }

    def __init__(self, path="crosshair_settings.json"):
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
