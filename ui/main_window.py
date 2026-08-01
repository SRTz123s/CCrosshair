"""Главное окно приложения в стиле WinUI 3 (FluentWindow, как Zapret2)."""

from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QColor, QIcon, QKeySequence
from qfluentwidgets import (FluentIcon, FluentWindow, InfoBar,
                            InfoBarPosition, NavigationItemPosition,
                            setThemeColor)

from config.settings_manager import SettingsManager
from core import windows_api
from core.crosshair_window import CrosshairWindow
from ui.app_icon import resolve_icon_path
from ui.i18n import t
from ui.pages.about_page import AboutPage
from ui.pages.crosshair_page import CrosshairPage
from ui.pages.profiles_page import ProfilesPage
from ui.pages.programs_page import ProgramsPage
from ui.pages.settings_page import SettingsPage
from ui.state import AppState
from ui.theme import apply_theme_mode

DEFAULT_ACCENT = '#0078D4'


class CrosshairFluentWindow(FluentWindow):
    """Главное окно с боковой навигацией и оверлеем прицела."""

    def __init__(self):
        super().__init__()
        self.settings = SettingsManager()
        self.state = AppState(self)
        self.crosshair = CrosshairWindow()
        self._current_theme_mode = 'system'
        self._applied_accent = None

        self.setWindowTitle('Custom Crosshair')
        self.resize(880, 640)
        self.setMinimumSize(720, 480)
        self._apply_app_icon()
        self._apply_mica()

        self._save_timer = QTimer(self)
        self._save_timer.setSingleShot(True)
        self._save_timer.setInterval(600)
        self._save_timer.timeout.connect(self.save_settings)

        self._load_settings()
        apply_theme_mode(self._current_theme_mode)

        self._build_pages()
        self._build_navigation()
        self._connect_state()
        self.apply_language(self.language())
        self._apply_accent()

        if self.state.program['show_on_startup']:
            self.state.set_enabled(True)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.check_active_windows)
        self.timer.start(100)

    # ------------------------------------------------------------ построение
    def _apply_app_icon(self):
        icon_path = resolve_icon_path()
        if not icon_path:
            return
        icon = QIcon(icon_path)
        self.setWindowIcon(icon)
        try:
            self.titleBar.setIcon(icon)
        except Exception:
            pass

    def _apply_mica(self):
        enabled = self.settings.load().get('mica', True)
        try:
            self.setMicaEffectEnabled(bool(enabled))
        except Exception:
            pass

    def _load_settings(self):
        data = self.settings.load()
        self._current_theme_mode = data.get('theme', 'system')
        self.state.set_params({
            'size': data['size'],
            'color': QColor(data['color']),
            'opacity': data['opacity'],
            'thickness': data['thickness'],
            'gap': data['gap'],
            'dot': data['dot'],
            'dot_size': data['dot_size'],
            'outline': data.get('outline', 0),
        })
        self.state.set_processes(data['selected_processes'])
        self.state.set_only_selected(True)
        self.state.set_program_many({
            'theme': self._current_theme_mode,
            'language': data.get('language', 'ru'),
            'follow_crosshair_accent': data.get('follow_crosshair_accent', True),
            'follow_windows_accent': data.get('follow_windows_accent', False),
            'show_on_startup': data.get('show_on_startup', False),
            'mica': data.get('mica', True),
        })
        self.state.set_hotkeys(data.get('hotkeys', {}))
        self.crosshair.update_crosshair(**self.state.render_params())

    def _build_pages(self):
        self.crosshair_page = CrosshairPage(self.state, self)
        self.settings_page = SettingsPage(self.state, self)
        self.profiles_page = ProfilesPage(self.state, self)
        self.programs_page = ProgramsPage(self.state, self)
        self.about_page = AboutPage(self)

    def _build_navigation(self):
        self._nav_items = {}
        self._nav_items['crosshair'] = self.addSubInterface(
            self.crosshair_page, FluentIcon.HOME,
            t(self.language(), 'nav.crosshair'))
        self._nav_items['profiles'] = self.addSubInterface(
            self.profiles_page, FluentIcon.TAG,
            t(self.language(), 'nav.profiles'),
            NavigationItemPosition.SCROLL)
        self._nav_items['programs'] = self.addSubInterface(
            self.programs_page, FluentIcon.GAME,
            t(self.language(), 'nav.programs'),
            NavigationItemPosition.SCROLL)
        self._nav_items['settings'] = self.addSubInterface(
            self.settings_page, FluentIcon.SETTING,
            t(self.language(), 'nav.settings'),
            NavigationItemPosition.BOTTOM)
        self._nav_items['about'] = self.addSubInterface(
            self.about_page, FluentIcon.INFO,
            t(self.language(), 'nav.about'),
            NavigationItemPosition.BOTTOM)

    def _connect_state(self):
        self.state.paramsChanged.connect(self._on_params_changed)
        self.state.enabledChanged.connect(self._on_enabled_changed)
        self.state.programChanged.connect(self._on_program_changed)
        self.settings_page.themeModeChanged.connect(self.apply_theme_mode)
        self.settings_page.languageChanged.connect(self.apply_language)
        self.settings_page.saveRequested.connect(self.save_settings)
        self.settings_page.resetRequested.connect(self.reset_settings)

        self.profiles_page.notify.connect(self._notify)
        self.profiles_page.importApplied.connect(self._on_import_applied)

        self.state.paramsChanged.connect(lambda _p: self._schedule_save())
        self.state.processesChanged.connect(lambda _t: self._schedule_save())
        self.state.onlySelectedChanged.connect(lambda _v: self._schedule_save())
        self.state.programChanged.connect(lambda _p: self._schedule_save())
        self.state.hotkeysChanged.connect(lambda _h: self._schedule_save())

    # -------------------------------------------------------------- события
    def _on_params_changed(self, params):
        self.crosshair.update_crosshair(**self.state.render_params())
        if self._accent_follows_crosshair():
            self._apply_accent()

    def _accent_follows_crosshair(self):
        return (not self.state.program['follow_windows_accent']
                and self.state.program['follow_crosshair_accent'])

    def _apply_accent(self):
        accent = None
        if self.state.program['follow_windows_accent']:
            accent = windows_api.get_windows_accent_color()
        if accent is None and self.state.program['follow_crosshair_accent']:
            accent = self.state.params['color'].name()
        if accent is None:
            accent = DEFAULT_ACCENT
        accent = accent.upper()
        if accent != self._applied_accent:
            self._applied_accent = accent
            setThemeColor(accent)

    def _on_program_changed(self, program):
        if program['theme'] != self._current_theme_mode:
            self._current_theme_mode = program['theme']
            apply_theme_mode(self._current_theme_mode)
        if program['language'] != self.language():
            self.apply_language(program['language'])
        self._apply_accent()
        try:
            self.setMicaEffectEnabled(bool(program['mica']))
        except Exception:
            pass

    def _on_import_applied(self):
        """После импорта настроек из JSON переприменяем интерфейс."""
        self.apply_language(self.language())
        self.settings_page.apply_state()
        self.programs_page.apply_state()
        self.crosshair_page.apply_state()
        self._apply_accent()

    def _on_enabled_changed(self, enabled):
        if enabled:
            self.crosshair.show_crosshair()
        else:
            self.crosshair.hide()

    def check_active_windows(self):
        """Скрывает прицел в невыбранных программах."""
        if not self.state.enabled or not self.state.only_selected:
            return
        active_title = windows_api.get_foreground_window_title()
        if not active_title:
            return
        if (self.state.selected_processes
                and active_title not in self.state.selected_processes):
            if self.crosshair.isVisible():
                self.crosshair.hide()
        else:
            if not self.crosshair.isVisible():
                self.crosshair.show_crosshair()

    # ---------------------------------------------------------- действия
    def language(self):
        return self.state.program.get('language', 'ru')

    def apply_language(self, language):
        language = language or 'ru'
        self.state.set_program('language', language)
        self._lang = language
        for key in ('crosshair', 'settings', 'programs', 'about'):
            self._nav_items[key].setText(t(language, f'nav.{key}'))
            self._nav_items[key].setToolTip(t(language, f'nav.{key}'))
        self.crosshair_page.apply_language(language)
        self.settings_page.apply_language(language)
        self.profiles_page.apply_language(language)
        self.programs_page.apply_language(language)
        self.about_page.apply_language(language)

    def apply_theme_mode(self, mode):
        self.state.set_program('theme', mode)

    def _schedule_save(self):
        timer = getattr(self, '_save_timer', None)
        if timer is not None:
            timer.start()

    def save_settings(self, silent=False):
        lang = self.language()
        data = {
            'size': self.state.params['size'],
            'color': self.state.params['color'].name(),
            'opacity': self.state.params['opacity'],
            'thickness': self.state.params['thickness'],
            'gap': self.state.params['gap'],
            'dot': self.state.params['dot'],
            'dot_size': self.state.params['dot_size'],
            'outline': self.state.params['outline'],
            'selected_processes': self.state.selected_processes,
            'theme': self._current_theme_mode,
            'language': lang,
            'follow_crosshair_accent': self.state.program['follow_crosshair_accent'],
            'follow_windows_accent': self.state.program['follow_windows_accent'],
            'show_on_startup': self.state.program['show_on_startup'],
            'mica': self.state.program['mica'],
            'hotkeys': dict(self.state.hotkeys),
        }
        try:
            self.settings.save(data)
        except Exception as exc:
            if not silent:
                self._notify(t(lang, 'notify.error'),
                             t(lang, 'notify.save_failed',
                               error=str(exc)), False)
            return
        if not silent:
            self._notify(t(lang, 'notify.saved'),
                         t(lang, 'notify.saved.desc'), True)

    def reset_settings(self):
        defaults = SettingsManager.reset()
        self.state.set_params({
            'size': defaults['size'],
            'color': QColor(defaults['color']),
            'opacity': defaults['opacity'],
            'thickness': defaults['thickness'],
            'gap': defaults['gap'],
            'dot': defaults['dot'],
            'dot_size': defaults['dot_size'],
            'outline': defaults['outline'],
        })
        self.state.set_processes(defaults['selected_processes'])
        self.state.set_only_selected(True)
        self.state.set_program_many({
            'theme': 'system',
            'language': 'ru',
            'follow_crosshair_accent': True,
            'follow_windows_accent': False,
            'show_on_startup': False,
            'mica': True,
        })
        self.state.set_hotkeys(SettingsManager.DEFAULTS.get('hotkeys', {}))
        self.crosshair_page.apply_state()
        self.settings_page.apply_state()
        self.programs_page.apply_state()
        self.apply_language(self.language())
        self._apply_mica()
        self._notify(t(self.language(), 'notify.reset'),
                     t(self.language(), 'notify.reset.desc'), True)

    def _notify(self, title, content, success=True):
        try:
            if success:
                InfoBar.success(title, content, parent=self,
                                position=InfoBarPosition.TOP_RIGHT,
                                duration=2500)
            else:
                InfoBar.error(title, content, parent=self,
                              position=InfoBarPosition.TOP_RIGHT,
                              duration=4000)
        except Exception:
            pass

    # -------------------------------------------------------------- события
    @staticmethod
    def _hotkey_matches(event, sequence):
        seq = QKeySequence(sequence)
        if seq.isEmpty():
            return False
        modifiers = (event.modifiers()
                     & ~Qt.KeyboardModifier.KeypadModifier)
        candidate = QKeySequence(int(modifiers.value) | int(event.key()))
        return candidate == seq

    def keyPressEvent(self, event):
        hotkeys = self.state.hotkeys
        if self._hotkey_matches(event, hotkeys.get('toggle')):
            self.state.set_enabled(not self.state.enabled)
        elif self._hotkey_matches(event, hotkeys.get('save')):
            self.save_settings()
        elif self._hotkey_matches(event, hotkeys.get('reset')):
            self.reset_settings()
        else:
            super().keyPressEvent(event)

    def closeEvent(self, event):
        self.timer.stop()
        self.save_settings(silent=True)
        self.crosshair.hide()
        super().closeEvent(event)
