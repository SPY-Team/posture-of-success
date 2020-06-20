import json

from PyQt5.QtCore import Qt, QSize, QUrl, QTimer, QEvent, QRect, pyqtSignal
from PyQt5.QtGui import QCloseEvent, QMouseEvent
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager
from PyQt5.QtWidgets import QWidget, QApplication, QStyle, QLabel, QVBoxLayout, \
    QDesktopWidget, QGraphicsOpacityEffect

from config import SERVER_BASE_ADDR
from graph_view import GraphView
from score import ScoreManager

WINDOWFLAGS = Qt.CustomizeWindowHint | \
              Qt.WindowStaysOnTopHint | \
              Qt.Tool | \
              Qt.FramelessWindowHint | \
              Qt.WindowDoesNotAcceptFocus | \
              Qt.X11BypassWindowManagerHint


class Detector(QWidget):
    enter = pyqtSignal(name="enter")

    def __init__(self):
        super().__init__()

        self.setWindowFlags(Qt.CustomizeWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.FramelessWindowHint |
            Qt.WindowDoesNotAcceptFocus |
            Qt.Tool |
            Qt.X11BypassWindowManagerHint)
        self.setProperty("class", "detector")
        self.setAttribute(Qt.WA_TranslucentBackground)

    def enterEvent(self, event: QEvent):
        self.enter.emit()


class PopupWindow(QWidget):
    def __init__(self, state, device):
        super().__init__()

        self.state = state
        self.close_requested = False
        self.score_manager = None
        self.device = device
        self.network = QNetworkAccessManager()
        self.minimize = False
        self.mouse_hover = False

        self.top = Detector()
        self.mid = Detector()
        self.bottom = Detector()
        self.top.enter.connect(self.leave)
        self.mid.enter.connect(self.leave)
        self.bottom.enter.connect(self.leave)

        self.last_score = None
        self.counter = 0

        # Setup UI
        self.setWindowFlags(WINDOWFLAGS)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.label = QLabel("...")

        self.graph_view = GraphView()

        self.layout = QVBoxLayout()
        # layout.addWidget(self.label)
        self.layout.addWidget(self.graph_view)

        self.update_size()

        self.frame = QWidget()
        self.frame.setLayout(self.layout)
        self.frame.setProperty("class", "overlay")

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.frame)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)
        self.setProperty("class", "root")
        self.setContentsMargins(0, 0, 0, 0)

        self.opacity = QGraphicsOpacityEffect()
        self.opacity.setOpacity(0.8)
        self.setGraphicsEffect(self.opacity)

        self.device.connectedChanged.connect(self.graph_view.connected_changed)
        self.device.updateNumber.connect(self.sensor_update)

        self.timer = QTimer()
        self.timer.setInterval(1000 / 30)
        self.timer.timeout.connect(self.graph_view.update_screen)
        self.timer.start()

    def update_size(self):
        if self.minimize:
            width, height = 120, 80
            self.layout.setContentsMargins(10, 10, 10, 10)
        else:
            width, height = 450, 300
            self.layout.setContentsMargins(20, 20, 20, 20)

        desktop: QDesktopWidget = QApplication.instance().desktop()
        desktop_rect = desktop.availableGeometry()
        popup_size = QSize(width, height)
        rect = QStyle.alignedRect(Qt.RightToLeft, Qt.AlignVCenter, popup_size, desktop_rect)
        self.setGeometry(rect)
        return desktop_rect, rect

    def start(self):
        print(self.state.sensor_values)
        self.score_manager = ScoreManager(self.state.score)
        self.graph_view.start(self.state.score)

        self.last_score = self.state.score
        self.counter = 0

        # Connect
        self.device.updateNumber.connect(self.score_manager.score_update)
        self.score_manager.updateScore.connect(self.score_update)

        self.show()

    def set_minimized(self, minimize):
        self.minimize = minimize
        self.update_size()
        self.graph_view.size_changed(minimize)
        if minimize:
            self.frame.setStyleSheet("border-radius: 10px;")
        else:
            self.frame.setStyleSheet("border-radius: 30px;")

    def score_update(self, score, msg, sitting_time):
        if not self.state.is_logged_in():
            return
        if msg == "바른 자세" and not self.mouse_hover:
            self.set_minimized(True)
        else:
            self.set_minimized(False)

        self.graph_view.update_score(score, msg, sitting_time, self.minimize)

        self.counter += 1
        if self.counter == 50:
            self.send_data(self.counter / 10, score - self.last_score)
            self.last_score = score
            self.counter = 0

    def sensor_update(self, score):
        self.label.setText(str(score))

    def send_data(self, duration, dscore):
        print("send data")
        data = {"email": self.state.user_email, "duration": duration, "dscore": dscore}
        req = QNetworkRequest(QUrl(SERVER_BASE_ADDR + "/api/device/update_score"))
        req.setRawHeader("Content-Type".encode('utf-8'), "application/json".encode('utf-8'))
        self.network.post(req, json.dumps(data).encode('utf-8'))

    def closeEvent(self, event: QCloseEvent):
        if not self.close_requested:
            event.ignore()
        self.close_requested = False

    def enterEvent(self, event: QEvent):
        if self.minimize:
            self.set_minimized(False)
        else:
            self.opacity.setOpacity(0.1)

        self.mouse_hover = True
        self.setWindowFlag(Qt.WindowTransparentForInput, True)
        self.show()

        desktop, rect = self.update_size()
        self.top.setGeometry(QRect(0, 0, desktop.width(), rect.top()))
        self.mid.setGeometry(QRect(0, rect.top(), rect.left(), rect.height()))
        self.bottom.setGeometry(QRect(0, rect.bottom(), desktop.width(), desktop.height() - rect.bottom()))
        self.top.show()
        self.mid.show()
        self.bottom.show()

    def leave(self):
        self.mouse_hover = False

        self.top.hide()
        self.mid.hide()
        self.bottom.hide()

        self.opacity.setOpacity(0.8)
        self.setWindowFlag(Qt.WindowTransparentForInput, False)
        self.show()

    def mousePressEvent(self, event: QMouseEvent):
        event.setAccepted(False)

    def logout(self):
        self.close_requested = True
        self.close()
