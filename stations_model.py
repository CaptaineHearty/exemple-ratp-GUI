from typing import Tuple
from PySide2 import QtCore
from filtered_list_model import FilteredListModel
from api_runable import ApiRunnable

class StationsModel(FilteredListModel):
    def __init__(self, api, parent=None):
        super(StationsModel, self).__init__(parent)
        self.api = api

    @QtCore.Slot(str)
    def fetch_stations(self, bus_code):
        runnable = ApiRunnable(lambda: self.update_data(self.api.getStations(bus_code)))
        QtCore.QThreadPool.globalInstance().start(runnable)
    
