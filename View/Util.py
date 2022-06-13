from PyQt5 import QtCore
from typing import Callable


def unused(func: Callable) -> Callable:
    return func


class MyTimer:
    def __init__(self):
        self.timer = QtCore.QTimer()

    def singleShot(self, msec: int, func: Callable):
        self.timer.stop()
        self.timer.deleteLater()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(func)
        self.timer.setSingleShot(True)
        self.timer.start(msec)
