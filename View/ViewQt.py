import random
from PyQt5 import QtWidgets
from typing import Union
from UI.QtUI import Ui_Widget


class Problem(object):  # Sample
    def __init__(self, type, text, answer):
        self.type = type
        self.text = text
        self.answer = str(answer)


class Bank(object):  # Sample
    def __init__(self, name, problems):
        self.name = name
        self.problems = problems


banks = [  # TEST
    Bank(
        "範例題庫一",
        [
            Problem("單選", "1 + 1 = ?\n(A) 2\n(B) 3\n(C) 4\n(D) 5", "B"),
            Problem("填充", "1 + 1 = ?", "2"),
            Problem("多選", "1 + 1 < ?\n(A) 2\n(B) 3\n(C) 4\n(D) 5", "AB"),
        ],
    ),
    Bank("範例題庫二", []),
    Bank("範例題庫三", []),
]


class View(QtWidgets.QWidget):
    def __init__(self):
        super(View, self).__init__()
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.__banks = {}
        self.__test = []
        self.__testIndex = 0
        self.initBanks()

        # homePage
        self.ui.bankList.setCurrentItem(self.ui.bankList.item(0))
        self.ui.enterTestButton.clicked.connect(self.goToEnterTestPage)
        self.ui.bankList.itemDoubleClicked.connect(self.goToEnterTestPage)
        self.ui.deleteBankButton.clicked.connect(self.deleteBank)
        self.ui.addBankButton.clicked.connect(self.addBank)
        self.ui.editBankButton.clicked.connect(self.editBank)

        # editBankPage
        self.ui.homeButton.clicked.connect(self.goHome)
        self.ui.deleteProblemButton.clicked.connect(self.deleteProblem)
        self.ui.addProblemButton.clicked.connect(self.addProblem)
        self.ui.editProblemButton.clicked.connect(self.editProblem)

        # editProblemPage
        self.ui.backButton.clicked.connect(self.goToEditPage)
        self.ui.saveProblemButton.clicked.connect(self.saveProblem)

        # enterTestPage
        self.ui.homeButton_2.clicked.connect(self.goHome)
        self.ui.startTestButton.clicked.connect(self.startTest)

        # testPage
        self.ui.homeButton_3.clicked.connect(self.goHome)
        self.ui.nextProblemButton.clicked.connect(self.nextProblem)
        self.ui.prevProblemButton.clicked.connect(self.prevProblem)
        self.ui.lookAnswerButton.clicked.connect(self.lookAnswer)
        self.ui.submitButton.clicked.connect(self.submit)

        # resultPage
        self.ui.homeButton_4.clicked.connect(self.goHome)
        self.ui.testAgainButton.clicked.connect(self.testAgain)

        self.ui.stackedPages.setCurrentWidget(self.ui.homePage)

    def initBanks(self):
        self.__banks = {}
        for bank in banks:
            self.__banks[bank.name] = bank.problems
            self.ui.bankList.addItem(bank.name)

    def goToEnterTestPage(self):
        if self.ui.bankList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No bank selected!")
            return
        self.ui.bankName_2.setText(self.ui.bankList.currentItem().text())
        problemNum = len(self.__banks[self.ui.bankList.currentItem().text()])
        self.ui.problemNum.setText(str(problemNum))
        self.ui.testNum.setMaximum(problemNum)
        self.ui.stackedPages.setCurrentWidget(self.ui.enterTestPage)

    def deleteBank(self):
        if self.ui.bankList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No bank selected!")
            return
        reply = QtWidgets.QMessageBox.question(
            None,
            "刪除題庫",
            "確定要刪除題庫「{}」嗎？\n刪除後將無法復原。".format(self.ui.bankList.currentItem().text()),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.Yes,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            del self.__banks[self.ui.bankList.currentItem().text()]
            self.ui.bankList.takeItem(self.ui.bankList.currentRow())

    def addBank(self):
        self.ui.bankName.setText("")
        self.ui.problemList.clear()
        self.ui.stackedPages.setCurrentWidget(self.ui.editBankPage)

    def editBank(self):
        if self.ui.bankList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No bank selected!")
            return
        self.ui.bankName.setText(self.ui.bankList.currentItem().text())
        self.ui.problemList.clear()
        for problem in self.__banks[self.ui.bankList.currentItem().text()]:
            self.ui.problemList.addItem(problem.text.split("\n")[0])
        self.ui.problemList.setCurrentItem(self.ui.problemList.item(0))
        self.ui.stackedPages.setCurrentWidget(self.ui.editBankPage)

    def goHome(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.homePage)

    def deleteProblem(self):
        if self.ui.problemList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No problem selected!")
            return
        reply = QtWidgets.QMessageBox.question(
            None,
            "刪除題目",
            "確定要刪除題目「{}」嗎？\n刪除後將無法復原。".format(self.ui.problemList.currentItem().text()),
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.Yes,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            bank = self.ui.bankList.currentItem().text()
            problem = self.ui.problemList.currentRow()
            self.__banks[bank].remove(self.__banks[bank][problem])
            self.ui.problemList.takeItem(problem)

    def addProblem(self):
        if self.ui.bankName.text() == "":
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No bank name!")
            return
        self.ui.problemType.setCurrentIndex(0)
        self.ui.problemText.setPlainText("")
        self.ui.problemAnswer.setPlainText("")
        self.ui.stackedPages.setCurrentWidget(self.ui.editProblemPage)

    def editProblem(self):
        if self.ui.problemList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No problem selected!")
            return
        problem = self.__banks[self.ui.bankList.currentItem().text()][self.ui.problemList.currentRow()]
        self.ui.problemType.setCurrentText(problem.type)
        self.ui.problemText.setPlainText(problem.text)
        self.ui.problemAnswer.setPlainText(problem.answer)
        self.ui.stackedPages.setCurrentWidget(self.ui.editProblemPage)

    def goToEditPage(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.editBankPage)

    def saveProblem(self):
        pass

    def setProblem(self):
        self.ui.testProblemText.setText(self.__test[self.__testIndex].text)
        self.ui.currentNum.setText(str(self.__testIndex + 1))

    def startTest(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.testPage)
        # TODO: add Test class
        self.__test = random.sample(self.__banks[self.ui.bankName_2.text()], self.ui.testNum.value())
        self.__testIndex = 0
        self.ui.prevProblemButton.setEnabled(False)
        self.ui.nextProblemButton.setEnabled(True)
        self.setProblem()

    def nextProblem(self):
        self.saveAnswer()
        self.ui.prevProblemButton.setEnabled(True)
        self.__testIndex += 1
        if self.__testIndex >= len(self.__test) - 1:
            self.ui.nextProblemButton.setEnabled(False)
            self.__testIndex = len(self.__test) - 1
        self.setProblem()

    def prevProblem(self):
        self.saveAnswer()
        self.ui.nextProblemButton.setEnabled(True)
        self.__testIndex -= 1
        if self.__testIndex <= 0:
            self.ui.prevProblemButton.setEnabled(False)
            self.__testIndex = 0
        self.setProblem()

    def lookAnswer(self):
        pass

    def saveAnswer(self):
        pass

    def submit(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.resultPage)
        # SHOW RESULT
        self.ui.problemRightNum.setText(str(0))
        self.ui.problemWrongNum.setText(str(0))
        self.ui.problemLookNum.setText(str(0))

    def testAgain(self):
        self.goToEnterTestPage()
