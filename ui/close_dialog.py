"""Диалог выбора «свернуть в трей / выйти» с крестиком-отменой."""

from PyQt6.QtCore import Qt, QEvent
from PyQt6.QtWidgets import QPushButton

from qfluentwidgets import MessageBox

class CloseChoiceDialog(MessageBox):
    """Три исхода: «Свернуть в трей», «Выйти» и отмена (крестик)."""

    MINIMIZE_RESULT = 1   # свернуть в трей
    QUIT_RESULT = 2       # полностью выйти
    DISMISS_RESULT = 0    # крестик / Esc / клик по фону — передумал

    def __init__(self, title, content, minimize_text, quit_text, parent=None):
        super().__init__(title, content, parent)
        self.yesButton.setText(minimize_text)
        self.cancelButton.setText(quit_text)

        # переподключаем кнопки на свои коды результата вместо accept/reject
        try:
            self.yesButton.clicked.disconnect()
        except Exception:
            pass
        try:
            self.cancelButton.clicked.disconnect()
        except Exception:
            pass
        self.yesButton.clicked.connect(lambda: self.done(MINIMIZE_RESULT))
        self.cancelButton.clicked.connect(lambda: self.done(QUIT_RESULT))

        # крестик-отмена в правом верхнем углу окна
        self.closeButton = QPushButton('✕', self.widget)
        self.closeButton.setObjectName('closeButton')
        self.closeButton.setFixedSize(28, 28)
        self.closeButton.setCursor(Qt.CursorShape.PointingHandCursor)
        self.closeButton.clicked.connect(lambda: self.done(DISMISS_RESULT))
        self.closeButton.setStyleSheet(
            'QPushButton{border:none;border-radius:4px;color:grey;'
            'background:transparent;}'
            'QPushButton:hover{background:rgba(0,0,0,0.08);color:black;}'
        )
        self._place_close_button()

        # клик по фону-маске тоже означает «передумал»
        self.setClosableOnMaskClicked(True)

    def _place_close_button(self):
        btn = getattr(self, 'closeButton', None)
        if btn is None:
            return
        x = self.widget.width() - self.closeButton.width() - 8
        y = 6
        self.closeButton.move(x, y)

    def _is_close_button_hit(self, pos):
        return getattr(self, 'closeButton', False) and \
            self.closeButton.geometry().contains(pos)

    def eventFilter(self, obj, e):
        if e.type() == QEvent.Type.MouseButtonRelease \
                and e.button() == Qt.MouseButton.LeftButton:
            if obj is self.widget and self._is_close_button_hit(e.pos()):
                self.done(DISMISS_RESULT)
                return True
        return super().eventFilter(obj, e)