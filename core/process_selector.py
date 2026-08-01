"""Виджет выбора активных окон / программ (Fluent-стиль)."""

from PyQt6.QtCore import Qt, QItemSelectionModel, pyqtSignal
from PyQt6.QtGui import QStandardItem, QStandardItemModel
from PyQt6.QtWidgets import QAbstractItemView, QHBoxLayout, QVBoxLayout, QWidget

from qfluentwidgets import CaptionLabel, ListView, PushButton

from ui.i18n import t

from . import windows_api


class ProcessSelector(QWidget):
    """Список активных окон с возможностью множественного выбора."""

    selectionChanged = pyqtSignal(list)

    def __init__(self, parent=None):
        super().__init__(parent)
        self._lang = 'ru'
        self.model = QStandardItemModel(self)
        self.init_ui()
        self.refresh_processes()

    def init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(10)

        self.hint = CaptionLabel(t(self._lang, 'programs.hint'))
        layout.addWidget(self.hint)

        self.process_list = ListView()
        self.process_list.setModel(self.model)
        self.process_list.setSelectionMode(
            QAbstractItemView.SelectionMode.MultiSelection)
        self.process_list.setMinimumHeight(240)
        self.process_list.setMaximumHeight(360)
        self.process_list.selectionModel().selectionChanged.connect(
            lambda *_: self.selectionChanged.emit(self.get_selected_titles()))
        layout.addWidget(self.process_list)

        buttons = QHBoxLayout()
        self.refresh_btn = PushButton(t(self._lang, 'programs.refresh'))
        self.refresh_btn.clicked.connect(self.refresh_processes)
        self.clear_btn = PushButton(t(self._lang, 'programs.clear'))
        self.clear_btn.clicked.connect(self.clear_selection)
        buttons.addWidget(self.refresh_btn)
        buttons.addWidget(self.clear_btn)
        buttons.addStretch()
        layout.addLayout(buttons)

    def apply_language(self, language):
        self._lang = language or 'ru'
        self.hint.setText(t(self._lang, 'programs.hint'))
        self.refresh_btn.setText(t(self._lang, 'programs.refresh'))
        self.clear_btn.setText(t(self._lang, 'programs.clear'))

    def refresh_processes(self):
        self.model.clear()
        seen = set()
        for hwnd, title in windows_api.enum_visible_windows():
            if not title or title in seen:
                continue
            seen.add(title)
            pid = windows_api.get_window_process_pid(hwnd)
            item = QStandardItem(f'{title}   (PID: {pid})')
            item.setData(title, Qt.ItemDataRole.UserRole)
            item.setEditable(False)
            self.model.appendRow(item)

    def clear_selection(self):
        self.process_list.clearSelection()

    def get_selected_titles(self):
        model = self.process_list.selectionModel()
        return [
            self.model.itemFromIndex(index).data(Qt.ItemDataRole.UserRole)
            for index in model.selectedRows()
        ]

    def select_titles(self, titles):
        titles = set(titles)
        selection_model = self.process_list.selectionModel()
        selection_model.blockSignals(True)
        selection_model.clearSelection()
        for row in range(self.model.rowCount()):
            item = self.model.item(row)
            if item.data(Qt.ItemDataRole.UserRole) in titles:
                selection_model.select(
                    self.model.index(row, 0),
                    QItemSelectionModel.SelectionFlag.Select,
                )
        selection_model.blockSignals(False)
        self.selectionChanged.emit(self.get_selected_titles())
