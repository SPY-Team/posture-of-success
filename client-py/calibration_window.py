from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsView, QGraphicsScene
from PyQt5.QtGui import QIcon, QMovie, QPixmap
from PyQt5.QtCore import pyqtSignal, QCoreApplication, Qt, QUrl
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
from config import SERVER_BASE_ADDR
import json


def detect(values):
    lhip, lthigh, lback, rhip, rthigh, rback, dist = values
    thigh_imbalance = (lthigh - rthigh) / (lthigh + rthigh + 1)
    if sum(values[:6]) == 0:
        return False, "의자에 앉아 주세요."
    elif thigh_imbalance > 0.5:
        return False, "허벅지 왼쪽으로 쏠림"
    elif thigh_imbalance < -0.5:
        return False, "허벅지 오른쪽으로 쏠림"
    elif lhip == 0 and rhip == 0:
        return False, "엉덩이를 당겨 앉아 주세요."
    elif dist == -1:
        return False, "너무 뒤로 기대지 말아주세요."
    elif lback == 0 and rback == 0:
        return False, "허리를 등받이에 밀착해 주세요."
    else:
        return True, "바른 자세"


class CalibrationWindow(QWidget):
    calibrated = pyqtSignal(str, float, tuple, name="calibrated")

    def __init__(self, device):
        super().__init__()

        self.cnt = 0
        self.user_email = None
        self.score = None
        self.values = (0, 0, 0, 0, 0, 0, 0)

        self.network = QNetworkAccessManager()
        chair = QGraphicsView()
        scene = QGraphicsScene()
        scene.addPixmap(QPixmap("chair.png"))
        chair.setScene(scene)
        chair.setFixedWidth(150)
        chair.setFixedHeight(300)

        self.setWindowTitle("센서 조정")
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(300, 300, 560, 460)

        self.label = QLabel()
        self.label.setProperty("class", "big")
        self.label.setAlignment(Qt.AlignHCenter)

        movie = QMovie("loader.gif")
        movie.start()
        busy_label = QLabel()
        busy_label.setMovie(movie)
        busy_label.setAlignment(Qt.AlignHCenter)

        layout = QVBoxLayout()
        layout.addStretch(1)
        layout.addWidget(self.label)
        layout.addWidget(chair)
        layout.addWidget(busy_label)
        layout.addStretch(1)
        layout.setContentsMargins(50, 50, 50, 50)
        layout.setSpacing(20)
        layout.setAlignment(Qt.AlignHCenter)

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
        self.cnt = 0
        self.values = (0, 0, 0, 0, 0, 0, 0)
        self.show()

    def device_changed(self, connected):
        if connected:
            self.label.setText("최초 1회 센서 값을 조정합니다.\n바른 자세를 취해주세요.")
        else:
            self.label.setText("최초 1회 센서 값을 조정합니다.\n장치를 연결해 주세요.")

    def finish(self, values):
        data = {"email": self.user_email,
                "sensor_data": str(values)}

        req = QNetworkRequest(QUrl(SERVER_BASE_ADDR + "/api/device/update_sensor_data"))
        req.setRawHeader("Content-Type".encode('utf-8'), "application/json".encode('utf-8'))
        self.network.post(req, json.dumps(data).encode('utf-8'))

        self.calibrated.emit(self.user_email, self.score, values)
        self.user_email = None
        self.score = None
        self.close()

    def sensor_update(self, values):
        if self.user_email is None:
            return
        correct_posture, msg = detect(values)
        if correct_posture:
            self.cnt += 1
            self.values = tuple(sum(x) for x in zip(values, self.values))
            msg = "이 자세를 {:.1f}초간 유지해주세요.".format((50 - self.cnt) / 10)
        else:
            self.cnt = 0
            self.values = (0, 0, 0, 0, 0, 0, 0)
        self.label.setText("최초 1회 센서 값을 조정합니다.\n바른 자세를 취해주세요.\n" + msg)

        if self.cnt >= 50:
            values = tuple(v / self.cnt for v in self.values)
            self.finish(values)

    def logout(self):
        self.user_email = None
        self.close()

    def closeEvent(self, event):
        if self.user_email is not None:
            QCoreApplication.exit()
