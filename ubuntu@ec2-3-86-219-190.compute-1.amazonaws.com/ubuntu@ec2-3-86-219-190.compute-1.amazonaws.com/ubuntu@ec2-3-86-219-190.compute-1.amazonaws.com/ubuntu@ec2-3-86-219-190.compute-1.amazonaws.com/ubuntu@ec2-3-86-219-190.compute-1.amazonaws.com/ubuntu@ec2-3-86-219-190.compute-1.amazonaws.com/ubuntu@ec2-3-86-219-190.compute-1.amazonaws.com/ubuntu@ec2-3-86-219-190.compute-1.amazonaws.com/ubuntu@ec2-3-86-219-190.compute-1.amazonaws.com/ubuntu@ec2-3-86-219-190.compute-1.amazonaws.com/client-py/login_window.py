from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QVBoxLayout, QPushButton, QSizePolicy, QHBoxLayout, QGroupBox
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QIcon


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
