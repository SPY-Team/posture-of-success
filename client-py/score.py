from PyQt5.QtCore import QObject, pyqtSignal, QThread
import math


class ScoreManager(QObject):
    updateScore = pyqtSignal(float, str, name='updateScore')

    def __init__(self, score):
        super().__init__()
        self.score = score
        self.x = 0
        self.cooltime = 10

    def get_score(self):
        return self.score

    def score_update(self, values):
        lhip, lthigh, lback, rhip, rthigh, rback, dist = values
        thigh_imbalance = (lthigh - rthigh) / (lthigh + rthigh + 1)
        msg = ""

        if self.cooltime > 0:
            self.cooltime -= 1

        def wrong_posture():
            self.x = max(self.x - 10, 0)
            if self.cooltime == 0:
                self.score = self.score * (1 - 0.005)
                self.score -= 1
                self.cooltime = 10

        if sum(values[:6]) == 0:
            msg = "일어섬"
        elif thigh_imbalance > 0.5:
            wrong_posture()
            msg = "허벅지 왼쪽으로 쏠림"
        elif thigh_imbalance < -0.5:
            wrong_posture()
            msg = "허벅지 오른쪽으로 쏠림"
        elif lhip == 0 and rhip == 0:
            wrong_posture()
            msg = "둔부를 내민 자세"
        elif lback == 0 and rback == 0:
            wrong_posture()
            msg = "허리를 숙인 자세"
        else:
            self.x += 1
            self.score += -math.expm1(-self.x * 0.005)
            self.cooltime = 10
            msg = "바른 자세"

        self.score = max(0, self.score)
        self.updateScore.emit(self.score, msg)

