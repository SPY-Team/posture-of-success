from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from PyQt5.QtCore import QCoreApplication, pyqtSignal
from PyQt5.QtGui import QIcon


class SystemTrayIcon(QSystemTrayIcon):
    calibrate = pyqtSignal()
    logout = pyqtSignal()

    def __init__(self, state, parent=None):
        QSystemTrayIcon.__init__(self, QIcon('icon.png'), parent)
        menu = QMenu(parent)
        self.calibrate_action = menu.addAction("센서 조정")
        self.logout_action = menu.addAction("로그아웃")
        self.exit_action = menu.addAction("종료")
        self.setContextMenu(menu)
        menu.triggered.connect(self.action)
        self.login_changed(state.is_logged_in())
        state.loginChanged.connect(self.login_changed)

    def login_changed(self, logged_in):
        self.calibrate_action.setEnabled(logged_in)

    def action(self, action):
        if action == self.calibrate_action:
            self.calibrate.emit()
        elif action == self.exit_action:
            QCoreApplication.exit()
        elif action == self.logout_action:
            self.logout.emit()
