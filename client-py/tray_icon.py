from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from PyQt5.QtCore import QCoreApplication, pyqtSignal


class SystemTrayIcon(QSystemTrayIcon):
    logout = pyqtSignal()

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        menu = QMenu(parent)
        self.logout_action = menu.addAction("로그아웃")
        self.exit_action = menu.addAction("종료")
        self.setContextMenu(menu)
        menu.triggered.connect(self.action)

    def action(self, action):
        if action == self.exit_action:
            QCoreApplication.exit()
        elif action == self.logout_action:
            self.logout.emit()
