"""Страница «Профили» — коды прицела и экспорт/импорт настроек в JSON."""

import json

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QApplication, QFileDialog, QHBoxLayout,
                             QLineEdit)

from qfluentwidgets import (FluentIcon, LineEdit, PrimaryPushButton,
                            PushButton, SettingCard, SettingCardGroup)

from core import profile_codec
from ui.i18n import t
from ui.pages.base_page import BasePage


class ProfilesPage(BasePage):
    """Сохранение настроек прицела в виде кода и полный экспорт в JSON."""

    notify = pyqtSignal(str, str, bool)
    importApplied = pyqtSignal()

    def __init__(self, state, parent=None):
        self.state = state
        super().__init__('profiles.title', 'profiles.subtitle', parent)
        self._lang = state.program.get('language', 'ru')
        self.setObjectName('profilesPage')

        # ──────────────────────────────── код прицела
        self.add_section_title('profiles.section.crosshair')
        self.crosshair_group = SettingCardGroup(
            t(self._lang, 'profiles.section.crosshair'), self.content)

        self.copy_card = SettingCard(
            FluentIcon.COPY, t(self._lang, 'profiles.copy'),
            t(self._lang, 'profiles.copy.desc'),
        )
        self.copy_btn = PrimaryPushButton(t(self._lang, 'profiles.copy.btn'))
        self.copy_btn.setFixedHeight(34)
        self.copy_btn.clicked.connect(self._copy_code)
        self.copy_card.hBoxLayout.addWidget(
            self.copy_btn, 0, Qt.AlignmentFlag.AlignRight)
        self.crosshair_group.addSettingCard(self.copy_card)

        self.apply_card = SettingCard(
            FluentIcon.LINK, t(self._lang, 'profiles.apply'),
            t(self._lang, 'profiles.apply.desc'),
        )
        self.code_edit = LineEdit(self)
        self.code_edit.setPlaceholderText(
            t(self._lang, 'profiles.apply.placeholder'))
        self.code_edit.setMinimumWidth(280)
        self.apply_btn = PushButton(t(self._lang, 'profiles.apply.btn'))
        self.apply_btn.setFixedHeight(34)
        self.apply_btn.clicked.connect(self._apply_code)
        self.code_edit.returnPressed.connect(self._apply_code)
        row = QHBoxLayout()
        row.addWidget(self.code_edit)
        row.addSpacing(8)
        row.addWidget(self.apply_btn)
        self.apply_card.hBoxLayout.addLayout(row)
        self.crosshair_group.addSettingCard(self.apply_card)
        self.add_widget(self.crosshair_group)
        self.add_spacing(8)

        # ──────────────────────────────── настройки программы
        self.add_section_title('profiles.section.program')
        self.program_group = SettingCardGroup(
            t(self._lang, 'profiles.section.program'), self.content)

        self.export_card = SettingCard(
            FluentIcon.SAVE, t(self._lang, 'profiles.export'),
            t(self._lang, 'profiles.export.desc'),
        )
        self.export_btn = PushButton(t(self._lang, 'profiles.export.btn'))
        self.export_btn.setFixedHeight(34)
        self.export_btn.clicked.connect(self._export_json)
        self.export_card.hBoxLayout.addWidget(
            self.export_btn, 0, Qt.AlignmentFlag.AlignRight)
        self.program_group.addSettingCard(self.export_card)

        self.import_card = SettingCard(
            FluentIcon.FOLDER, t(self._lang, 'profiles.import'),
            t(self._lang, 'profiles.import.desc'),
        )
        self.import_btn = PushButton(t(self._lang, 'profiles.import.btn'))
        self.import_btn.setFixedHeight(34)
        self.import_btn.clicked.connect(self._import_json)
        self.import_card.hBoxLayout.addWidget(
            self.import_btn, 0, Qt.AlignmentFlag.AlignRight)
        self.program_group.addSettingCard(self.import_card)
        self.add_widget(self.program_group)

    # ------------------------------------------------------------ действия
    def _copy_code(self):
        code = profile_codec.encode_crosshair(self.state.params)
        QApplication.clipboard().setText(code)
        self.notify.emit(t(self._lang, 'profiles.copied'),
                         t(self._lang, 'profiles.copied.desc'), True)

    def _apply_code(self):
        code = self.code_edit.text().strip()
        params = profile_codec.decode_crosshair(code)
        if params is None:
            self.notify.emit(t(self._lang, 'profiles.invalid'),
                             t(self._lang, 'profiles.invalid.desc'), False)
            return
        self.state.set_params(params)
        self.notify.emit(t(self._lang, 'profiles.applied'),
                         t(self._lang, 'profiles.applied.desc'), True)

    def _export_json(self):
        path, _ = QFileDialog.getSaveFileName(
            self, t(self._lang, 'profiles.export.title'),
            'custom_crosshair_settings.json', 'JSON (*.json)')
        if not path:
            return
        data = profile_codec.export_json(self.state)
        try:
            with open(path, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as exc:
            self.notify.emit(t(self._lang, 'profiles.export.failed'),
                             str(exc), False)
            return
        self.notify.emit(t(self._lang, 'profiles.exported'),
                         path, True)

    def _import_json(self):
        path, _ = QFileDialog.getOpenFileName(
            self, t(self._lang, 'profiles.import.title'), '',
            'JSON (*.json)')
        if not path:
            return
        try:
            with open(path, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except (OSError, ValueError) as exc:
            self.notify.emit(t(self._lang, 'profiles.import.failed'),
                             str(exc), False)
            return
        params, program, hotkeys, processes, only_selected = \
            profile_codec.import_json(data)
        if params:
            self.state.set_params(params)
        if program:
            self.state.set_program_many(program)
        if hotkeys:
            self.state.set_hotkeys(hotkeys)
        self.state.set_processes(processes)
        self.state.set_only_selected(only_selected)
        self.importApplied.emit()
        self.notify.emit(t(self._lang, 'profiles.imported'),
                         path, True)

    # ------------------------------------------------------------ перевод
    def apply_language(self, language):
        super().apply_language(language)
        self._lang = language or 'ru'
        self.crosshair_group.titleLabel.setText(
            t(self._lang, 'profiles.section.crosshair'))
        self.program_group.titleLabel.setText(
            t(self._lang, 'profiles.section.program'))

        self.copy_card.titleLabel.setText(t(self._lang, 'profiles.copy'))
        self.copy_card.contentLabel.setText(t(self._lang, 'profiles.copy.desc'))
        self.copy_btn.setText(t(self._lang, 'profiles.copy.btn'))

        self.apply_card.titleLabel.setText(t(self._lang, 'profiles.apply'))
        self.apply_card.contentLabel.setText(
            t(self._lang, 'profiles.apply.desc'))
        self.apply_btn.setText(t(self._lang, 'profiles.apply.btn'))
        self.code_edit.setPlaceholderText(
            t(self._lang, 'profiles.apply.placeholder'))

        self.export_card.titleLabel.setText(t(self._lang, 'profiles.export'))
        self.export_card.contentLabel.setText(
            t(self._lang, 'profiles.export.desc'))
        self.export_btn.setText(t(self._lang, 'profiles.export.btn'))

        self.import_card.titleLabel.setText(t(self._lang, 'profiles.import'))
        self.import_card.contentLabel.setText(
            t(self._lang, 'profiles.import.desc'))
        self.import_btn.setText(t(self._lang, 'profiles.import.btn'))
