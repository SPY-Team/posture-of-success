from PyQt5.QtCore import pyqtSignal, QObject


class State(QObject):
    loginChanged = pyqtSignal(bool, name="loginChanged")

    def __init__(self, parent=None):
        super().__init__(parent)
        self.user_email = None
        self.score = None
        self.sensor_values = None

    def login(self, email, score):
        if not self.is_logged_in():
            self.user_email = email
            self.score = score
            self.loginChanged.emit(True)

    def logout(self):
        if self.is_logged_in():
            self.user_email = None
            self.score = None
            self.loginChanged.emit(False)

    def is_logged_in(self):
        return self.user_email is not None
