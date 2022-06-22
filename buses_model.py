from typing import Tuple
from PySide2 import QtCore
from filtered_list_model import FilteredListModel
from api_runable import ApiRunnable


class BusesModel(FilteredListModel):
    def __init__(self, api, parent=None):
        super(BusesModel, self).__init__(parent)
        self.api = api

    @QtCore.Slot(str)
    def fetch_buses(self, filter=""):
        runnable = ApiRunnable(lambda: self.update_data(self.api.getBuses(), filter))
        QtCore.QThreadPool.globalInstance().start(runnable)
