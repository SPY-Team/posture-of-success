from PyQt5.QtCore import QObject, pyqtSignal, QThread


class Device(QObject):
    updateNumber = pyqtSignal(tuple, name='updateNumber')
    connectedChanged = pyqtSignal(bool, name='connected')

    def run(self):
        while True:
            self.updateNumber.emit((100, 100, 100, 100, 100, 100))
            QThread.msleep(100)

    def is_connected(self):
        return True
