from PyQt5.QtCore import QObject, pyqtSignal, QThread


class ScoreManager(QObject):
    updateScore = pyqtSignal(float, str, name='updateScore')

    def __init__(self, device):
        super().__init__()
        self.device = device
        self.score = 0
        self.msg = ""
        device.updateNumber.connect(self.score_update)

    def score_update(self, values):
        lhip, lthigh, lback, rhip, rthigh, rback = values
        thigh_imbalance = (lthigh - rthigh) / (lthigh + rthigh + 1)
        msg = ""
        if sum(values) == 0:
            msg = "일어섬"
        elif thigh_imbalance > 0.5:
            self.score -= 1
            msg = "허벅지 왼쪽으로 쏠림"
        elif thigh_imbalance < -0.5:
            self.score -= 1
            msg = "허벅지 오른쪽으로 쏠림"
        elif lhip == 0 and rhip == 0:
            self.score -= 1
            msg = "둔부를 내민 자세"
        elif lback == 0 and rback == 0:
            self.score -= 1
            msg = "허리를 숙인 자세"
        else:
            self.score += 1
            msg = "바른 자세"
        self.updateScore.emit(self.score, msg)

