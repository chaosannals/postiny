from PySide6.QtWidgets import QMainWindow
from PySide6.QtGui import QIcon
from .mainwindow_ui import Ui_MainWindow

class MainWindow(QMainWindow):
    '''
    主窗口
    '''

    def __init__(self, parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.setWindowIcon(QIcon(':/app.ico'))