import sys
import pretty_errors
from loguru import logger
from PySide6.QtWidgets import QApplication
from postiny.mainwindow import MainWindow
from storage.habit import storage_init_habit

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
    storage_init_habit()
    
    app = QApplication()
    win = MainWindow()
    win.show()
    sys.exit(app.exec())

if '__main__' == __name__:
    main()
