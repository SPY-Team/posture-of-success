import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFont, QFontDatabase

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
    QFontDatabase.addApplicationFont("font.ttf")
    app.setFont(QFont("GMarket Sans TTF", 12))
    app.setStyleSheet("""
    * {
        color: #353772;
        margin: 0;
        padding: 0;
    }
    .big {
        font-size: 32px;
    }
    QLineEdit {
        height: 30px;
        font-size: 20px;
    }
    .root > * {
        background-color: white;
        border-radius: 30px;
    }
    QPushButton {
        height: 36px;
    }
    QPushButton::open {
        color: white;
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2a366e, stop:1 #394994);
        border: none;
        border-radius: 4px;
        padding: 5px 20px;
    }
    QPushButton::closed {
        color: white;
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #394994, stop:1 #2a366e);
        border: none;
        border-radius: 4px;
        padding: 5px 20px;
    }
    QPushButton::open.inverted {
        color: #353772;
        background-color: #dddddd;
        border: none;
        border-radius: 4px;
        padding: 5px 20px;
    }
    QPushButton::closed.inverted {
        color: grey;
        background-color: white;
        border: none;
        border-radius: 4px;
        padding: 5px 20px;
    }
    QLineEdit {
        background-color: transparent;
        border: none;
        border-bottom: 3px solid #dddddd;
        margin: 5px 0px;
    }
    QLineEdit:focus {
        border: none;
        border-bottom: 3px solid #353772;
    }
    QCheckBox::indicator {
        width: 20px;
        height: 20px;
    }
    """)

    # Tray Icon
    tray_icon = SystemTrayIcon(QIcon('icon.png'))
    tray_icon.show()

    # Start device thread
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

    tray_icon.logout.connect(popup.real_close)
    tray_icon.logout.connect(login.logout)

    sys.exit(app.exec_())
