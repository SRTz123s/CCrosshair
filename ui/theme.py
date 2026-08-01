"""Синхронизация темы интерфейса (тёмная / светлая / системная)."""

from qfluentwidgets import Theme, setTheme


def theme_to_qfluent(theme_mode):
    """Переводит строковый режим темы в Theme из qfluentwidgets."""
    if theme_mode == 'dark':
        return Theme.DARK
    if theme_mode == 'light':
        return Theme.LIGHT
    return Theme.AUTO


def apply_theme_mode(theme_mode):
    """Применяет режим темы ко всему приложению."""
    setTheme(theme_to_qfluent(theme_mode))
