"""Иконка приложения: ищется рядом с exe или в папке проекта."""

import os
import sys

APP_ICON_ICO = "app.ico"
APP_ICON_PNG = "app.png"


def _base_dirs():
    """Папки, где может лежать иконка: рядом с exe, в ресурсах PyInstaller,
    рядом с исходниками."""
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.abspath(__file__))
        base = os.path.dirname(base)  # из ui/ поднимаемся в корень проекта
    dirs = [base]
    meipass = getattr(sys, '_MEIPASS', None)
    if meipass:
        dirs.append(meipass)
    return dirs


def resolve_icon_path():
    """Возвращает путь к иконке приложения (ico или png), если она есть."""
    for base in _base_dirs():
        for name in (APP_ICON_ICO, APP_ICON_PNG):
            path = os.path.join(base, name)
            if os.path.exists(path):
                return path
    return None
