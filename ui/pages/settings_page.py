"""Страница «Настройки» с подвкладками «Программа» и «Горячие клавиши»."""

from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtWidgets import (QHBoxLayout, QKeySequenceEdit, QStackedWidget,
                             QVBoxLayout, QWidget)

from PyQt6.QtGui import QKeySequence

from qfluentwidgets import (CaptionLabel, ComboBox, FluentIcon,
                            PrimaryPushButton, PushButton, SegmentedWidget,
                            SettingCard, SettingCardGroup,
                            SwitchSettingCard)

from ui.i18n import LANGUAGES, t
from ui.pages.base_page import BasePage


class ThemeSettingCard(SettingCard):
    """Карточка выбора темы интерфейса (авто / тёмная / светлая)."""

    themeModeChanged = pyqtSignal(str)

    def __init__(self, icon, title, content, theme_mode, parent=None):
        super().__init__(icon, title, content, parent)
        self.segmented = SegmentedWidget(self)
        self.setThemeTexts('Авто', 'Тёмная', 'Светлая')
        self.segmented.setCurrentItem(theme_mode)
        self.segmented.currentItemChanged.connect(self._on_changed)
        self.hBoxLayout.addWidget(self.segmented, 0, Qt.AlignmentFlag.AlignRight)

    def _on_changed(self, route_key):
        self.themeModeChanged.emit(route_key)

    def setThemeMode(self, mode):
        self.segmented.blockSignals(True)
        self.segmented.setCurrentItem(mode)
        self.segmented.blockSignals(False)

    def setThemeTexts(self, auto_text, dark_text, light_text):
        keys = ('system', 'dark', 'light')
        texts = (auto_text, dark_text, light_text)
        items = getattr(self.segmented, 'items', {})
        for key, text in zip(keys, texts):
            if key in items:
                self.segmented.setItemText(key, text)
            else:
                self.segmented.addItem(key, text)


class LanguageSettingCard(SettingCard):
    """Карточка выбора языка интерфейса."""

    languageChanged = pyqtSignal(str)

    def __init__(self, icon, title, content, language, parent=None):
        super().__init__(icon, title, content, parent)
        self.combo = ComboBox(self)
        for lang, label in LANGUAGES.items():
            self.combo.addItem(label, userData=lang)
        self.setLanguage(language)
        self.combo.currentIndexChanged.connect(self._on_changed)
        self.hBoxLayout.addWidget(self.combo, 0, Qt.AlignmentFlag.AlignRight)

    def _on_changed(self, _index):
        self.languageChanged.emit(self.combo.currentData())

    def setLanguage(self, language):
        langs = list(LANGUAGES)
        index = langs.index(language) if language in langs else 0
        self.combo.blockSignals(True)
        self.combo.setCurrentIndex(index)
        self.combo.blockSignals(False)


class HotkeySettingCard(SettingCard):
    """Карточка настройки горячей клавиши с записью комбинации."""

    hotkeyChanged = pyqtSignal(str)

    def __init__(self, icon, title, content, sequence, parent=None):
        super().__init__(icon, title, content, parent)
        self.edit = QKeySequenceEdit(QKeySequence(sequence), self)
        self.edit.setMinimumHeight(34)
        self.edit.setMaximumWidth(240)
        self.edit.keySequenceChanged.connect(self._on_changed)
        self.hBoxLayout.addWidget(self.edit, 0, Qt.AlignmentFlag.AlignRight)

    def _on_changed(self, sequence):
        text = sequence.toString(QKeySequence.SequenceFormat.PortableText)
        if text:
            self.hotkeyChanged.emit(text)

    def setSequence(self, sequence):
        self.edit.blockSignals(True)
        self.edit.setKeySequence(QKeySequence(sequence))
        self.edit.blockSignals(False)


