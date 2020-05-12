import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QIcon, QPolygonF
from score import ScoreManager
import connect
import simul

class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.exit_action = menu.addAction("종료")
        self.setContextMenu(menu)
        menu.triggered.connect(self.exit)

    def exit(self, action):
        if action == self.exit_action:
            QCoreApplication.exit()


class LoginWindow(QWidget):
    loginSuccess = pyqtSignal()

    def __init__(self, device):
        super().__init__()

        self.device = device

        # Setup UI
        self.setWindowTitle("성공의 자세")
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(300, 300, 600, 400)

        label = QLabel("로그인")

        id_field = QLineEdit()
        id_field.setPlaceholderText("ID")
        pw_field = QLineEdit()
        pw_field.setPlaceholderText("Password")
        pw_field.setEchoMode(QLineEdit.Password)

        fields_box = QVBoxLayout()
        fields_box.addWidget(id_field)
        fields_box.addWidget(pw_field)

        login_button = QPushButton("로그인")
        login_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        register_button = QPushButton("회원가입")
        register_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        form_box = QHBoxLayout()
        form_box.addLayout(fields_box)
        form_box.addWidget(login_button)
        form_box.addWidget(register_button)

        login_box = QVBoxLayout()
        login_box.addWidget(label)
        login_box.addLayout(form_box)

        login_group = QGroupBox()
        login_group.setLayout(login_box)

        login_box = QVBoxLayout()
        login_box.addWidget(login_group)

        self.device_status = QLabel()
        self.device_status.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        main_layout = QVBoxLayout()
        main_layout.addLayout(login_box)
        main_layout.addWidget(self.device_status)
        main_layout.setStretch(0, 0)
        main_layout.setStretch(1, 1)

        self.setLayout(main_layout)

        # Connect
        self.update_status()
        login_button.clicked.connect(self.login_clicked)

    def login_clicked(self):
        self.loginSuccess.emit()
        self.close()

    def update_status(self):
        if self.device.is_connected():
            self.device_status.setText("장치가 연결되었습니다.")
        else:
            self.device_status.setText("장치가 연결되어 있지 않습니다. 연결을 기다리는 중...")


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("성공의 자세")
    app.setQuitOnLastWindowClosed(False)

    # Tray Icon
    tray_icon = SystemTrayIcon(QIcon('icon.png'))
    tray_icon.show()

    # Start background thread
    device_thread = QThread()
    device = connect.Device()
    device.moveToThread(device_thread)
    device_thread.started.connect(device.run)
    device_thread.start()

    # Score calculation
    score_manager = ScoreManager(device)

    # Login Window
    login = LoginWindow(device)
    login.show()

    # Popup Window
    popup = PopupWindow(score_manager)
    login.loginSuccess.connect(popup.start)

    sys.exit(app.exec_())
