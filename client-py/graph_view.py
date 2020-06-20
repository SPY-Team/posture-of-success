from PyQt5.QtCore import Qt, QPointF
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor, QPainter, QFont, QTextDocument, QTextCharFormat, QTextCursor, \
    QLinearGradient, QPainterPath
from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QApplication


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

        self.score_list = [0]
        self.minimize = False
        self.size_changed(False)

        self.connected_changed(False)

    def start(self, score):
        self.score_list = [score]

    def showEvent(self, event):
        size = self.viewport().size()
        self.scene().setSceneRect(0, 0, size.width(), size.height())
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    def size_changed(self, minimized):
        self.minimize = minimized
        size = self.viewport().size()
        width = size.width()
        if minimized:
            self.sitting_time_text.setX(width - self.sitting_time_text.boundingRect().width())
            self.sitting_time_text.setY(38)
            self.msg_text.hide()
        else:
            self.sitting_time_text.setX(0)
            self.sitting_time_text.setY(26)
            self.msg_text.show()

    def update_score(self, score, msg, sitting_time, minimize):
        self.size_changed(minimize)
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
        self.score_text.setX(width - self.score_text.boundingRect().width())
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
            self.size_changed(False)
            self.update_screen()

