from PySide2 import QtCore

class ApiRunnable(QtCore.QRunnable):
    def __init__(self, func, *args):
        super(ApiRunnable, self).__init__()
        self.args = args
        self.func = func
    
    def run(self):        
        self.func(*self.args)