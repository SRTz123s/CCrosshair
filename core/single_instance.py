"""Защита от повторного запуска приложения.

Создаётся Win32-named mutex (global, чтобы работало для других сессий).
Если mutex уже существует — значит приложение уже запущено,
повторный запуск активирует существующее окно и завершается.
"""

import ctypes
import sys

from core import windows_api

# Обязательный префикс Global\ для мутексов, разделяемых между сессиями
MUTEX_NAME = r"Global\CustomCrosshair.SingleInstance"

ERROR_ALREADY_EXISTS = 183

MUTEX_ALL_ACCESS = 0x1F0001


class SingleInstanceGuard:
    """Держит named-mutex на время жизни приложения."""

    def __init__(self, name):
        kernel32 = ctypes.windll.kernel32
        self.handle = kernel32.CreateMutexW(None, False, name)
        self.is_first = (
            kernel32.GetLastError() != ERROR_ALREADY_EXISTS
        )

    def release(self):
        if self.handle:
            ctypes.windll.kernel32.CloseHandle(self.handle)
            self.handle = None


def ensure_single_instance():
    """Возвращает объект-хранитель, если это первый экземпляр.

    Если уже запущен другой экземпляр — пытается вернуть его окно на передний
    план и завершает текущий процесс с кодом 0. Родитель (main.py) должен
    после вызова соответственно выйти.
    """
    guard = SingleInstanceGuard(MUTEX_NAME)
    if guard.is_first:
        return guard

    # Повторный запуск: пытаемся активировать уже открытое окно
    activated = False
    try:
        activated = windows_api.activate_existing_window(
            windows_api.MAIN_WINDOW_TITLE)
    except Exception:
        activated = False

    guard.release()

    if not activated:
        try:
            from PyQt6.QtWidgets import QMessageBox
            QMessageBox.information(
                None, 'CustomCrosshair',
                'Программа уже запущена. См. значок в трее.')
        except Exception:
            pass
    sys.exit(0)
    return None