import sys
from loguru import logger
from PySide6.QtWidgets import QApplication
from postiny.view.mainwindow import MainWindow

@logger.catch
def main():
    '''
    
    '''

    logger.add(
        'logs/postiny.log',
        level='TRACE',
        rotation='2000 KB',
        retention='7 days',
        encoding='utf8'
    )
    app = QApplication()
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if '__main__' == __name__:
    main()
