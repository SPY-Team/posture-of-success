import sys
from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon
from score import ScoreManager
from tray_icon import SystemTrayIcon
from login_window import LoginWindow
from popup_window import PopupWindow
import connect
import simul


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
