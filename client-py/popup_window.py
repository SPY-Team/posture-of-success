from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QApplication, QStyle, QLabel, QVBoxLayout, \
    QDesktopWidget, QGraphicsOpacityEffect
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor, QPainter, QFont, QTextDocument, QTextCharFormat, QTextCursor, \
    QCloseEvent, QLinearGradient, QPainterPath, QMouseEvent
from PyQt5.QtCore import Qt, QSize, QPointF, QUrl, QTimer, QEvent, QRect, pyqtSignal
from score import ScoreManager
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager
from config import SERVER_BASE_ADDR
import json

WINDOWFLAGS = Qt.CustomizeWindowHint | \
              Qt.WindowStaysOnTopHint | \
              Qt.Tool | \
              Qt.FramelessWindowHint | \
              Qt.WindowDoesNotAcceptFocus | \
              Qt.X11BypassWindowManagerHint


def make_text(text, size):
    document = QTextDocument()
    fmt = QTextCharFormat()
    font: QFont = QApplication.instance().font()
    font.setPixelSize(size)
    fmt.setFont(font)
    cursor = QTextCursor(document)
    cursor.insertText(text, fmt)
    return document


class GraphView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setScene(QGraphicsScene())
        self.setBackgroundBrush(Qt.transparent)
        self.setRenderHint(QPainter.Antialiasing)

        self.graph = self.scene().addPolygon(QPolygonF(), QPen(Qt.transparent), QBrush())

        color = QColor.fromRgb(0x35, 0x37, 0x72)
        pen = QPen(color, 3)
        pen.setCapStyle(Qt.RoundCap)
        self.path = self.scene().addPath(QPainterPath(), pen)

        self.score_text = self.scene().addText("")
        self.score_text.setDefaultTextColor(color)

        self.msg_text = self.scene().addText("")
        self.msg_text.setDefaultTextColor(color)
        self.msg_text.setX(0)
        self.msg_text.setY(0)

        self.sitting_time_text = self.scene().addText("")
        self.sitting_time_text.setDefaultTextColor(color)
        self.sitting_time_text.setX(0)
        self.sitting_time_text.setY(26)

        self.score_list = [0]
        self.minimize = False

        self.connected_changed(False)

    def start(self, score):
        self.score_list = [score]

    def showEvent(self, event):
        size = self.viewport().size()
        self.scene().setSceneRect(0, 0, size.width(), size.height())
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    def update_score(self, score, msg, sitting_time):
        if msg == "바른 자세":
            self.minimize = True
            self.msg_text.setDocument(make_text("", 24))
        else:
            self.minimize = False
            self.msg_text.setDocument(make_text(msg, 24))
        self.sitting_time_text.setDocument(make_text("{:.0f}초".format(sitting_time), 16))
        if msg != "일어섬":
            self.score_list.append(score)

    def update_screen(self):
        score = self.score_list[-1]
        size = self.viewport().size()
        width = size.width()
        height = size.height()

        gradient = QLinearGradient(QPointF(0, 0), QPointF(0, height))
        gradient.setColorAt(0.0, QColor.fromRgb(0x35, 0x37, 0x72))
        gradient.setColorAt(1.0, Qt.white)
        self.graph.setBrush(QBrush(gradient))

        self.score_text.setDocument(make_text("{:.0f}".format(score), 36))
        self.score_text.setX((width - self.score_text.boundingRect().width()))
        self.score_text.setY(0)

        window_size = 1000
        scores = self.score_list[-window_size:]
        self.update_graph(scores, width, height)

        self.scene().update()

    def update_graph(self, scores, width, height):
        if len(scores) > 1 and not self.minimize:
            min_score = (int(min(scores) + 1) // 100) * 100
            max_score = (int(max(scores) + 1) // 100 + 1) * 100

            def get_y(sc):
                h = height * 0.7
                return height - ((sc - min_score) / (max_score - min_score + 0.0001) * h)

            points = [QPointF(0, height)]
            path = None
            for i, s in enumerate(scores):
                x = i / (len(scores) - 1) * (width - 6) + 3
                y = get_y(s)
                point = QPointF(x, min(y, height - 5))
                points.append(point)
                if path is None:
                    path = QPainterPath(point)
                else:
                    path.lineTo(point)
            points.append(QPointF(width, height))
            polygon = QPolygonF(points)
            self.graph.setPolygon(polygon)
            self.path.setPath(path)
        else:
            self.graph.setPolygon(QPolygonF())
            self.path.setPath(QPainterPath())

    def connected_changed(self, connected):
        if not connected:
            self.msg_text.setDocument(make_text("장치를 연결해 주세요.", 24))
            self.minimize = False
            self.update_screen()


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
        self.alt_position = False

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

        self.update_size()

        self.label = QLabel("...")

        self.graph_view = GraphView()

        layout = QVBoxLayout()
        # layout.addWidget(self.label)
        layout.addWidget(self.graph_view)
        layout.setContentsMargins(20, 20, 20, 20)

        frame = QWidget()
        frame.setLayout(layout)
        frame.setProperty("class", "overlay")

        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
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
            width, height = 1.5, 0.9
        else:
            width, height = 5, 3
        if self.alt_position:
            align = Qt.LeftToRight
        else:
            align = Qt.RightToLeft

        desktop: QDesktopWidget = QApplication.instance().desktop()
        desktop_rect = desktop.availableGeometry()
        dpi_x = desktop.logicalDpiX()
        dpi_y = desktop.logicalDpiY()
        popup_size = QSize(dpi_x * width, dpi_y * height)
        rect = QStyle.alignedRect(align, Qt.AlignVCenter, popup_size, desktop_rect)
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
        self.score_manager.updateScore.connect(self.graph_view.update_score)

        self.show()

    def score_update(self, score, msg):
        if not self.state.is_logged_in():
            return
        if msg == "바른 자세":
            self.minimize = True
        else:
            self.minimize = False

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
        self.opacity.setOpacity(0.1)
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
