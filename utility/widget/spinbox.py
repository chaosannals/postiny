from PySide6.QtCore import Qt
from PySide6.QtWidgets import QSpinBox, QLineEdit, QAbstractSpinBox
from PySide6.QtGui import QShowEvent, QPaintEvent, QKeyEvent, QMouseEvent, QValidator

class SpinBox(QSpinBox):
    '''
    
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.isNull = True
        self.isNullable = True

    def value(self):
        return None if self.isNull else super().value()

    def setNull(self, v):
        self.isNull = v
        if v:
            e = self.findChild(QLineEdit, 'qt_spinbox_lineedit')
            if not (len(e.text()) == 0):
                e.clear()

    def setNullable(self, v):
        self.isNullable = v
        self.update()

    def setValue(self, v):
        if v is None:
            self.setNull(True)
        else:
            self.setNull(False)
            super().setValue(v)

    def showEvent(self, event: QShowEvent) -> None:
        super().showEvent(event)
        self.setNull(self.isNull)

    def paintEvent(self, event: QPaintEvent) -> None:
        self.setNull(self.isNull)
        super().paintEvent(event)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        k = event.key()

        if self.isNullable and k >= Qt.Key_0 and k <= Qt.Key_9 and self.isNull:
            self.setNull(False)

        if k == Qt.Key_Tab and self.isNullable and self.isNull:
            return QAbstractSpinBox.keyPressEvent(event)
        
        if k == Qt.Key_Backspace and self.isNullable:
            e = self.findChild(QLineEdit, 'qt_spinbox_lineedit')
            if e.selectedText() == e.text():
                self.setNull(True)
                return event.accept()

        return super().keyPressEvent(event)

    def mousePressEvent(self, event: QMouseEvent) -> None:
        super().mousePressEvent(event)
        if self.isNullable and self.isNull and self.calendarWidget().isVisible():
            self.setNull(True)

    def focusNextPrevChild(self, next: bool) -> bool:
        if self.isNullable and self.isNull:
            return QAbstractSpinBox.focusNextPrevChild(next)
        return super().focusNextPrevChild(next)

    def validate(self, input: str, pos: int) -> object:
        if self.isNullable and self.isNull:
            return QValidator.Acceptable
        return super().validate(input, pos)
