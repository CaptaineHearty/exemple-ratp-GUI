from re import S
from typing import Tuple
from PySide2 import QtCore
from pprint import pprint

class FilteredListModel(QtCore.QAbstractListModel):
    # Data =  [ (name1, id1), (name2, id2) ]
    NameRole = QtCore.Qt.UserRole + 1000
    IdRole = QtCore.Qt.UserRole + 1001

    def __init__(self, parent=None):
        super(FilteredListModel, self).__init__(parent)
        self.raw_data = list()
        self.filtered_data = list()
        self.previous_row_count = 0

    def rowCount(self, parent=None):
        return len(self.filtered_data)

    def get_filtered_data(self, filter_arg):
        return list(filter(lambda x: filter_arg in x[0], self.raw_data))

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if index.isValid():
            item = self.filtered_data[index.row()]
            if role == FilteredListModel.NameRole:
                return item[0]
            elif role == FilteredListModel.IdRole:
                return item[1]
        return ""
    
    def roleNames(self):
        return {FilteredListModel.NameRole:b"name", FilteredListModel.IdRole:b"id"}

    @QtCore.Slot()
    def update_data_impl(self): 
        self.beginRemoveRows(QtCore.QModelIndex(), 0, self.previous_row_count)
        self.endRemoveRows()
        self.beginInsertRows(QtCore.QModelIndex(), 0, self.rowCount()-1)
        self.endInsertRows()      
    
    def check_data(self, data):
        if isinstance(data, list):
            return all(map(self.check_row_valid, data))
        return False

    def check_row_valid(self, row):
        if isinstance(row, tuple) and len(row) >= 2:
            if isinstance(row[0], str) and isinstance(row[1], str):
                return True
        return False

    @QtCore.Slot(int, int, result=str)
    def get_elem_at(self, row, column):
        if row <= len(self.filtered_data) and row >= 0:
            if column <= len(self.filtered_data[row]) and column >= 0:
                return self.filtered_data[row][column]
        print(f"Error : row or column out of range, row = {row} and column = {column}")
        return ""

    @QtCore.Slot(list, str)
    def update_data(self, data, filter=""):
        if self.check_data(data):
            self.previous_row_count = self.rowCount()
            self.raw_data = data
            self.filtered_data.clear()
            self.filtered_data = self.get_filtered_data(filter)
            QtCore.QMetaObject.invokeMethod(self, "update_data_impl")
            
        else:
            print("API donnée invalide")
            pprint(data)

