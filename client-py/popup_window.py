from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QApplication, QStyle, QLabel, QVBoxLayout
from PyQt5.QtGui import QPolygonF, QPen, QBrush, QColor, QPainter, QFont, QTextDocument, QTextCharFormat, QTextCursor
from PyQt5.QtCore import Qt, QSize, QPointF


class GraphView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.setScene(QGraphicsScene())
        self.setBackgroundBrush(QColor(43, 43, 43))
        self.setRenderHint(QPainter.Antialiasing)

        pen = QPen(Qt.transparent)
        brush = QBrush(Qt.green)
        self.graph = self.scene().addPolygon(QPolygonF(), pen, brush)
        self.score_text = self.scene().addText("Score")
        self.score_text.setDefaultTextColor(Qt.white)
        self.score_list = []

    def showEvent(self, event):
        size = self.viewport().size()
        self.scene().setSceneRect(0, 0, size.width(), size.height())
        self.setAlignment(Qt.AlignTop | Qt.AlignLeft)

    def update_score(self, score):
        self.score_list.append(score)

        size = self.viewport().size()
        width = size.width()
        height = size.height()

        document = QTextDocument()
        fmt = QTextCharFormat()
        fmt.setFont(QFont("monospace", 24))
        fmt.setTextOutline(QPen(Qt.black))
        cursor = QTextCursor(document)
        cursor.insertText(str(score), fmt)
        self.score_text.setDocument(document)
        self.score_text.setX((width - self.score_text.boundingRect().width()) // 2)
        self.score_text.setY((height - self.score_text.boundingRect().height()) // 2)

        window_size = 100
        scores = self.score_list[-window_size:]

        if len(scores) > 1:
            max_score = max(scores)
            points = [QPointF(0, height)]
            for i, s in enumerate(scores):
                x = i / (len(scores) - 1) * width
                y = height - (s / max_score * height)
                points.append(QPointF(x, y))
            points.append(QPointF(width, height))
            polygon = QPolygonF(points)
            self.graph.setPolygon(polygon)


class PopupWindow(QWidget):
    def __init__(self, score_manager):
        super().__init__()

        self.score_manager = score_manager
        self.device = score_manager.device

        # Setup UI
        self.setWindowFlags(Qt.CustomizeWindowHint | Qt.WindowStaysOnTopHint | Qt.Dialog | Qt.Tool)

        desktop_rect = QApplication.instance().desktop().availableGeometry()
        self.setGeometry(QStyle.alignedRect(Qt.LeftToRight, Qt.AlignHCenter, QSize(600, 200), desktop_rect))

        self.label = QLabel("...")

        self.graph_view = GraphView()

        main_layout = QVBoxLayout()
        main_layout.addWidget(self.label)
        main_layout.addWidget(self.graph_view)

        self.setLayout(main_layout)

        # Connect
        score_manager.device.updateNumber.connect(self.sensor_update)
        score_manager.updateScore.connect(self.graph_view.update_score)

    def start(self):
        self.show()

    def sensor_update(self, score):
        self.label.setText(str(score))
