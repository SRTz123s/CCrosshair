"""Страница «Прицел» — предпросмотр, статус и параметры прицела."""

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QHBoxLayout, QVBoxLayout

from qfluentwidgets import (CardWidget, FluentIcon, InfoBadge, InfoLevel,
                            PrimaryPushButton, SettingCardGroup,
                            SwitchSettingCard, StrongBodyLabel)

from ui.crosshair_preview import CrosshairPreview
from ui.i18n import t
from ui.pages.base_page import BasePage
from ui.widgets import ColorSettingCard, SliderSettingCard


class CrosshairPage(BasePage):
    """Главная страница: предпросмотр, переключатель и параметры прицела."""

    def __init__(self, state, parent=None):
        self.state = state
        super().__init__('crosshair.title', 'crosshair.subtitle', parent)
        self._lang = state.program.get('language', 'ru')
        self.setObjectName('crosshairPage')

        # ──────────────────────────────── предпросмотр
        self.add_section_title('crosshair.section.preview')
        preview_card = CardWidget(self.content)
        preview_layout = QVBoxLayout(preview_card)
        preview_layout.setContentsMargins(24, 20, 24, 20)
        self.preview = CrosshairPreview()
        self.preview.setFixedSize(240, 200)
        preview_layout.addWidget(self.preview, 0, Qt.AlignmentFlag.AlignCenter)
        self.add_widget(preview_card)
        self.add_spacing(8)

        # ──────────────────────────────── статус
        self.add_section_title('crosshair.section.status')
        self.status_card = CardWidget(self.content)
        self.status_card.setFixedHeight(116)
        status_layout = QVBoxLayout(self.status_card)
        status_layout.setContentsMargins(24, 14, 24, 14)
        status_layout.setSpacing(10)

        row = QHBoxLayout()
        self.status_title = StrongBodyLabel(t(self._lang, 'crosshair.status'))
        self.status_badge = InfoBadge(self, InfoLevel.WARNING)
        self.status_badge.setText(t(self._lang, 'crosshair.off'))
        row.addWidget(self.status_title)
        row.addStretch()
        row.addWidget(self.status_badge)
        status_layout.addLayout(row)

        self.toggle_btn = PrimaryPushButton('')
        self.toggle_btn.setFixedHeight(40)
        self.toggle_btn.setIcon(FluentIcon.PLAY)
        self.toggle_btn.clicked.connect(self.toggle_crosshair)
        status_layout.addWidget(self.toggle_btn)
        self.add_widget(self.status_card)
        self.add_spacing(8)

        # ──────────────────────────────── параметры
        self.add_section_title('crosshair.section.params')
        self.params_group = SettingCardGroup(
            t(self._lang, 'crosshair.section.params'), self.content)

        self.size_card = SliderSettingCard(
            FluentIcon.ZOOM_IN, t(self._lang, 'crosshair.param.size'),
            t(self._lang, 'crosshair.param.size.desc'), 10, 250,
            state.params['size'],
        )
        self.gap_card = SliderSettingCard(
            FluentIcon.RIGHT_ARROW, t(self._lang, 'crosshair.param.gap'),
            t(self._lang, 'crosshair.param.gap.desc'), 1, 40,
            state.params['gap'],
        )
        self.thickness_card = SliderSettingCard(
            FluentIcon.EDIT, t(self._lang, 'crosshair.param.thickness'),
            t(self._lang, 'crosshair.param.thickness.desc'), 1, 20,
            state.params['thickness'],
        )
        self.opacity_card = SliderSettingCard(
            FluentIcon.VIEW, t(self._lang, 'crosshair.param.opacity'),
            t(self._lang, 'crosshair.param.opacity.desc'), 10, 100,
            state.params['opacity'], suffix='%',
        )
        self.dot_size_card = SliderSettingCard(
            FluentIcon.PLAY_SOLID, t(self._lang, 'crosshair.param.dot_size'),
            t(self._lang, 'crosshair.param.dot_size.desc'), 1, 20,
            state.params['dot_size'],
        )
        self.outline_card = SliderSettingCard(
            FluentIcon.COPY, t(self._lang, 'crosshair.param.outline'),
            t(self._lang, 'crosshair.param.outline.desc'), 0, 10,
            state.params['outline'],
        )
        self.color_card = ColorSettingCard(
            FluentIcon.BRUSH, t(self._lang, 'crosshair.param.color'),
            t(self._lang, 'crosshair.param.color.desc'),
            state.params['color'],
        )
        self.dot_switch = SwitchSettingCard(
            FluentIcon.ACCEPT, t(self._lang, 'crosshair.param.dot'),
            t(self._lang, 'crosshair.param.dot.desc'),
        )
        self.dot_switch.setChecked(bool(state.params['dot']))

        for card in (self.size_card, self.gap_card, self.thickness_card,
                     self.opacity_card, self.dot_size_card,
                     self.outline_card, self.color_card, self.dot_switch):
            self.params_group.addSettingCard(card)
        self.add_widget(self.params_group)

        # связи
        self.size_card.valueChanged.connect(
            lambda v: self.state.set_param('size', v))
        self.gap_card.valueChanged.connect(
            lambda v: self.state.set_param('gap', v))
        self.thickness_card.valueChanged.connect(
            lambda v: self.state.set_param('thickness', v))
        self.opacity_card.valueChanged.connect(
            lambda v: self.state.set_param('opacity', v))
        self.dot_size_card.valueChanged.connect(
            lambda v: self.state.set_param('dot_size', v))
        self.outline_card.valueChanged.connect(
            lambda v: self.state.set_param('outline', v))
        self.dot_switch.checkedChanged.connect(
            lambda checked: self.state.set_param('dot', checked))
        self.color_card.colorChanged.connect(
            lambda color: self.state.set_color(color))

        self.state.paramsChanged.connect(self._on_params_changed)
        self.state.enabledChanged.connect(self._on_enabled_changed)
        self.state.hotkeysChanged.connect(self._on_hotkeys_changed)
        self._on_params_changed(dict(self.state.params))
        self._on_enabled_changed(self.state.enabled)

    # -------------------------------------------------------------- действия
    def toggle_crosshair(self):
        self.state.set_enabled(not self.state.enabled)

    def _toggle_text(self):
        base_key = ('crosshair.show' if not self.state.enabled
                    else 'crosshair.hide')
        hotkey = self.state.hotkeys.get('toggle', 'Ctrl+Shift+C')
        return f'{t(self._lang, base_key)}    ({hotkey})'

    def _on_hotkeys_changed(self, _hotkeys):
        self.toggle_btn.setText(self._toggle_text())

    def _on_params_changed(self, params):
        self.preview.set_params(
            size=params['size'],
            color=params['color'],
            opacity=params['opacity'] / 100.0,
            thickness=params['thickness'],
            gap=params['gap'],
            dot=params['dot'],
            dot_size=params['dot_size'],
            outline=params['outline'],
        )

    def _on_enabled_changed(self, enabled):
        if enabled:
            self.status_badge.setText(t(self._lang, 'crosshair.on'))
            self.status_badge.setLevel(InfoLevel.SUCCESS)
            self.toggle_btn.setIcon(FluentIcon.CANCEL)
        else:
            self.status_badge.setText(t(self._lang, 'crosshair.off'))
            self.status_badge.setLevel(InfoLevel.WARNING)
            self.toggle_btn.setIcon(FluentIcon.PLAY)
        self.toggle_btn.setText(self._toggle_text())

    def apply_state(self):
        """Синхронизирует виджеты с текущим состоянием (после сброса)."""
        p = self.state.params
        self.size_card.setValue(p['size'])
        self.gap_card.setValue(p['gap'])
        self.thickness_card.setValue(p['thickness'])
        self.opacity_card.setValue(p['opacity'])
        self.dot_size_card.setValue(p['dot_size'])
        self.outline_card.setValue(p['outline'])
        self.dot_switch.setChecked(bool(p['dot']))
        self.color_card.setColor(p['color'])

    def apply_language(self, language):
        super().apply_language(language)
        self._lang = language or 'ru'
        self.status_title.setText(t(self._lang, 'crosshair.status'))
        self.params_group.titleLabel.setText(
            t(self._lang, 'crosshair.section.params'))
        texts = [
            (self.size_card, 'crosshair.param.size',
             'crosshair.param.size.desc'),
            (self.gap_card, 'crosshair.param.gap',
             'crosshair.param.gap.desc'),
            (self.thickness_card, 'crosshair.param.thickness',
             'crosshair.param.thickness.desc'),
            (self.opacity_card, 'crosshair.param.opacity',
             'crosshair.param.opacity.desc'),
            (self.dot_size_card, 'crosshair.param.dot_size',
             'crosshair.param.dot_size.desc'),
            (self.outline_card, 'crosshair.param.outline',
             'crosshair.param.outline.desc'),
            (self.color_card, 'crosshair.param.color',
             'crosshair.param.color.desc'),
            (self.dot_switch, 'crosshair.param.dot',
             'crosshair.param.dot.desc'),
        ]
        for card, title_key, desc_key in texts:
            card.titleLabel.setText(t(self._lang, title_key))
            card.contentLabel.setText(t(self._lang, desc_key))
        self.color_card.apply_language(self._lang)
        self._on_enabled_changed(self.state.enabled)
