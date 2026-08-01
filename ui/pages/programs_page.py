"""Страница «Программы» — выбор приложений для показа прицела."""

from PyQt6.QtWidgets import QVBoxLayout

from qfluentwidgets import (CardWidget, FluentIcon, SettingCardGroup,
                            SwitchSettingCard)

from core.process_selector import ProcessSelector
from ui.i18n import t
from ui.pages.base_page import BasePage


class ProgramsPage(BasePage):
    """Настройка режима отображения прицела в конкретных программах."""

    def __init__(self, state, parent=None):
        self.state = state
        super().__init__('programs.title', 'programs.subtitle', parent)
        self._lang = state.program.get('language', 'ru')
        self.setObjectName('programsPage')

        self.add_section_title('programs.section.mode')
        self.mode_group = SettingCardGroup(
            t(self._lang, 'programs.section.mode'), self.content)
        self.only_selected_switch = SwitchSettingCard(
            FluentIcon.GAME, t(self._lang, 'programs.only_selected'),
            t(self._lang, 'programs.only_selected.desc'),
        )
        self.only_selected_switch.setChecked(state.only_selected)
        self.only_selected_switch.checkedChanged.connect(
            state.set_only_selected)
        self.mode_group.addSettingCard(self.only_selected_switch)
        self.add_widget(self.mode_group)
        self.add_spacing(8)

        self.add_section_title('programs.section.list')
        self.list_card = CardWidget(self.content)
        list_layout = QVBoxLayout(self.list_card)
        list_layout.setContentsMargins(16, 14, 16, 14)
        self.selector = ProcessSelector()
        self.selector.selectionChanged.connect(state.set_processes)
        list_layout.addWidget(self.selector)
        self.add_widget(self.list_card)

        self.state.processesChanged.connect(self._on_processes_changed)
        self.selector.select_titles(state.selected_processes)

    def _on_processes_changed(self, titles):
        self.selector.select_titles(titles)

    def apply_state(self):
        """Синхронизирует виджеты с текущим состоянием (после сброса)."""
        self.only_selected_switch.setChecked(self.state.only_selected)
        self.selector.select_titles(self.state.selected_processes)

    def apply_language(self, language):
        super().apply_language(language)
        self._lang = language or 'ru'
        self.mode_group.titleLabel.setText(
            t(self._lang, 'programs.section.mode'))
        self.only_selected_switch.titleLabel.setText(
            t(self._lang, 'programs.only_selected'))
        self.only_selected_switch.contentLabel.setText(
            t(self._lang, 'programs.only_selected.desc'))
        self.selector.apply_language(self._lang)
