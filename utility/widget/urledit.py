from typing import Sequence
from urllib.parse import urlparse
from loguru import logger
from PySide6.QtCore import QStringListModel
from PySide6.QtWidgets import QWidget, QCompleter, QTableWidgetItem, QPushButton
from .urledit_ui import Ui_UrlEdit


class UrlEdit(QWidget):
    '''

    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.result_url = None
        self.result_partition = {}
        self.ui = Ui_UrlEdit()
        self.ui.setupUi(self)
        self.ui.urlClearButton.clicked.connect(self.onClickClearButthon)
        self.ui.partitionClearButton.clicked.connect(self.onClickClearButthon)
        self.ui.urlNextButton.clicked.connect(self.onClickNextButton)
        self.ui.partitionNextButton.clicked.connect(self.onClickNextButton)

        self.ui.queryAddButton.clicked.connect(self.onClickQueryAddButton)
        self.hostCompleter = QCompleter()
        self.ui.hostEdit.setCompleter(self.hostCompleter)
        self.pathCompleter = QCompleter()
        self.ui.pathEdit.setCompleter(self.pathCompleter)
        self.onModeSwitch()

    @property
    def value(self) -> dict:
        r = self.partition.copy()
        r['url'] = self.url
        return r

    @property
    def partition(self) -> dict:
        return self.result_partition

    @property
    def url(self) -> str:
        return self.result_url

    @property
    def protocol(self) -> str:
        return self.result_partition.get('protocol', 'http')

    @property
    def host(self):
        return self.result_partition.get('host')

    @property
    def port(self):
        return self.result_partition.get('port')

    @property
    def path(self) -> str:
        return self.result_partition.get('path')

    @property
    def query_string(self) -> str:
        return self.result_partition.get('query')

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
        self.ui.queryTable.clearContents()
        self.ui.queryTable.setRowCount(0)
        self.ui.hashEdit.clear()

    def onModeSwitch(self):
        n = self.ui.modeStack.currentIndex()
        if n == 1:
            h = self.ui.urlWidget.height()
            self.composeUrl()
            self.setMaximumHeight(h)
        else:
            self.analyseUrl()
            self.setMaximumHeight(16777215)

    def addQueryRow(self):
        rc = self.ui.queryTable.rowCount()
        self.ui.queryTable.insertRow(rc)
        db = QPushButton()
        db.setText('??????')
        db.setStyleSheet('QPushButton { color: #f00; background: #fff; margin: 5px; border: 1px solid #f00 }')
        db.clicked.connect(lambda: self.onClickQueryTableItemDeleteButton(db))
        self.ui.queryTable.setCellWidget(rc, 3, db)
        return rc

    def composeUrl(self):
        '''
        ?????? URL ?????????????????????
        '''

        has_host = self.host is None or len(self.host) == 0
        host = '' if has_host else self.host
        port = '' if self.port is None or has_host else f':{self.port}'
        path = '' if self.path is None or len(self.path) == 0 else f'/{self.path}'
        url = f'{self.protocol}://{host}{port}{path}'

        # ????????????
        query = []
        for i in range(self.ui.queryTable.rowCount()):
            ki = self.ui.queryTable.item(i, 0)
            k = ki.text().strip()
            if len(k) > 0:
                vi = self.ui.queryTable.item(i, 1)
                v = '' if vi is None else vi.text().strip()
                query.append(f'{k}={v}')
        query_string = '&'.join(query)
        if len(query) > 0:
            url = f'{url}?{query_string}'

        # ?????? hash
        h = self.ui.hashEdit.text().strip()
        if len(h) > 0:
            url = f'{url}#{h}'
        
        self.ui.urlEdit.setText(url)

        self.result_url = self.ui.urlEdit.text()
        self.result_partition = {
            'protocol': self.ui.protocolBox.currentText(),
            'host': self.ui.hostEdit.text(),
            'port': self.ui.portBox.value(),
            'path': self.ui.pathEdit.text(),
            'query': query_string,
            'hash': h,
        }

    def analyseUrl(self):
        '''
        ?????? URL ??????????????????
        '''

        try:
            pr = urlparse(self.ui.urlEdit.text())
            logger.info('{}', pr)
            for i in range(self.ui.protocolBox.count()):
                t = self.ui.protocolBox.itemText(i)
                if t == pr.scheme:
                    self.ui.protocolBox.setCurrentIndex(i)
            self.ui.hostEdit.setText(pr.hostname)
            self.ui.portBox.setValue(pr.port)
            self.ui.pathEdit.setText(pr.path.strip('/'))
            # ????????????
            self.ui.queryTable.clearContents()
            self.ui.queryTable.setRowCount(0)
            for q in pr.query.split('&'):
                k, v = q.split('=', 2)
                r = self.addQueryRow()
                qki = QTableWidgetItem()
                qki.setText(k)
                self.ui.queryTable.setItem(r, 0, qki)
                qvi = QTableWidgetItem()
                qvi.setText(v)
                self.ui.queryTable.setItem(r, 1, qvi)
            self.ui.hashEdit.setText(pr.fragment)

            self.result_url = self.ui.urlEdit.text()
            self.result_partition = {
                'protocol': pr.scheme,
                'host': self.ui.hostEdit.text(),
                'port': self.ui.portBox.value(),
                'path': self.ui.pathEdit.text(),
                'query': pr.query,
                'hash': self.ui.hashEdit.text(),
            }
        except ValueError as e:
            self.clearPartition()

    def onClickClearButthon(self):
        self.clear()

    def onClickNextButton(self):
        i = self.ui.modeStack.currentIndex()
        c = self.ui.modeStack.count()
        self.ui.modeStack.setCurrentIndex((i + 1) % c)
        self.onModeSwitch()

    def onClickQueryAddButton(self):
        '''
        
        '''

        self.addQueryRow()

    def onClickQueryTableItemDeleteButton(self, db):
        for i in range(self.ui.queryTable.rowCount()):
            b = self.ui.queryTable.cellWidget(i, 2)
            if b == db:
                logger.info('????????? {} ???????????????', i + 1)
                self.ui.queryTable.removeRow(i)
                break