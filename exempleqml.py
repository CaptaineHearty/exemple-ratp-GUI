
import sys

from PySide2.QtGui import QGuiApplication
from PySide2.QtQml import QQmlApplicationEngine
from buses_model import BusesModel
from stations_model import StationsModel
from etas_model import EtasModel
from api import ApiRatp
from pprint import pprint
import rc_icons

app = QGuiApplication(sys.argv)

engine = QQmlApplicationEngine()

myApi = ApiRatp(engine)

busesModel = BusesModel(myApi, engine)
busesModel.fetch_buses()

stationsModel = StationsModel(myApi, engine)

etasModel = EtasModel(myApi, engine)

print(sys.argv)

engine.rootContext().setContextProperty("busesModel", busesModel)
engine.rootContext().setContextProperty("stationsModel", stationsModel)
engine.rootContext().setContextProperty("etasModel", etasModel)
engine.rootContext().setContextProperty("myApi", myApi)

engine.quit.connect(app.quit)
engine.load('main.qml')


sys.exit(app.exec_())