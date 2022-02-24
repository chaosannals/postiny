from PySide6.QtCore import QThreadPool, QRunnable

class TTask(QRunnable):
    '''
    
    '''
    
    def __init__(self, callback, data=None):
        '''
        '''

        super().__init__()
        self.callback = callback
        self.data = data

    def run(self):
        '''
        '''
        
        callback = self.callback
        callback(self.data)

    @classmethod
    def start(CLASS, callback, data=None):
        '''
        
        '''

        pool = QThreadPool.globalInstance()
        task = CLASS(callback, data)
        task.setAutoDelete(True)
        pool.start(task)