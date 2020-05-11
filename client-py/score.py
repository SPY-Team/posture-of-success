from PyQt5.QtCore import QObject, pyqtSignal, QThread


class ScoreManager(QObject):
    updateScore = pyqtSignal(float, name='updateScore')

    def __init__(self, device):
        super().__init__()
        self.device = device
        device.updateNumber.connect(self.score_update)

    def score_update(self, values):
        self.updateScore.emit(values[0])
