from PyQt5.QtCore import QObject, pyqtSignal, QThread
import random


class Device(QObject):
    updateNumber = pyqtSignal(tuple, name='updateNumber')
    connectedChanged = pyqtSignal(bool, name='connected')

    def run(self):
        while True:
            self.updateNumber.emit((random.randint(0, 4095), 100, 100, 100, 100, 100, 0))
            QThread.msleep(100)

    def is_connected(self):
        return True
