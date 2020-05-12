from PyQt5.QtWidgets import QGraphicsView, QGraphicsScene, QWidget, QApplication, QStyle, QLabel, QVBoxLayout
from PyQt5.QtGui import QPolygonF
from PyQt5.QtCore import Qt, QSize


class GraphView(QGraphicsView):
    def __init__(self):
        super().__init__()

        self.scene = QGraphicsScene()
        super().setScene(self.scene)

        self.graph = self.scene.addPolygon(QPolygonF())

    def showEvent(self, event):
        size = self.viewport().size()
        self.scene.setSceneRect(0, 0, size.width(), size.height())


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

    def start(self):
        self.show()

    def sensor_update(self, score):
        self.label.setText(str(score))
