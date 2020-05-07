import sys
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon
from connect import Device


class MyApp(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Icon')
        self.setWindowIcon(QIcon('web.png'))
        self.setGeometry(300, 300, 300, 300)

        self.label = QLabel()
        self.label.setText("Hello")

        vbox = QVBoxLayout()
        vbox.addWidget(self.label)

        self.setLayout(vbox)
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    myapp = MyApp()
    thread = QThread()
    device = Device()
    device.moveToThread(thread)
    thread.started.connect(device.run)
    thread.start()
    device.updateNumber.connect(myapp.label.setText)
    sys.exit(app.exec_())
