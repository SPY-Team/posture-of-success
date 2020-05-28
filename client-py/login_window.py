from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QSizePolicy, QHBoxLayout, QGroupBox\
    , QErrorMessage, QCheckBox, QGridLayout, QFrame
from PyQt5.QtCore import pyqtSignal, QUrl, QCoreApplication, QSettings, Qt
from PyQt5.QtGui import QIcon, QDesktopServices, QCloseEvent
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager, QNetworkReply
import json
from config import SERVER_BASE_ADDR


class LoginWindow(QWidget):
    tryLogin = pyqtSignal(dict, name="tryLogin")
    loginSuccess = pyqtSignal()

    def __init__(self, device):
        super().__init__()

        self.settings = QSettings("Capstone", "posture-of-success")

        self.device = device
        self.is_waiting = False
        self.login = QNetworkAccessManager()
        self.login.finished.connect(self.login_response)
        self.logged_in = False

        self.error_dialog = QErrorMessage()

        # Setup UI
        self.setWindowTitle("성공의 자세")
        self.setWindowIcon(QIcon('icon.png'))
        self.setGeometry(300, 300, 560, 460)

        label = QLabel("로그인")
        label.setProperty("class", "big")

        self.id_field = QLineEdit(self.settings.value("login/id", ""))
        self.id_field.setPlaceholderText("Email")
        self.pw_field = QLineEdit(self.settings.value("login/pw", ""))
        self.pw_field.setPlaceholderText("Password")
        self.pw_field.setEchoMode(QLineEdit.Password)
        self.pw_field.returnPressed.connect(self.login_clicked)

        fields_box = QVBoxLayout()
        fields_box.addWidget(self.id_field)
        fields_box.addWidget(self.pw_field)

        self.login_button = QPushButton("로그인")
        register_button = QPushButton("회원가입")
        register_button.setProperty("class", "inverted")

        self.save_login_checkbox = QCheckBox("자동 로그인")

        self.device_status = QLabel()

        grid = QGridLayout()
        grid.addWidget(self.save_login_checkbox, 0, 0)
        grid.addWidget(self.login_button, 0, 1)
        grid.addWidget(self.device_status, 1, 0)
        grid.addWidget(register_button, 1, 1)
        grid.setSpacing(20)

        login_box = QVBoxLayout()
        login_box.addStretch(1)
        login_box.addWidget(label)
        login_box.addLayout(fields_box)
        login_box.addLayout(grid)
        login_box.addStretch(1)

        login_box.setContentsMargins(50, 50, 50, 50)
        login_box.setSpacing(20)

        frame = QWidget()
        frame.setLayout(login_box)

        main_layout = QVBoxLayout()
        main_layout.addWidget(frame)
        main_layout.setContentsMargins(0, 0, 0, 0)

        self.setLayout(main_layout)
        self.setProperty("class", "root")
        self.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(Qt.WA_TranslucentBackground)
        #self.setWindowFlags(Qt.FramelessWindowHint)

        # Connect
        self.update_status()
        self.device.connectedChanged.connect(self.update_status)
        self.login_button.clicked.connect(self.login_clicked)
        register_button.clicked.connect(self.register)

        if self.settings.value("login/id", "") != "":
            self.save_login_checkbox.setChecked(True)
            self.login_clicked()

    def login_clicked(self):
        if not self.is_waiting:
            print("login clicked")
            self.is_waiting = True
            self.login_button.setEnabled(False)
            data = {"email": self.id_field.text(),
                    "password": self.pw_field.text()}

            req = QNetworkRequest(QUrl(SERVER_BASE_ADDR + "/api/device/signin"))
            req.setRawHeader("Content-Type".encode('utf-8'), "application/json".encode('utf-8'))
            self.login.post(req, json.dumps(data).encode('utf-8'))

    def login_response(self, response : QNetworkReply):
        self.is_waiting = False
        self.login_button.setEnabled(True)

        err = response.error()
        if err == QNetworkReply.NoError:
            reply = str(response.readAll(), 'utf-8')
            reply_json = json.loads(reply)
            print(reply_json)
            if "success" in reply_json and reply_json["success"]:
                self.logged_in = True
                self.loginSuccess.emit()
                self.close()
            else:
                self.error_dialog.showMessage('아이디나 비밀번호가 맞지 않습니다!')
        else:
            self.error_dialog.showMessage("서버 연결에 실패했습니다. 에러 코드=" + str(err))

    def save_login(self, id, pw):
        self.settings.setValue("login/id", id)
        self.settings.setValue("login/pw", pw)
        self.settings.sync()

    def register(self):
        QDesktopServices.openUrl(QUrl(SERVER_BASE_ADDR + "/signup"))

    def update_status(self):
        if self.device.is_connected():
            self.device_status.setText("장치가 연결되었습니다.")
        else:
            self.device_status.setText("장치 연결을 기다리는 중...")

    def logout(self):
        self.logged_in = False
        self.show()

    def closeEvent(self, event: QCloseEvent):
        if self.save_login_checkbox.isChecked():
            print("saving login info")
            self.save_login(self.id_field.text(), self.pw_field.text())
        else:
            print("deleting login info")
            self.save_login("", "")
        if not self.logged_in:
            QCoreApplication.exit()