class ActionsSettingCard(SettingCard):
    """Карточка действий: сохранение и сброс настроек."""

    saveClicked = pyqtSignal()
    resetClicked = pyqtSignal()

    def __init__(self, icon, title, content, parent=None):
        super().__init__(icon, title, content, parent)
        self.save_btn = PrimaryPushButton('Сохранить')
        self.save_btn.setFixedHeight(34)
        self.save_btn.clicked.connect(self.saveClicked)
        self.reset_btn = PushButton('Сбросить')
        self.reset_btn.setFixedHeight(34)
        self.reset_btn.clicked.connect(self.resetClicked)
        self.hBoxLayout.addWidget(self.save_btn, 0, Qt.AlignmentFlag.AlignRight)
        self.hBoxLayout.addSpacing(8)
        self.hBoxLayout.addWidget(self.reset_btn, 0, Qt.AlignmentFlag.AlignRight)


class SettingsPage(BasePage):
    """Настройки программы: подвкладки «Программа» и «Горячие клавиши»."""

    themeModeChanged = pyqtSignal(str)
    languageChanged = pyqtSignal(str)
    saveRequested = pyqtSignal()
    resetRequested = pyqtSignal()

    def __init__(self, state, parent=None):
        self.state = state
        super().__init__('settings.title', 'settings.subtitle', parent)
        self._lang = state.program.get('language', 'ru')
        self.setObjectName('settingsPage')

        # ──────────────────────────────── подвкладки
        self.sub_tabs = SegmentedWidget()
        self._sub_items = getattr(self.sub_tabs, 'items', {})
        self.sub_tabs.addItem('program', t(self._lang, 'settings.tab.program'))
        self.sub_tabs.addItem('hotkeys', t(self._lang, 'settings.tab.hotkeys'))
        self.sub_tabs.currentItemChanged.connect(self._switch_sub_tab)
        self.add_widget(self.sub_tabs)
        self.add_spacing(8)

        self.stack = QStackedWidget()
        self.program_page = QWidget()
        self.hotkeys_page = QWidget()
        self.stack.addWidget(self.program_page)
        self.stack.addWidget(self.hotkeys_page)
        self.add_widget(self.stack)

        self._build_program_tab()
        self._build_hotkeys_tab()

        self.state.programChanged.connect(self._on_program_changed)

    # ------------------------------------------------------------ helpers
    def _section_title(self, key, layout):
        from qfluentwidgets import StrongBodyLabel
        label = StrongBodyLabel(t(self._lang, key))
        label.setProperty("tone", "primary")
        layout.addWidget(label)
        return label

    # ----------------------------------------------------------- вкладка «Программа»
    def _build_program_tab(self):
        layout = QVBoxLayout(self.program_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.program_section_title = self._section_title(
            'settings.section.theme', layout)
        self.theme_group = SettingCardGroup(
            t(self._lang, 'settings.section.theme'), self.program_page)
        self.theme_card = ThemeSettingCard(
            FluentIcon.PALETTE, t(self._lang, 'settings.theme'),
            t(self._lang, 'settings.theme.desc'),
            self.state.program['theme'],
        )
        self.theme_card.themeModeChanged.connect(self.themeModeChanged)
        self.theme_group.addSettingCard(self.theme_card)
        layout.addWidget(self.theme_group)
        layout.addSpacing(12)

        self.app_section_title = self._section_title(
            'settings.section.app', layout)
        self.app_group = SettingCardGroup(
            t(self._lang, 'settings.section.app'), self.program_page)

        self.language_card = LanguageSettingCard(
            FluentIcon.FONT, t(self._lang, 'settings.language'),
            t(self._lang, 'settings.language.desc'),
            self.state.program['language'],
        )
        self.language_card.languageChanged.connect(self.languageChanged)
        self.app_group.addSettingCard(self.language_card)

        self.follow_crosshair_switch = SwitchSettingCard(
            FluentIcon.BRUSH, t(self._lang, 'settings.accent.crosshair'),
            t(self._lang, 'settings.accent.crosshair.desc'),
        )
        self.follow_crosshair_switch.setChecked(
            bool(self.state.program['follow_crosshair_accent']))
        self.follow_crosshair_switch.checkedChanged.connect(
            lambda v: self.state.set_program('follow_crosshair_accent', v))
        self.app_group.addSettingCard(self.follow_crosshair_switch)

        self.follow_windows_switch = SwitchSettingCard(
            FluentIcon.APPLICATION, t(self._lang, 'settings.accent.windows'),
            t(self._lang, 'settings.accent.windows.desc'),
        )
        self.follow_windows_switch.setChecked(
            bool(self.state.program['follow_windows_accent']))
        self.follow_windows_switch.checkedChanged.connect(
            lambda v: self.state.set_program('follow_windows_accent', v))
        self.app_group.addSettingCard(self.follow_windows_switch)

        self.mica_switch = SwitchSettingCard(
            FluentIcon.PALETTE, t(self._lang, 'settings.mica'),
            t(self._lang, 'settings.mica.desc'),
        )
        self.mica_switch.setChecked(bool(self.state.program['mica']))
        self.mica_switch.checkedChanged.connect(
            lambda v: self.state.set_program('mica', v))
        self.app_group.addSettingCard(self.mica_switch)

        self.startup_switch = SwitchSettingCard(
            FluentIcon.PLAY_SOLID, t(self._lang, 'settings.startup'),
            t(self._lang, 'settings.startup.desc'),
        )
        self.startup_switch.setChecked(
            bool(self.state.program['show_on_startup']))
        self.startup_switch.checkedChanged.connect(
            lambda v: self.state.set_program('show_on_startup', v))
        self.app_group.addSettingCard(self.startup_switch)
        layout.addWidget(self.app_group)
        layout.addSpacing(12)

        self.actions_section_title = self._section_title(
            'settings.section.actions', layout)
        self.actions_group = SettingCardGroup(
            t(self._lang, 'settings.section.actions'), self.program_page)
        self.actions_card = ActionsSettingCard(
            FluentIcon.SETTING, t(self._lang, 'settings.actions'),
            t(self._lang, 'settings.actions.desc'),
        )
        self.actions_card.saveClicked.connect(self.saveRequested)
        self.actions_card.resetClicked.connect(self.resetRequested)
        self.actions_group.addSettingCard(self.actions_card)
        layout.addWidget(self.actions_group)
        layout.addStretch()

    # --------------------------------------------------------- вкладка «Горячие клавиши»
    def _build_hotkeys_tab(self):
        layout = QVBoxLayout(self.hotkeys_page)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignmentFlag.AlignTop)

        self.hotkeys_section_title = self._section_title(
            'settings.section.hotkeys', layout)
        self.hotkeys_group = SettingCardGroup(
            t(self._lang, 'settings.section.hotkeys'), self.hotkeys_page)

        self.hotkey_cards = {}
        for key, icon, title_key, desc_key in (
            ('toggle', FluentIcon.PLAY, 'hotkeys.toggle',
             'hotkeys.toggle.desc'),
            ('save', FluentIcon.SAVE, 'hotkeys.save', 'hotkeys.save.desc'),
            ('reset', FluentIcon.SYNC, 'hotkeys.reset',
             'hotkeys.reset.desc'),
        ):
            card = HotkeySettingCard(
                icon, t(self._lang, title_key), t(self._lang, desc_key),
                self.state.hotkeys[key],
            )
            card.hotkeyChanged.connect(
                lambda seq, k=key: self.state.set_hotkey(k, seq))
            self.hotkey_cards[key] = card
            self.hotkeys_group.addSettingCard(card)

        self.hotkey_titles = {
            'toggle': ('hotkeys.toggle', 'hotkeys.toggle.desc'),
            'save': ('hotkeys.save', 'hotkeys.save.desc'),
            'reset': ('hotkeys.reset', 'hotkeys.reset.desc'),
        }
        layout.addWidget(self.hotkeys_group)
        layout.addSpacing(12)

        self.hotkeys_hint = CaptionLabel(t(self._lang, 'hotkeys.tip'))
        self.hotkeys_hint.setWordWrap(True)
        layout.addWidget(self.hotkeys_hint)

        row = QHBoxLayout()
        self.reset_hotkeys_btn = PushButton(
            t(self._lang, 'hotkeys.reset_all'))
        self.reset_hotkeys_btn.clicked.connect(self._reset_hotkeys)
        row.addWidget(self.reset_hotkeys_btn)
        row.addStretch()
        layout.addLayout(row)
        layout.addStretch()

    def _reset_hotkeys(self):
        from config.settings_manager import SettingsManager
        defaults = SettingsManager.DEFAULTS.get('hotkeys', {})
        self.state.set_hotkeys(dict(defaults))
        for key, card in self.hotkey_cards.items():
            card.setSequence(self.state.hotkeys[key])

    def _switch_sub_tab(self, route_key):
        index = 1 if route_key == 'hotkeys' else 0
        self.stack.setCurrentIndex(index)

    # ------------------------------------------------------------ события
    def _on_program_changed(self, program):
        self.follow_crosshair_switch.setChecked(
            bool(program['follow_crosshair_accent']))
        self.follow_windows_switch.setChecked(
            bool(program['follow_windows_accent']))
        self.mica_switch.setChecked(bool(program['mica']))
        self.startup_switch.setChecked(bool(program['show_on_startup']))

    def apply_state(self):
        """Синхронизирует виджеты с текущим состоянием (после сброса)."""
        self.theme_card.setThemeMode(self.state.program['theme'])
        self.language_card.setLanguage(self.state.program['language'])
        self._on_program_changed(self.state.program)
        for key, card in self.hotkey_cards.items():
            card.setSequence(self.state.hotkeys[key])

    def apply_language(self, language):
        super().apply_language(language)
        self._lang = language or 'ru'
        self.sub_tabs.setItemText('program', t(self._lang, 'settings.tab.program'))
        self.sub_tabs.setItemText('hotkeys', t(self._lang, 'settings.tab.hotkeys'))

        self.theme_group.titleLabel.setText(
            t(self._lang, 'settings.section.theme'))
        self.app_group.titleLabel.setText(
            t(self._lang, 'settings.section.app'))
        self.actions_group.titleLabel.setText(
            t(self._lang, 'settings.section.actions'))
        self.program_section_title.setText(
            t(self._lang, 'settings.section.theme'))
        self.app_section_title.setText(t(self._lang, 'settings.section.app'))
        self.actions_section_title.setText(
            t(self._lang, 'settings.section.actions'))
        self.hotkeys_section_title.setText(
            t(self._lang, 'settings.section.hotkeys'))

        self.theme_card.titleLabel.setText(t(self._lang, 'settings.theme'))
        self.theme_card.contentLabel.setText(t(self._lang, 'settings.theme.desc'))
        self.theme_card.setThemeTexts(
            t(self._lang, 'settings.theme.auto'),
            t(self._lang, 'settings.theme.dark'),
            t(self._lang, 'settings.theme.light'),
        )

        self.language_card.titleLabel.setText(t(self._lang, 'settings.language'))
        self.language_card.contentLabel.setText(
            t(self._lang, 'settings.language.desc'))

        switches = [
            (self.follow_crosshair_switch, 'settings.accent.crosshair',
             'settings.accent.crosshair.desc'),
            (self.follow_windows_switch, 'settings.accent.windows',
             'settings.accent.windows.desc'),
            (self.mica_switch, 'settings.mica', 'settings.mica.desc'),
            (self.startup_switch, 'settings.startup', 'settings.startup.desc'),
        ]
        for switch, title_key, desc_key in switches:
            switch.titleLabel.setText(t(self._lang, title_key))
            switch.contentLabel.setText(t(self._lang, desc_key))

        self.actions_card.titleLabel.setText(t(self._lang, 'settings.actions'))
        self.actions_card.contentLabel.setText(
            t(self._lang, 'settings.actions.desc'))
        self.actions_card.save_btn.setText(t(self._lang, 'settings.save'))
        self.actions_card.reset_btn.setText(t(self._lang, 'settings.reset'))

        self.hotkeys_group.titleLabel.setText(
            t(self._lang, 'settings.section.hotkeys'))
        self.hotkeys_hint.setText(t(self._lang, 'hotkeys.tip'))
        self.reset_hotkeys_btn.setText(t(self._lang, 'hotkeys.reset_all'))
        for key, (title_key, desc_key) in self.hotkey_titles.items():
            card = self.hotkey_cards[key]
            card.titleLabel.setText(t(self._lang, title_key))
            card.contentLabel.setText(t(self._lang, desc_key))
