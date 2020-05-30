import sys

from PyQt5.QtCore import QThread
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QFont, QFontDatabase

from tray_icon import SystemTrayIcon
from login_window import LoginWindow
from calibration_window import CalibrationWindow
from popup_window import PopupWindow
from state import State
import connect
import simul


if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setApplicationName("성공의 자세")
    app.setQuitOnLastWindowClosed(False)
    QFontDatabase.addApplicationFont("font.ttf")
    app.setFont(QFont("210 Namoogothic", 12))
    app.setWindowIcon(QIcon('icon.png'))
    app.setStyleSheet("""
    * {
        color: #353772;
        margin: 0;
        padding: 0;
    }
    .frame {
        background-color: white; 
        border-radius: 30px;
    }
    .huge {
        font-size: 32px;
    }
    .big {
        font-size: 20px;
    }
    .overlay {
        background-color: white; 
        border-radius: 30px;
    }
    QPushButton {
        height: 36px;
        padding: 5px 20px;
        border-radius: 4px;
        border: none;
    }
    QPushButton::open {
        color: white;
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #2a366e, stop:1 #394994);
    }
    QPushButton::closed {
        color: white;
        background-color: qlineargradient(x1:0, y1:0, x2:0, y2:1,
            stop:0 #394994, stop:1 #2a366e);
    }
    QPushButton::open.inverted {
        color: #353772;
        background-color: #dddddd;
    }
    QPushButton::closed.inverted {
        color: grey;
        background-color: white;
    }
    QLineEdit {
        height: 30px;
        font-size: 20px;
        background-color: transparent;
        border: none;
        border-bottom: 2px solid #dddddd;
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
    QGraphicsView {
        border: none;
        background-color: transparent; 
    }
    """)

    # Program state
    state = State()

    # Tray Icon
    tray_icon = SystemTrayIcon(state)
    tray_icon.show()

    # Start device thread
    device_thread = QThread()
    device = connect.Device()
    device.moveToThread(device_thread)
    device_thread.started.connect(device.run)
    device_thread.start()

    # Login Window
    login = LoginWindow(state, device)

    # Calibration Window
    calib_window = CalibrationWindow(state, device)

    # Popup Window
    popup = PopupWindow(state, device)

    def show_popup():
        if state.sensor_values is None:
            calib_window.start()
        else:
            popup.start()
    login.loginSuccess.connect(show_popup)
    calib_window.calibrated.connect(show_popup)

    def logout():
        popup.logout()
        calib_window.logout()
        login.logout()
    tray_icon.logout.connect(logout)

    def calibrate():
        popup.logout()
        calib_window.start()
    tray_icon.calibrate.connect(calibrate)

    login.show()

    sys.exit(app.exec_())
