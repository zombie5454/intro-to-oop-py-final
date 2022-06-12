from PyQt5 import QtWidgets
from UI.QtUI import Ui_Widget
from typing import Callable
from Control.Controller import Controller


def unused(func: Callable) -> Callable:
    return func


class CustomListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, id: int, text: str, parent: QtWidgets.QListWidget):
        super().__init__(text, parent)
        self.id = id


class View(QtWidgets.QWidget):
    def __init__(self):
        super(View, self).__init__()

        # attributes
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.controller = None

        # homePage
        self.ui.enterExamButton.clicked.connect(self.enterExam)
        self.ui.bankList.itemDoubleClicked.connect(self.enterExam)
        self.ui.deleteBankButton.clicked.connect(self.deleteBank)
        self.ui.editBankButton.clicked.connect(self.editBank)
        self.ui.addBankButton.clicked.connect(self.addBank)

        # editBankPage
        self.ui.homeButton.clicked.connect(self.goHome)
        self.ui.bankSaveButton.clicked.connect(self.saveBank)
        self.ui.deleteQuestionButton.clicked.connect(self.deleteQuestion)
        self.ui.editQuestionButton.clicked.connect(self.editQuestion)
        self.ui.addQuestionButton.clicked.connect(self.addQuestion)

        # editQuestionPage
        self.ui.backButton.clicked.connect(self.goToEditBankPage)
        self.ui.saveQuestionButton.clicked.connect(self.saveQuestion)
        self.ui.questionType.currentIndexChanged.connect(self.changeQuestionType)

        # enterExamPage
        self.ui.homeButton_2.clicked.connect(self.goHome)
        self.ui.beginExamButton.clicked.connect(self.beginExam)

        # examPage
        self.ui.homeButton_3.clicked.connect(self.goHome)
        self.ui.nextQuestionButton.clicked.connect(self.nextQuestion)
        self.ui.showAnswerButton.clicked.connect(self.showAnswer)
        self.ui.checkAnswerButton.clicked.connect(self.checkAnswer)

        # resultPage
        self.ui.homeButton_4.clicked.connect(self.goHome)
        self.ui.testAgainButton.clicked.connect(self.testAgain)

        # hide unsupported features
        self.ui.deleteBankButton.setVisible(False)
        self.ui.deleteQuestionButton.setVisible(False)
        self.ui.editQuestionButton.setVisible(False)

        # initialize
        self.goHome()

    def goHome(self):
        self.ui.bankList.clear()
        for bank in self.controller.getBanks():
            self.ui.bankList.addItem(CustomListWidgetItem(bank.name, bank.name, self.ui.bankList))
        # self.ui.bankList.setCurrentItem(self.ui.bankList.item(0))
        self.ui.stackedPages.setCurrentWidget(self.ui.homePage)

    def goToEditBankPage(self):
        self.ui.questionList.clear()
        if self.ui.bankList.currentItem() is not None:
            bankName = self.ui.bankList.currentItem().text()
            self.ui.bankName.setText(bankName)
            for q in self.controller.getQuestionList(bankName, 10):
                self.ui.questionList.addItem(CustomListWidgetItem(q.id, q.text.split("\n")[0], self.ui.questionList))
        # self.ui.questionList.setCurrentItem(self.ui.questionList.item(0))
        self.ui.stackedPages.setCurrentWidget(self.ui.editBankPage)

    def goToEditQuestionPage(self):
        self.ui.questionType.setCurrentIndex(0)
        self.ui.stackedAnswer.setCurrentWidget(self.ui.choice)
        if self.ui.questionList.currentItem() is not None:
            questionText = self.ui.questionList.currentItem().text()
            id = self.ui.questionList.currentItem().id
            self.ui.questionText.setPlainText(questionText)
            self.ui.shortAnswer_1.setPlainText(self.controller.getQuestion(self.ui.bankName.text(), id).answer)
        self.ui.stackedPages.setCurrentWidget(self.ui.editQuestionPage)

    def goToEnterExamPage(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.enterExamPage)

    def goToExamPage(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.examPage)
        self.ui.stackedExamAnswer.setCurrentWidget(self.ui.examChoice)  ##

    def goToResultPage(self):
        rightNum, totalNum, showNum = self.controller.endExam()
        self.ui.questionRightNum.setText(str(rightNum))
        self.ui.questionWrongNum.setText(str(totalNum - rightNum))
        self.ui.questionShowNum.setText(str(showNum))
        self.ui.stackedPages.setCurrentWidget(self.ui.resultPage)

    def setController(self, controller):
        self.controller = controller

    @unused
    def deleteBank(self):
        if self.ui.bankList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No bank selected!")
            return
        bankName = self.ui.bankList.currentItem().text()
        reply = QtWidgets.QMessageBox.question(
            None,
            "刪除題庫",
            "確定要刪除題庫「" + bankName + "」嗎？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.controller.deleteBank(bankName)
            self.goHome()

    def editBank(self):
        self.ui.bankName.setEnabled(False)
        if self.ui.bankList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No bank selected!")
            return
        self.goToEditBankPage()

    def addBank(self):
        self.ui.bankName.setEnabled(True)
        self.ui.bankList.setCurrentItem(None)
        self.ui.bankName.setText("")
        self.goToEditBankPage()

    def saveBank(self):
        bankName = self.ui.bankName.text()
        try:
            self.controller.addBank(Bank(bankName))
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", str(e))
        self.goHome()

    @unused
    def deleteQuestion(self):
        if self.ui.questionList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No question selected!")
            return
        questionText = self.ui.questionList.currentItem().text()
        reply = QtWidgets.QMessageBox.question(
            None,
            "刪除題目",
            "確定要刪除題目「" + questionText + "」嗎？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.controller.deleteQuestion(self.ui.bankList.currentItem().text(), questionText)
            self.goToEditBankPage()

    @unused
    def editQuestion(self):
        if self.ui.questionList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No question selected!")
            return
        self.goToEditQuestionPage()

    def addQuestion(self):
        self.ui.questionText.setPlainText("")
        self.ui.questionList.setCurrentItem(None)
        self.goToEditQuestionPage()

    def saveQuestion(self):
        bankName = self.ui.bankList.currentItem().text()
        questionType = self.ui.questionType.currentText()
        questionText = self.ui.questionText.toPlainText()
        shortAnswer_1 = self.ui.shortAnswer_1.toPlainText()
        try:
            self.controller.addQuestion(bankName, questionType, questionText, shortAnswer_1)
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", str(e))
        self.goToEditBankPage()

    def changeQuestionType(self):
        index = self.ui.questionType.currentIndex()
        self.ui.stackedAnswer.setCurrentIndex(index)

    def enterExam(self):
        if self.ui.bankList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No bank selected!")
            return
        bankName = self.ui.bankList.currentItem().text()
        questionNum = self.controller.enterExam(bankName)
        self.ui.bankName_2.setText(bankName)
        self.ui.questionNum.setText(str(questionNum))
        self.ui.examNum.setMaximum(questionNum)
        self.goToEnterExamPage()

    def beginExam(self):
        bankName = self.ui.bankName_2.text()
        examNum = int(self.ui.examNum.text())
        self.controller.beginExam(bankName, examNum)
        self.ui.stackedPages.setCurrentWidget(self.ui.examPage)
        self.nextQuestion()

    def nextQuestion(self):
        question, idx = self.controller.getNextQuestion()
        if idx == int(self.ui.examNum.text()):
            self.ui.nextQuestionButton.setText("結束測驗")
        if idx == -1:
            self.goToResultPage()
            self.ui.nextQuestionButton.setText("下一題")
            return
        self.ui.examQuestionType.setText(question.type)
        self.ui.examQuestionText.setText(question.text)
        self.ui.examShortAnswer_1.setPlainText("")
        self.ui.examShortAnswer_1.setStyleSheet("color: white")
        self.ui.currentNum.setText(str(idx))
        self.ui.examShortAnswer_1.setFocus()
        self.ui.examShortAnswer_1.setEnabled(True)
        self.ui.checkAnswerButton.setEnabled(True)

    def showAnswer(self):
        answer = self.controller.showAnswer()
        self.ui.examShortAnswer_1.setPlainText(answer)

    def checkAnswer(self):
        answer = self.ui.examShortAnswer_1.toPlainText()
        self.ui.examShortAnswer_1.setEnabled(False)
        self.ui.checkAnswerButton.setEnabled(False)
        correct = self.controller.checkAnswer(answer)
        if correct:
            self.ui.examShortAnswer_1.setStyleSheet("color: green")
        else:
            self.ui.examShortAnswer_1.setStyleSheet("color: red")
            self.ui.examShortAnswer_1.setPlainText(self.ui.examShortAnswer_1.toPlainText() + "\n\n錯誤答案\n")

    def testAgain(self):
        self.goToEnterExamPage()
