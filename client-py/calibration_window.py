from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt


class CalibrationWindow(QWidget):
    calibrated = pyqtSignal(str, float, tuple, name="calibrated")

    def __init__(self, device):
        super().__init__()

        self.user_email = None
        self.score = None

        self.setWindowTitle("센서 조정")
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(300, 300, 560, 460)

        self.label = QLabel()
        self.label.setProperty("class", "big")
        self.label.setAlignment(Qt.AlignHCenter)

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.label)
        layout.addStretch(1)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)

        frame = QWidget()
        frame.setLayout(layout)
        frame.setProperty("class", "frame")

        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)
        self.setProperty("class", "root")
        self.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.device_changed(device.is_connected())
        device.connectedChanged.connect(self.device_changed)
        device.updateNumber.connect(self.sensor_update)

    def start(self, user_email, score):
        self.user_email = user_email
        self.score = score
        self.show()

    def device_changed(self, connected):
        if connected:
            self.label.setText("최초 1회 센서 값을 조정합니다.\n바른 자세를 취해주세요.")
        else:
            self.label.setText("최초 1회 센서 값을 조정합니다.\n장치를 연결해 주세요.")

    def finish(self, values):
        self.calibrated.emit(self.user_email, self.score, values)
        self.user_email = None
        self.score = None
        self.close()

    def sensor_update(self, values):
        if self.user_email is not None:
            self.finish(values)

    def logout(self):
        self.user_email = None
        self.close()

    def closeEvent(self, event):
        if self.user_email is not None:
            QCoreApplication.exit()
