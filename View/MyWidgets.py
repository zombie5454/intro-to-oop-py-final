from PyQt5 import QtWidgets, QtCore
from typing import Any, Callable
from Model.question import Question
from Model.question_type import QuestionType
from Model.question_bank import QuestionBank


class BankListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, bank: QuestionBank, parent: QtWidgets.QListWidget):
        super().__init__("   " + bank.name + "   ", parent)
        self.id = bank.issuedID
        self.bankName = bank.name
        self.bankDir = bank.directory


class QuestionListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, question: Question, parent: QtWidgets.QListWidget):
        super().__init__("   " + question.question.replace("\n", "  ") + "   ", parent)
        self.id = question.ID
        self.questionType = question.type
        self.questionText = question.question
        if question.type == QuestionType.CHOICE or question.type == QuestionType.MULTIPLECHOICE:
            self.questionChoices = question.choices
        elif question.type == QuestionType.FILL:
            self.questionAns = question.ans


class MyRadioButton(QtWidgets.QRadioButton):
    def __init__(self, is_true: bool, text: str):
        super().__init__(text)
        self.is_true = is_true


class MyTimer(object):
    def __init__(self):
        self.timer = QtCore.QTimer()

    def singleShot(self, msec: int, func: Callable):
        self.timer.stop()
        self.timer.deleteLater()
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(func)
        self.timer.setSingleShot(True)
        self.timer.start(msec)
