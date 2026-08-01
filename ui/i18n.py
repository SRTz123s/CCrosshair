"""Интернационализация интерфейса (русский / английский)."""

DEFAULT_LANGUAGE = 'ru'

LANGUAGES = {
    'ru': 'Русский',
    'en': 'English',
}

STRINGS = {
    'ru': {
        'app.title': 'Custom Crosshair',

        'nav.crosshair': 'Прицел',
        'nav.settings': 'Настройки',
        'nav.programs': 'Программы',
        'nav.profiles': 'Профили',
        'nav.about': 'О программе',

        'crosshair.title': 'Прицел',
        'crosshair.subtitle': 'Настройте прицел: он отображается поверх '
                              'всех окон в центре экрана.',
        'crosshair.section.preview': 'Предпросмотр',
        'crosshair.section.status': 'Статус',
        'crosshair.status': 'Прицел',
        'crosshair.on': 'Включен',
        'crosshair.off': 'Выключен',
        'crosshair.show': 'Показать прицел',
        'crosshair.hide': 'Скрыть прицел',
        'crosshair.section.params': 'Параметры прицела',
        'crosshair.param.size': 'Размер',
        'crosshair.param.size.desc': 'Длина каждой линии прицела',
        'crosshair.param.gap': 'Зазор',
        'crosshair.param.gap.desc': 'Отступ линий от центра',
        'crosshair.param.thickness': 'Толщина',
        'crosshair.param.thickness.desc': 'Ширина линий прицела',
        'crosshair.param.opacity': 'Прозрачность',
        'crosshair.param.opacity.desc': 'Непрозрачность прицела',
        'crosshair.param.dot_size': 'Размер точки',
        'crosshair.param.dot_size.desc': 'Размер точки в центре',
        'crosshair.param.outline': 'Обводка',
        'crosshair.param.outline.desc': 'Толщина чёрной обводки линий и точки '
                                        '(0 — без обводки)',
        'crosshair.param.color': 'Цвет прицела',
        'crosshair.param.color.desc': 'Выберите цвет линий',
        'crosshair.param.dot': 'Точка в центре',
        'crosshair.param.dot.desc': 'Показывать точку в центре экрана',
        'crosshair.color.tooltip': 'Открыть палитру цветов',
        'crosshair.color.dialog': 'Выберите цвет прицела',

        'settings.title': 'Настройки',
        'settings.subtitle': 'Настройки интерфейса и поведения программы.',
        'settings.tab.program': 'Программа',
        'settings.tab.hotkeys': 'Горячие клавиши',
        'settings.section.theme': 'Тема',
        'settings.theme': 'Тема интерфейса',
        'settings.theme.desc': 'Автоматически или по выбору',
        'settings.theme.auto': 'Авто',
        'settings.theme.dark': 'Тёмная',
        'settings.theme.light': 'Светлая',
        'settings.section.app': 'Приложение',
        'settings.language': 'Язык',
        'settings.language.desc': 'Язык интерфейса',
        'settings.accent.crosshair': 'Цвет прицела как акцент',
        'settings.accent.crosshair.desc': 'Акцентный цвет интерфейса совпадает '
                                          'с цветом прицела',
        'settings.accent.windows': 'Акцент из Windows',
        'settings.accent.windows.desc': 'Использовать системный акцентный цвет '
                                        'Windows (приоритетнее цвета прицела)',
        'settings.mica': 'Эффект Mica',
        'settings.mica.desc': 'Полупрозрачный фон окна (Windows 11)',
        'settings.startup': 'Показывать прицел при запуске',
        'settings.startup.desc': 'Автоматически включать прицел при старте '
                                 'программы',
        'settings.section.hotkeys': 'Горячие клавиши',
        'settings.section.actions': 'Действия',
        'hotkeys.toggle': 'Показать / скрыть прицел',
        'hotkeys.toggle.desc': 'Быстрое включение и выключение прицела',
        'hotkeys.save': 'Сохранить настройки',
        'hotkeys.save.desc': 'Записать текущие настройки в файл',
        'hotkeys.reset': 'Сбросить настройки',
        'hotkeys.reset.desc': 'Вернуть настройки по умолчанию',
        'hotkeys.tip': 'Кликните по полю и нажмите нужное сочетание клавиш, '
                       'чтобы изменить горячую клавишу. Чтобы очистить поле, '
                       'нажмите Backspace.',
        'hotkeys.reset_all': 'Сбросить горячие клавиши',
        'settings.actions': 'Настройки',
        'settings.actions.desc': 'Сохранить изменения или вернуть значения '
                                 'по умолчанию',
        'settings.save': 'Сохранить',
        'settings.reset': 'Сбросить',

        'programs.title': 'Программы',
        'programs.subtitle': 'Показывайте прицел только в выбранных '
                             'приложениях.',
        'programs.section.mode': 'Режим отображения',
        'programs.only_selected': 'Только в выбранных программах',
        'programs.only_selected.desc': 'Прицел будет виден лишь в активных '
                                       'окнах из списка ниже. Если список '
                                       'пуст — прицел показывается во всех '
                                       'окнах.',
        'programs.section.list': 'Программы',
        'programs.hint': 'Отметьте программы, в которых будет виден прицел',
        'programs.refresh': 'Обновить список',
        'programs.clear': 'Очистить выбор',

        'profiles.title': 'Профили',
        'profiles.subtitle': 'Сохраняйте настройки прицела в виде кода и '
                             'обменивайтесь ими, а также экспортируйте все '
                             'настройки программы в JSON-файл.',
        'profiles.section.crosshair': 'Прицел',
        'profiles.copy': 'Код прицела',
        'profiles.copy.desc': 'Скопируйте код, чтобы перенести настройки '
                              'прицела на другой компьютер',
        'profiles.copy.btn': 'Скопировать код',
        'profiles.apply': 'Импорт по коду',
        'profiles.apply.desc': 'Вставьте код прицела и примените его',
        'profiles.apply.btn': 'Применить код',
        'profiles.apply.placeholder': 'Вставьте код прицела…',
        'profiles.section.program': 'Настройки программы',
        'profiles.export': 'Экспорт в JSON',
        'profiles.export.desc': 'Сохранить все настройки программы в '
                                'JSON-файл',
        'profiles.export.btn': 'Экспорт…',
        'profiles.export.title': 'Сохранить настройки',
        'profiles.export.failed': 'Не удалось сохранить файл',
        'profiles.exported': 'Настройки экспортированы',
        'profiles.import': 'Импорт из JSON',
        'profiles.import.desc': 'Загрузить настройки программы из '
                                'JSON-файла',
        'profiles.import.btn': 'Импорт…',
        'profiles.import.title': 'Открыть настройки',
        'profiles.import.failed': 'Не удалось прочитать файл',
        'profiles.imported': 'Настройки импортированы',
        'profiles.copied': 'Код скопирован',
        'profiles.copied.desc': 'Код прицела скопирован в буфер обмена',
        'profiles.invalid': 'Некорректный код',
        'profiles.invalid.desc': 'Не удалось распознать код прицела',
        'profiles.applied': 'Код применён',
        'profiles.applied.desc': 'Параметры прицела загружены из кода',

        'about.title': 'О программе',
        'about.subtitle': 'Custom Crosshair — настраиваемый прицел поверх '
                          'всех окон.',
        'about.section.app': 'Приложение',
        'about.version': 'Версия 1.0.0',
        'about.desc': 'Приложение рисует прицел в центре экрана поверх всех '
                      'окон. Параметры настраиваются на странице «Прицел», '
                      'тему интерфейса — на странице «Настройки», а показ '
                      'можно ограничить выбранными программами.',

        'notify.saved': 'Сохранено',
        'notify.saved.desc': 'Настройки сохранены',
        'notify.error': 'Ошибка',
        'notify.save_failed': 'Не удалось сохранить настройки: {error}',
        'notify.reset': 'Сброшено',
        'notify.reset.desc': 'Настройки возвращены к значениям по умолчанию',
    },
    'en': {
        'app.title': 'Custom Crosshair',

        'nav.crosshair': 'Crosshair',
        'nav.settings': 'Settings',
        'nav.programs': 'Programs',
        'nav.profiles': 'Profiles',
        'nav.about': 'About',

        'crosshair.title': 'Crosshair',
        'crosshair.subtitle': 'Configure the crosshair: it is displayed '
                              'above all windows in the center of the screen.',
        'crosshair.section.preview': 'Preview',
        'crosshair.section.status': 'Status',
        'crosshair.status': 'Crosshair',
        'crosshair.on': 'On',
        'crosshair.off': 'Off',
        'crosshair.show': 'Show crosshair',
        'crosshair.hide': 'Hide crosshair',
        'crosshair.section.params': 'Crosshair settings',
        'crosshair.param.size': 'Size',
        'crosshair.param.size.desc': 'Length of each crosshair line',
        'crosshair.param.gap': 'Gap',
        'crosshair.param.gap.desc': 'Offset of lines from the center',
        'crosshair.param.thickness': 'Thickness',
        'crosshair.param.thickness.desc': 'Width of crosshair lines',
        'crosshair.param.opacity': 'Opacity',
        'crosshair.param.opacity.desc': 'Opacity of the crosshair',
        'crosshair.param.dot_size': 'Dot size',
        'crosshair.param.dot_size.desc': 'Size of the center dot',
        'crosshair.param.outline': 'Outline',
        'crosshair.param.outline.desc': 'Thickness of the black outline around '
                                        'lines and dot (0 — no outline)',
        'crosshair.param.color': 'Crosshair color',
        'crosshair.param.color.desc': 'Choose the line color',
        'crosshair.param.dot': 'Center dot',
        'crosshair.param.dot.desc': 'Show a dot in the center of the screen',
        'crosshair.color.tooltip': 'Open color palette',
        'crosshair.color.dialog': 'Choose crosshair color',

        'settings.title': 'Settings',
        'settings.subtitle': 'Interface and program behavior settings.',
        'settings.tab.program': 'Program',
        'settings.tab.hotkeys': 'Hotkeys',
        'settings.section.theme': 'Theme',
        'settings.theme': 'Interface theme',
        'settings.theme.desc': 'Automatically or by choice',
        'settings.theme.auto': 'Auto',
        'settings.theme.dark': 'Dark',
        'settings.theme.light': 'Light',
        'settings.section.app': 'Application',
        'settings.language': 'Language',
        'settings.language.desc': 'Interface language',
        'settings.accent.crosshair': 'Crosshair color as accent',
        'settings.accent.crosshair.desc': 'The interface accent color matches '
                                          'the crosshair color',
        'settings.accent.windows': 'Accent from Windows',
        'settings.accent.windows.desc': 'Use the Windows system accent color '
                                        '(takes priority over the crosshair '
                                        'color)',
        'settings.mica': 'Mica effect',
        'settings.mica.desc': 'Semi-transparent window background (Windows 11)',
        'settings.startup': 'Show crosshair on startup',
        'settings.startup.desc': 'Automatically enable the crosshair when '
                                 'the program starts',
        'settings.section.hotkeys': 'Hotkeys',
        'settings.section.actions': 'Actions',
        'hotkeys.toggle': 'Show / hide crosshair',
        'hotkeys.toggle.desc': 'Quickly enable and disable the crosshair',
        'hotkeys.save': 'Save settings',
        'hotkeys.save.desc': 'Write current settings to a file',
        'hotkeys.reset': 'Reset settings',
        'hotkeys.reset.desc': 'Restore default settings',
        'hotkeys.tip': 'Click the field and press the desired key '
                       'combination to change the hotkey. To clear the '
                       'field, press Backspace.',
        'hotkeys.reset_all': 'Reset hotkeys',
        'settings.actions': 'Settings',
        'settings.actions.desc': 'Save changes or restore default values',
        'settings.save': 'Save',
        'settings.reset': 'Reset',

        'programs.title': 'Programs',
        'programs.subtitle': 'Show the crosshair only in selected '
                             'applications.',
        'programs.section.mode': 'Display mode',
        'programs.only_selected': 'Only in selected programs',
        'programs.only_selected.desc': 'The crosshair is visible only in the '
                                       'active windows from the list below. '
                                       'If the list is empty, the crosshair '
                                       'is shown in all windows.',
        'programs.section.list': 'Programs',
        'programs.hint': 'Mark the programs where the crosshair is visible',
        'programs.refresh': 'Refresh list',
        'programs.clear': 'Clear selection',

        'profiles.title': 'Profiles',
        'profiles.subtitle': 'Save crosshair settings as a code and share '
                             'them, or export all program settings to a '
                             'JSON file.',
        'profiles.section.crosshair': 'Crosshair',
        'profiles.copy': 'Crosshair code',
        'profiles.copy.desc': 'Copy the code to transfer crosshair settings '
                              'to another computer',
        'profiles.copy.btn': 'Copy code',
        'profiles.apply': 'Import by code',
        'profiles.apply.desc': 'Paste the crosshair code and apply it',
        'profiles.apply.btn': 'Apply code',
        'profiles.apply.placeholder': 'Paste the crosshair code…',
        'profiles.section.program': 'Program settings',
        'profiles.export': 'Export to JSON',
        'profiles.export.desc': 'Save all program settings to a JSON file',
        'profiles.export.btn': 'Export…',
        'profiles.export.title': 'Save settings',
        'profiles.export.failed': 'Failed to save file',
        'profiles.exported': 'Settings exported',
        'profiles.import': 'Import from JSON',
        'profiles.import.desc': 'Load program settings from a JSON file',
        'profiles.import.btn': 'Import…',
        'profiles.import.title': 'Open settings',
        'profiles.import.failed': 'Failed to read file',
        'profiles.imported': 'Settings imported',
        'profiles.copied': 'Code copied',
        'profiles.copied.desc': 'Crosshair code copied to clipboard',
        'profiles.invalid': 'Invalid code',
        'profiles.invalid.desc': 'Could not recognize the crosshair code',
        'profiles.applied': 'Code applied',
        'profiles.applied.desc': 'Crosshair settings loaded from the code',

        'about.title': 'About',
        'about.subtitle': 'Custom Crosshair — a customizable crosshair above '
                          'all windows.',
        'about.section.app': 'Application',
        'about.version': 'Version 1.0.0',
        'about.desc': 'The application draws a crosshair in the center of the '
                      'screen above all windows. Parameters are configured on '
                      'the "Crosshair" page, the interface theme on the '
                      '"Settings" page, and display can be limited to '
                      'selected programs.',

        'notify.saved': 'Saved',
        'notify.saved.desc': 'Settings saved',
        'notify.error': 'Error',
        'notify.save_failed': 'Failed to save settings: {error}',
        'notify.reset': 'Reset',
        'notify.reset.desc': 'Settings restored to default values',
    },
}


def t(language, key, **kwargs):
    """Возвращает переведённую строку по ключу."""
    table = STRINGS.get(language) or STRINGS.get(DEFAULT_LANGUAGE, {})
    fallback = STRINGS.get(DEFAULT_LANGUAGE, {}).get(key, key)
    text = table.get(key, fallback)
    if kwargs:
        try:
            text = text.format(**kwargs)
        except Exception:
            pass
    return text
