from random import randbytes
from loguru import logger
from PySide6.QtWidgets import QWidget, QPushButton
from .httprequestform_ui import Ui_HttpRequestForm
from storage.habit.http import HabitRequestModel

class HttpRequestForm(QWidget):
    '''
    HTTP 请求表单
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_HttpRequestForm()
        self.ui.setupUi(self)
        self.ui.headerAddButton.clicked.connect(self.onClickHeaderAddButton)

        hrm = HabitRequestModel.select().limit(100)
        hrs = hrm.dicts()
        hosts = set()
        paths = set()
        for hr in hrs:
            hosts.add(hr['url_host'])
            paths.add(hr['url_path'])
            logger.info(f'hr: {hr}')
        self.ui.urlEdit.tipHosts(hosts)
        self.ui.urlEdit.tipPaths(paths)

    @property
    def urlInfo(self):
        r = self.ui.urlEdit.value.copy()
        r['method'] = self.ui.methodBox.currentText()
        r['headers'] = self.headers.copy()
        return r

    @property
    def headers(self):
        '''
        
        '''
        ct = self.ui.contentTypeBox.currentText()
        if ct.startswith('multipart/form-data'):
            b = randbytes(32).hex()
            ct += f'; boundary={b}'

        r = {'Content-Type': ct }
        return r

    def addHeaderRow(self):
        '''
        添加单条报首项
        '''

        rc = self.ui.headersTable.rowCount()
        self.ui.headersTable.insertRow(rc)
        db = QPushButton()
        db.setText('删除')
        db.setStyleSheet('QPushButton { color: #f00; background: #fff; margin: 5px; border: 1px solid #f00 }')
        db.clicked.connect(lambda: self.onClickHeadersTableItemDeleteButton(db))
        self.ui.headersTable.setCellWidget(rc, 3, db)
        return rc

    def onClickHeaderAddButton(self):
        '''
        点击添加报首项按钮事件处理
        '''
        
        self.addHeaderRow()

    def onClickHeadersTableItemDeleteButton(self, db):
        '''
        点击删除报首项按钮事件处理
        '''
        
        for i in range(self.ui.headersTable.rowCount()):
            b = self.ui.headersTable.cellWidget(i, 2)
            if b == db:
                logger.info('删除第 {} 项请求报首', i + 1)
                self.ui.headersTable.removeRow(i)
                break