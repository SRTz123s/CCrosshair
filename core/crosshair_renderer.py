"""Единая отрисовка прицела для оверлея и предпросмотра."""

from PyQt6.QtCore import QPointF, Qt
from PyQt6.QtGui import QColor, QPainter, QPen

OUTLINE_COLOR = QColor('#000000')


def draw_crosshair(painter, center, size, color, opacity, gap, thickness,
                   dot, dot_size, outline=0):
    """Рисует прицел с заданными параметрами.

    Линии рисуются без сглаживания и точно по сетке пикселей, поэтому даже
    толщина в 1px выглядит тонкой, чёткой и полностью непрозрачной.

    Весь прицел жёстко привязан к центральной точке (cx, cy): точка рисуется
    ровно в (cx, cy), а плечи линий симметричны относительно неё и имеют
    одинаковую длину. Растеризатор Qt не рисует конечный пиксель линии
    (отрезок [x1, x2) покрывает пиксели x1..x2-1), поэтому правое и нижнее
    плечи рисуются от cx+gap+1 до cx+half+1 — так размах прицела становится
    нечётным и его оптический центр точно совпадает с точкой.

    center     — точка центра (QPoint / QPointF)
    size       — длина линии (полный размер)
    color      — QColor
    opacity    — прозрачность 0..1
    gap        — зазор от центра до начала линий
    thickness  — толщина линий
    dot        — рисовать ли центральную точку
    dot_size   — диаметр центральной точки
    outline    — толщина чёрной обводки линий и точки (0 — без обводки)
    """
    painter.setOpacity(opacity)
    painter.setRenderHint(QPainter.RenderHint.Antialiasing, False)

    outline = max(0, int(outline))
    half = size // 2
    cx = int(round(center.x()))
    cy = int(round(center.y()))

    def draw_lines(pen):
        painter.setPen(pen)
        painter.drawLine(QPointF(cx - half, cy), QPointF(cx - gap, cy))
        painter.drawLine(QPointF(cx + gap + 1, cy), QPointF(cx + half + 1, cy))
        painter.drawLine(QPointF(cx, cy - half), QPointF(cx, cy - gap))
        painter.drawLine(QPointF(cx, cy + gap + 1), QPointF(cx, cy + half + 1))

    if outline > 0:
        outline_pen = QPen(OUTLINE_COLOR, thickness + 2 * outline)
        outline_pen.setCapStyle(Qt.PenCapStyle.FlatCap)
        draw_lines(outline_pen)

    pen = QPen(color, thickness)
    pen.setCapStyle(Qt.PenCapStyle.FlatCap)
    draw_lines(pen)

    if dot:
        painter.setRenderHint(QPainter.RenderHint.Antialiasing, True)
        painter.setPen(Qt.PenStyle.NoPen)
        if outline > 0:
            radius = (dot_size + 2 * outline) / 2.0
            painter.setBrush(OUTLINE_COLOR)
            painter.drawEllipse(QPointF(cx, cy), radius, radius)
        painter.setBrush(color)
        painter.drawEllipse(QPointF(cx, cy), dot_size / 2.0, dot_size / 2.0)
