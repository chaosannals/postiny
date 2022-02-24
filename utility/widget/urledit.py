from typing import Sequence
from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QWidget, QCompleter
from .urledit_ui import Ui_UrlEdit

class UrlEdit(QWidget):
    '''
    
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_UrlEdit()
        self.ui.setupUi(self)
        self.hostCompleter = QCompleter()
        self.ui.hostEdit.setCompleter(self.hostCompleter)
        self.pathCompleter = QCompleter()
        self.ui.pathEdit.setCompleter(self.pathCompleter)

    def protocol(self) -> str:
        return self.ui.protocolBox.currentText()

    def host(self)->str:
        return self.ui.hostEdit.text()

    def tipHosts(self, hosts: Sequence[str]):
        m = QStringListModel(hosts)
        self.hostCompleter.setModel(m)

    def tipPaths(self, paths: Sequence[str]):
        m = QStringListModel(paths)
        self.pathCompleter.setModel(m)