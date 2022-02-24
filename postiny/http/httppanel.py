from datetime import datetime
from PySide6.QtWidgets import QWidget
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
        self.ui.addressClearButton.clicked.connect(self.onClickAddressClearButton)
        self.ui.requestButton.clicked.connect(self.onClickRequestButton)

        hrm = HabitRequestModel.select().limit(100)
        hrs = hrm.dicts()
        logger.info(f'hrs: {hrs}')

    def onClickAddressClearButton(self):
        '''
        
        '''

        self.ui.addressPathEdit.clear()

    def onClickRequestButton(self):
        '''
        
        '''

        m = HabitRequestModel()
        m.url_protocol = self.ui.addressProtocolBox.currentText()
        m.url_host = self.ui.addressHostEdit.text()
        m.url_path = self.ui.addressPathEdit.text()

        TTask.start(self.request, m)

    def request(self, m: HabitRequestModel):
        '''
        
        '''

        m.create_at = datetime.now()
        m.save()
        logger.info(m)

        