from PyQt5 import QtWidgets


class MyListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, id: int, text: str, parent: QtWidgets.QListWidget):
        super().__init__(text, parent)
        self.id = id


class MyRadioButton(QtWidgets.QRadioButton):
    def __init__(self, is_true: bool, text: str):
        super().__init__(text)
        self.is_true = is_true
