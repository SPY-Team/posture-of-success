from PyQt5.QtWidgets import QSystemTrayIcon, QMenu
from PyQt5.QtCore import QCoreApplication


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
