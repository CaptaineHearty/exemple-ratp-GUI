from os import remove
from PySide2 import QtCore
from api_runable import ApiRunnable



class EtasModel(QtCore.QAbstractTableModel):
    def __init__(self, api, parent=None):
        super(EtasModel, self).__init__(parent)
        self.api = api
        self.tab = list()
        self.bus_code = ""
        self.station_code = ""
        self.api_data = list()

    def rowCount(self, parent=None):
        return len(self.tab)
    def columnCount(self, parent=None):
        return 2
    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid(): 
            return self.tab[index.row()][index.column()]
        return ""

    @QtCore.Slot()    
    def updateSyncImpl(self):        
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.rowCount()) # supression des données affichées
        self.tab.clear() # supression réel des données 
        self.endRemoveRows()
        self.beginInsertRows(QtCore.QModelIndex(), 0, len(self.api_data)-1)
        self.tab = self.api_data
        self.endInsertRows()

    def updateSync(self, bus_code, station_code):
        self.bus_code = bus_code
        self.station_code = station_code
        data_A = self.api.getEtas(self.bus_code, self.station_code, "A")
        data_R = self.api.getEtas(self.bus_code, self.station_code, "R")
        self.api_data = data_A + data_R
        QtCore.QMetaObject.invokeMethod(self, "updateSyncImpl")
        
    @QtCore.Slot(str, str)
    def update(self, bus_code, station_code):
        runnable = ApiRunnable(lambda: self.updateSync(bus_code, station_code))
        QtCore.QThreadPool.globalInstance().start(runnable)

