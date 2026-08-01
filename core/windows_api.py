"""Низкоуровневые обёртки над Win32 API."""

import ctypes
import winreg

user32 = ctypes.windll.user32


def get_foreground_window_title():
    """Возвращает заголовок активного окна или None."""
    hwnd = user32.GetForegroundWindow()
    length = user32.GetWindowTextLengthW(hwnd)
    if length <= 0:
        return None
    buffer = ctypes.create_unicode_buffer(length + 1)
    user32.GetWindowTextW(hwnd, buffer, length + 1)
    return buffer.value


def enum_visible_windows():
    """Возвращает список (hwnd, title) видимых окон с непустым заголовком."""
    windows = []

    @ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    def _callback(hwnd, _lparam):
        if user32.IsWindowVisible(hwnd):
            length = user32.GetWindowTextLengthW(hwnd)
            if length > 0:
                buffer = ctypes.create_unicode_buffer(length + 1)
                user32.GetWindowTextW(hwnd, buffer, length + 1)
                windows.append((hwnd, buffer.value))
        return True

    user32.EnumWindows(_callback, 0)
    return windows


def get_window_process_pid(hwnd):
    """Возвращает PID процесса, которому принадлежит окно."""
    pid = ctypes.c_ulong()
    user32.GetWindowThreadProcessId(hwnd, ctypes.byref(pid))
    return pid.value


def get_windows_theme():
    """Возвращает 'dark' или 'light' в зависимости от темы Windows."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CURRENT_USER,
            r"Software\Microsoft\Windows\CurrentVersion\Themes\Personalize",
        )
        value, _ = winreg.QueryValueEx(key, "AppsUseLightTheme")
        winreg.CloseKey(key)
        return "dark" if value == 0 else "light"
    except OSError:
        return "light"


def get_windows_accent_color():
    """Возвращает системный акцентный цвет Windows в виде '#RRGGBB' или None."""
    try:
        dwmapi = ctypes.windll.dwmapi
        color = ctypes.c_uint()
        opaque = ctypes.c_int()
        dwmapi.DwmGetColorizationColor(ctypes.byref(color), ctypes.byref(opaque))
        value = color.value & 0xFFFFFF
        red = value >> 16
        green = (value >> 8) & 0xFF
        blue = value & 0xFF
        return '#%02X%02X%02X' % (red, green, blue)
    except Exception:
        return None


def remove_window_shadow(hwnd):
    """Отключает системную тень и неклиентскую отрисовку окна через DWM.

    У прозрачного бескаркасного окна-оверлея Windows может рисовать тень
    вокруг прямоугольника окна. Эта функция убирает её.
    """
    try:
        dwmapi = ctypes.windll.dwmapi
        DWMWA_NCRENDERING_POLICY = 2
        DWMNCRP_DISABLED = 1
        policy = ctypes.c_int(DWMNCRP_DISABLED)
        dwmapi.DwmSetWindowAttribute(
            hwnd, DWMWA_NCRENDERING_POLICY,
            ctypes.byref(policy), ctypes.sizeof(policy))
    except Exception:
        pass
