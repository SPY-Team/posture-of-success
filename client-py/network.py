import requests
import json
from PyQt5.QtCore import pyqtSignal, QObject


class Network(QObject):
    response = pyqtSignal(dict, name="response")
    failure = pyqtSignal(str, name="failure")

    def request(self, data):
        print("request: ", data)
        faux = json.loads('{"result": "success"}')
        self.response.emit(faux)
