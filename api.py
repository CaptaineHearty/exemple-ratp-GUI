import requests
from PySide2 import QtCore


class ApiRatp(QtCore.QObject):
    def getSpinBusy(self):
        return self.spin_busy_intern

    @QtCore.Signal
    def spinBusyChanged(self):
        pass

    spin_busy = QtCore.Property(type=bool, fget=getSpinBusy, notify=spinBusyChanged)

    def __init__(self, parent=None):
        super(ApiRatp, self).__init__(parent)
        self.headers = {
            "accept": "application/json",
        }
        self.url = "https://api-ratp.pierre-grimaud.fr/v4"
        self.nb_retry = 5
        self.spin_busy_intern = False

    def call(self, arg):
        return requests.get(f"{self.url}/{arg}", headers=self.headers).json()

    def getBuses(self):
        return self.call_with_retries(self.getBusesNoRetry)

    def getBusesNoRetry(self):
        try:
            r = self.call("lines/buses")["result"]
            if "buses" in r:
                return list(map(lambda r: (r["name"], r["code"]), r["buses"]))
            return None
        except requests.exceptions.ConnectionError:
            return [("Invalide, pas d'internet", -1)]

    def getStationsNoRetry(self, bus_code, way):
        try:
            r = self.call(f"stations/buses/{bus_code}?way={way}")["result"]
            if "stations" in r:
                return list(map(lambda r: (r["name"], r["slug"]), r["stations"]))
            return None
        except requests.exceptions.ConnectionError:
            return [("Invalide, pas d'internet", "")]

    def getStations(self, bus_code):
        stations_A = self.call_with_retries(self.getStationsNoRetry, bus_code, "A")
        stations_R = self.call_with_retries(self.getStationsNoRetry, bus_code, "R")
        if stations_A == None and stations_R == None:
            return [("J'ai essayer 5 fois chef ça marche pas", -1)]
        elif stations_A == None:
            return stations_R
        elif stations_R == None:
            return stations_A
        return list(set(stations_A + stations_R))

    def call_with_retries(self, func, *args):
        self.spin_busy_intern = True
        self.spinBusyChanged.emit()
        for x in range(self.nb_retry):
            ret = func(*args)
            if ret != None:
                self.spin_busy_intern = False
                self.spinBusyChanged.emit()
                return ret
        self.spin_busy_intern = False
        self.spinBusyChanged.emit()
        return [("J'ai essayer 5 fois chef ça marche pas", -1)]

    def getEtasNoRetry(self, bus_code, station_code, way):
        try:
            print(f"schedules/buses/{bus_code}/{station_code}/{way}")
            r = self.call(f"schedules/buses/{bus_code}/{station_code}/{way}")["result"]
            if "schedules" in r:
                return list(
                    map(lambda r: (r["message"], r["destination"]), r["schedules"])
                )
            return None
        except requests.exceptions.ConnectionError:
            return [("Invalide, pas d'internet", -1)]

    def getEtas(self, bus_code, station_code, way):
        return self.call_with_retries(self.getEtasNoRetry, bus_code, station_code, way)
