"""Общее состояние приложения: связывает страницы интерфейса и оверлей прицела."""

from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QColor


class AppState(QObject):
    """Единый источник данных о параметрах прицела и его видимости."""

    paramsChanged = pyqtSignal(dict)
    processesChanged = pyqtSignal(list)
    onlySelectedChanged = pyqtSignal(bool)
    enabledChanged = pyqtSignal(bool)
    programChanged = pyqtSignal(dict)
    hotkeysChanged = pyqtSignal(dict)

    def __init__(self, parent=None):
        super().__init__(parent)
        self.params = {
            'size': 30,
            'color': QColor(0, 255, 0),
            'opacity': 100,
            'thickness': 2,
            'gap': 5,
            'dot': True,
            'dot_size': 3,
            'outline': 0,
        }
        self.selected_processes = []
        self.only_selected = True
        self.enabled = False
        self.program = {
            'theme': 'system',
            'language': 'ru',
            'follow_crosshair_accent': True,
            'follow_windows_accent': False,
            'show_on_startup': False,
            'mica': True,
            'launch_with_windows': False,
        }
        self.hotkeys = {
            'toggle': 'Ctrl+Shift+C',
            'save': 'Ctrl+Shift+S',
            'reset': 'Ctrl+Shift+R',
        }

    # ----------------------------------------------------------- параметры
    def set_param(self, key, value):
        if key in self.params and self.params[key] != value:
            self.params[key] = value
            self.paramsChanged.emit(dict(self.params))

    def set_params(self, params):
        changed = False
        for key, value in params.items():
            if key in self.params and self.params[key] != value:
                self.params[key] = value
                changed = True
        if changed:
            self.paramsChanged.emit(dict(self.params))

    def set_color(self, color):
        self.set_param('color', QColor(color))

    def render_params(self):
        """Параметры для отрисовки прицела (прозрачность в долях)."""
        params = dict(self.params)
        params['opacity'] = params['opacity'] / 100.0
        return params

    # ---------------------------------------------------------- программы
    def set_processes(self, titles):
        titles = list(titles)
        if titles != self.selected_processes:
            self.selected_processes = titles
            self.processesChanged.emit(list(titles))

    def set_only_selected(self, value):
        value = bool(value)
        if value != self.only_selected:
            self.only_selected = value
            self.onlySelectedChanged.emit(value)

    # ----------------------------------------------------------- видимость
    def set_enabled(self, value):
        value = bool(value)
        if value != self.enabled:
            self.enabled = value
            self.enabledChanged.emit(value)

    # ------------------------------------------------------------- программа
    def set_program(self, key, value):
        if key in self.program and self.program[key] != value:
            self.program[key] = value
            self.programChanged.emit(dict(self.program))

    def set_program_many(self, values):
        changed = False
        for key, value in values.items():
            if key in self.program and self.program[key] != value:
                self.program[key] = value
                changed = True
        if changed:
            self.programChanged.emit(dict(self.program))

    # ------------------------------------------------------------ горячие клавиши
    def set_hotkey(self, key, sequence):
        if key in self.hotkeys and self.hotkeys[key] != sequence:
            self.hotkeys[key] = sequence
            self.hotkeysChanged.emit(dict(self.hotkeys))

    def set_hotkeys(self, hotkeys):
        changed = False
        for key, value in hotkeys.items():
            if key in self.hotkeys and self.hotkeys[key] != value:
                self.hotkeys[key] = value
                changed = True
        if changed:
            self.hotkeysChanged.emit(dict(self.hotkeys))
