"""Кодирование настроек прицела в компактный код и обратно.

Код позволяет делиться настройками прицела: скопировал код — вставил в
другой копии программы и применил. Формат:

    CH1:<base64url(json)>:<CRC32>

Также здесь собраны функции экспорта/импорта полных настроек программы
(прицел + настройки интерфейса + горячие клавиши + список программ) в JSON.
"""

import base64
import json
import zlib

from PyQt6.QtGui import QColor

PREFIX = 'CH1:'
PARAM_KEYS = ('size', 'color', 'opacity', 'thickness', 'gap',
              'dot', 'dot_size', 'outline')


def encode_crosshair(params):
    """Возвращает компактный код для параметров прицела."""
    data = {}
    for key in PARAM_KEYS:
        value = params.get(key)
        if key == 'color':
            value = QColor(value).name()
        data[key] = value
    payload = json.dumps(data, separators=(',', ':')).encode('utf-8')
    checksum = format(zlib.crc32(payload) & 0xFFFFFFFF, '08X')
    body = base64.urlsafe_b64encode(payload).decode('ascii')
    return f'{PREFIX}{body}:{checksum}'


def decode_crosshair(code):
    """Разбирает код прицела; возвращает dict параметров или None."""
    code = (code or '').strip()
    if not code.startswith(PREFIX):
        return None
    body, _, checksum = code[len(PREFIX):].rpartition(':')
    if not body or not checksum:
        return None
    try:
        payload = base64.urlsafe_b64decode(body.encode('ascii'))
    except Exception:
        return None
    if format(zlib.crc32(payload) & 0xFFFFFFFF, '08X') != checksum.upper():
        return None
    try:
        data = json.loads(payload.decode('utf-8'))
    except Exception:
        return None
    if not all(key in data for key in PARAM_KEYS):
        return None
    try:
        data['size'] = int(data['size'])
        data['opacity'] = int(data['opacity'])
        data['thickness'] = int(data['thickness'])
        data['gap'] = int(data['gap'])
        data['dot'] = bool(data['dot'])
        data['dot_size'] = int(data['dot_size'])
        data['outline'] = int(data['outline'])
        data['color'] = QColor(str(data['color']))
    except Exception:
        return None
    return data


def export_json(state):
    """Собирает все настройки программы в dict для сохранения в JSON."""
    params = dict(state.params)
    params['color'] = params['color'].name()
    return {
        'crosshair': params,
        'program': dict(state.program),
        'hotkeys': dict(state.hotkeys),
        'selected_processes': list(state.selected_processes),
        'only_selected': bool(state.only_selected),
    }


def import_json(data):
    """Возвращает (params, program, hotkeys, processes, only_selected)
    из загруженного JSON-словаря."""
    params = dict(data.get('crosshair', {}))
    if 'color' in params:
        params['color'] = QColor(str(params['color']))
    program = dict(data.get('program', {}))
    hotkeys = dict(data.get('hotkeys', {}))
    processes = list(data.get('selected_processes', []))
    only_selected = bool(data.get('only_selected', True))
    return params, program, hotkeys, processes, only_selected
