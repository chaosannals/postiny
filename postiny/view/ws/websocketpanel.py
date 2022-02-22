from PySide6.QtWidgets import QWidget
from .websocketpanel_ui import Ui_WebSocketPanel

class WebSocketPanel(QWidget):
    '''
    
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_WebSocketPanel()
        self.ui.setupUi(self)