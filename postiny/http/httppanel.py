from datetime import datetime
from PySide6.QtWidgets import QWidget, QCompleter
from loguru import logger
from storage.habit.http import HabitRequestModel
from utility.ttask import TTask
from .httppanel_ui import Ui_HttpPanel

class HttpPanel(QWidget):
    '''
    
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_HttpPanel()
        self.ui.setupUi(self)
        self.ui.requestButton.clicked.connect(self.onClickRequestButton)

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

    def onClickAddressClearButton(self):
        '''
        
        '''

        self.ui.addressPathEdit.clear()

    def onClickRequestButton(self):
        '''
        
        '''

        m = HabitRequestModel()
        d = self.ui.urlEdit.partition
        m.url_protocol = d['protocol']
        m.url_host = d['host']
        m.url_port = d['port']
        m.url_path = d['path']
        TTask.start(self.request, m)

    def request(self, m: HabitRequestModel):
        '''
        
        '''

        m.create_at = datetime.now()
        m.save()
        port = '' if m.url_port is None else f':{m.url_port}'
        url = f'{m.url_protocol}://{m.url_host}{port}/{m.url_path}'
        logger.info('{}', url)

        