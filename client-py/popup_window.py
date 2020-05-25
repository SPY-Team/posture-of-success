from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QApplication, QStyle, QLabel, QVBoxLayout, \
    QDesktopWidget
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor, QPainter, QFont, QTextDocument, QTextCharFormat, QTextCursor, \
    QCloseEvent, QRgba64
from PyQt5.QtCore import Qt, QSize, QPointF


def make_text(text):
    document = QTextDocument()
    fmt = QTextCharFormat()
    fmt.setFont(QFont("monospace", 24))
    fmt.setTextOutline(QPen(Qt.black))
    cursor = QTextCursor(document)
    cursor.insertText(text, fmt)
    return document


class GraphView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene())
        self.setBackgroundBrush(QColor(QRgba64.fromRgba(43, 43, 43, 10)))
        self.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.transparent)
        brush = QBrush(Qt.green)
        self.graph = self.scene().addPolygon(QPolygonF(), pen, brush)
        self.score_text = self.scene().addText("Score")
        self.score_text.setDefaultTextColor(Qt.white)
        self.msg_text = self.scene().addText("Message")
        self.msg_text.setDefaultTextColor(Qt.white)
        self.score_list = []

    def showEvent(self, event):
        size = self.viewport().size()
        self.scene().setSceneRect(0, 0, size.width(), size.height())
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    def update_score(self, score, msg):
        self.score_list.append(score)

        size = self.viewport().size()
        width = size.width()
        height = size.height()

        self.score_text.setDocument(make_text(str(score)))
        self.score_text.setX((width - self.score_text.boundingRect().width()) // 2)
        self.score_text.setY((height - self.score_text.boundingRect().height()) // 2)

        self.msg_text.setDocument(make_text(msg))

        window_size = 100
        scores = self.score_list[-window_size:]

        if len(scores) > 1:
            min_score = min(scores)
            max_score = max(scores)
            points = [QPointF(0, height)]
            for i, s in enumerate(scores):
                x = i / (len(scores) - 1) * width
                y = height - ((s - min_score) / (max_score - min_score + 1) * height)
                points.append(QPointF(x, y))
            points.append(QPointF(width, height))
            polygon = QPolygonF(points)
            self.graph.setPolygon(polygon)
            if scores[-2] < scores[-1]:
                self.graph.setBrush(QBrush(Qt.green))
            else:
                self.graph.setBrush(QBrush(Qt.red))
        self.scene().update()


class PopupWindow(QWidget):
    def __init__(self, score_manager):
        super().__init__()

        self.score_manager = score_manager
        self.device = score_manager.device

        # Setup UI
        self.setWindowFlags(
            Qt.CustomizeWindowHint |
            Qt.WindowStaysOnTopHint |
            Qt.Dialog |
            Qt.Tool |
            Qt.FramelessWindowHint |
            Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.setStyleSheet("background-color: rgba(0,0,0,0)")

        desktop: QDesktopWidget = QApplication.instance().desktop()
        desktop_rect = desktop.availableGeometry()
        dpi_x = desktop.logicalDpiX()
        dpi_y = desktop.logicalDpiY()
        popup_size = QSize(dpi_x, dpi_y)
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignHCenter, popup_size, desktop_rect))

        self.label = QLabel("...")

        self.graph_view = GraphView()

        main_layout = QVBoxLayout()
        #main_layout.addWidget(self.label)
        main_layout.addWidget(self.graph_view)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)

        # Connect
        score_manager.device.updateNumber.connect(self.sensor_update)
        score_manager.updateScore.connect(self.graph_view.update_score)

    def start(self):
        self.show()

    def sensor_update(self, score):
        self.label.setText(str(score))

    def closeEvent(self, event: QCloseEvent):
        event.ignore()
