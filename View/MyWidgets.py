from PyQt5 import QtWidgets
from typing import Any


class MyListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, key: Any, text: str, parent: QtWidgets.QListWidget):
        super().__init__(text, parent)
        self.key = key


class MyRadioButton(QtWidgets.QRadioButton):
    def __init__(self, is_true: bool, text: str):
        super().__init__(text)
        self.is_true = is_true
