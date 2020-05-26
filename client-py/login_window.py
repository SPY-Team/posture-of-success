from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QSizePolicy, QHBoxLayout, QGroupBox\
    , QErrorMessage, QCheckBox
from PyQt5.QtCore import pyqtSignal, QUrl, QCoreApplication, QSettings
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
        self.setGeometry(300, 300, 600, 400)

        label = QLabel("로그인")

        self.id_field = QLineEdit(self.settings.value("login/id", ""))
        self.id_field.setPlaceholderText("Email")
        self.pw_field = QLineEdit(self.settings.value("login/pw", ""))
        self.pw_field.setPlaceholderText("Password")
        self.pw_field.setEchoMode(QLineEdit.Password)

        fields_box = QVBoxLayout()
        fields_box.addWidget(self.id_field)
        fields_box.addWidget(self.pw_field)

        self.login_button = QPushButton("로그인")
        self.login_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        register_button = QPushButton("회원가입")
        register_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)

        form_box = QHBoxLayout()
        form_box.addLayout(fields_box)
        form_box.addWidget(self.login_button)
        form_box.addWidget(register_button)

        self.save_login_checkbox = QCheckBox("다음부터 자동 로그인")

        login_box = QVBoxLayout()
        login_box.addWidget(label)
        login_box.addLayout(form_box)
        login_box.addWidget(self.save_login_checkbox)

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
                if self.save_login_checkbox.isChecked():
                    self.save_login(self.id_field.text(), self.pw_field.text())
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

    def register(self):
        QDesktopServices.openUrl(QUrl(SERVER_BASE_ADDR + "/signup"))

    def update_status(self):
        if self.device.is_connected():
            self.device_status.setText("장치가 연결되었습니다.")
        else:
            self.device_status.setText("장치가 연결되어 있지 않습니다. 연결을 기다리는 중...")

    def closeEvent(self, event: QCloseEvent):
        if not self.logged_in:
            QCoreApplication.exit()
