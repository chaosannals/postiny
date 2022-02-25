from typing import Sequence
from urllib.parse import urlparse
from loguru import logger
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
        self.ui.urlClearButton.clicked.connect(self.onClickClearButthon)
        self.ui.partitionClearButton.clicked.connect(self.onClickClearButthon)
        self.ui.urlNextButton.clicked.connect(self.onClickNextButton)
        self.ui.partitionNextButton.clicked.connect(self.onClickNextButton)

        self.ui.urlEdit.textEdited.connect(self.onEditedUrlEdit)
        self.ui.protocolBox.currentIndexChanged.connect(self.onChangeProtocolBox)
        self.ui.hostEdit.textEdited.connect(self.onEditedHostEdit)
        self.ui.portBox.valueChanged.connect(self.onChangePortBox)
        self.ui.pathEdit.textEdited.connect(self.onEditedPathEdit)
        self.hostCompleter = QCompleter()
        self.ui.hostEdit.setCompleter(self.hostCompleter)
        self.pathCompleter = QCompleter()
        self.ui.pathEdit.setCompleter(self.pathCompleter)
        self.resizeByMode()

    @property
    def value(self) -> dict:
        r = self.partition
        r['url'] = self.url
        return r

    @property
    def partition(self) -> dict:
        return {
            'protocol': self.protocol,
            'host': self.host,
            'port': self.port,
            'path': self.path,
        }

    @property
    def url(self) -> str:
        return self.ui.urlEdit.text()

    @property
    def protocol(self) -> str:
        return self.ui.protocolBox.currentText()

    @property
    def host(self) -> str:
        return self.ui.hostEdit.text()

    @property
    def port(self):
        return self.ui.portBox.value()

    @property
    def path(self) -> str:
        return self.ui.pathEdit.text()

    def tipHosts(self, hosts: Sequence[str]):
        m = QStringListModel(hosts)
        self.hostCompleter.setModel(m)

    def tipPaths(self, paths: Sequence[str]):
        m = QStringListModel(paths)
        self.pathCompleter.setModel(m)

    def clear(self):
        self.ui.urlEdit.clear()
        self.clearPartition()

    def clearPartition(self):
        self.ui.hostEdit.clear()
        self.ui.portBox.clear()
        self.ui.pathEdit.clear()
        self.ui.queryTable.clear()

    def resizeByMode(self):
        n = self.ui.modeStack.currentIndex()
        if n == 1:
            h = self.ui.urlWidget.height()
            self.setMaximumHeight(h)
        else:
            self.setMaximumHeight(16777215)

    def updateUrl(self):
        '''
        
        '''
        port = '' if self.port is None else f':{self.port}'
        url = f'{self.protocol}://{self.host}{port}/{self.path}'
        self.ui.urlEdit.setText(url)

    def onClickClearButthon(self):
        self.clear()

    def onClickNextButton(self):
        i = self.ui.modeStack.currentIndex()
        c = self.ui.modeStack.count()
        self.ui.modeStack.setCurrentIndex((i + 1) % c)
        self.resizeByMode()

    def onEditedUrlEdit(self, text):
        '''

        '''

        try:
            pr = urlparse(text)
            logger.info('{}', pr)
            for i in range(self.ui.protocolBox.count()):
                t = self.ui.protocolBox.itemText(i)
                if t == pr.scheme:
                    self.ui.protocolBox.setCurrentIndex(i)
            self.ui.hostEdit.setText(pr.hostname)
            self.ui.portBox.setValue(pr.port)
            self.ui.pathEdit.setText(pr.path.strip('/'))
        except ValueError as e:
            self.clearPartition()

    def onChangeProtocolBox(self):
        '''
        
        '''

        self.updateUrl()

    def onEditedHostEdit(self, text):
        '''

        '''

        self.updateUrl()

    def onChangePortBox(self, text):
        '''

        '''

        self.updateUrl()


    def onEditedPathEdit(self, text):
        '''

        '''

        self.updateUrl()
