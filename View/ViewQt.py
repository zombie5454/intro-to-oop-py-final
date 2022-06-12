from PyQt5 import QtWidgets, QtCore, QtGui
from UI.QtUI import Ui_Widget
from typing import Callable, List, Union

# from Controller.controller import Controller


from .Module import Bank, Controller, QuestionType


def unused(func: Callable) -> Callable:
    return func


class MyListWidgetItem(QtWidgets.QListWidgetItem):
    def __init__(self, id: int, text: str, parent: QtWidgets.QListWidget):
        super().__init__(text, parent)
        self.id = id


class View(QtWidgets.QWidget):
    def __init__(self):
        super(View, self).__init__()

        # attributes
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.radioButtons: List[QtWidgets.QRadioButton] = []
        self.controller = None
        self.controller = Controller(self)

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
        self.ui.bankName.textChanged.connect(lambda: self.ui.bankName.setStyleSheet("color: white"))

        # editQuestionPage
        self.ui.backButton.clicked.connect(self.goToEditBankPage)
        self.ui.saveQuestionButton.clicked.connect(self.saveQuestion)
        self.ui.questionType.currentIndexChanged.connect(self.changeQuestionType)
        self.ui.addOptionButton.clicked.connect(self.addOption)
        self.ui.newOption.returnPressed.connect(self.addOption)
        self.ui.questionText.textChanged.connect(lambda: self.ui.questionText.setStyleSheet("color: white"))
        self.ui.newOption.textChanged.connect(lambda: self.ui.newOption.setStyleSheet("color: white"))
        self.ui.shortAnswer_1.textChanged.connect(lambda: self.ui.shortAnswer_1.setStyleSheet("color: white"))

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

        # init MyComboBax
        self.ui.questionType.addItem("單選", QuestionType.CHOICE)
        self.ui.questionType.addItem("多選", QuestionType.MULTIPLECHOICE)
        self.ui.questionType.addItem("填空", QuestionType.FILL)

        # initialize
        self.goHome()

    def goHome(self):
        self.ui.bankList.clear()
        for bank in self.controller.getBanks():
            self.ui.bankList.addItem(MyListWidgetItem(bank.name, bank.name, self.ui.bankList))
        # self.ui.bankList.setCurrentItem(self.ui.bankList.item(0))
        self.ui.stackedPages.setCurrentWidget(self.ui.homePage)

    def goToEditBankPage(self):
        self.ui.questionList.clear()
        if self.ui.bankList.currentItem() is not None:
            bankName = self.ui.bankList.currentItem().text()
            self.ui.bankName.setText(bankName)
            for q in self.controller.getQuestionList(bankName, 10):
                self.ui.questionList.addItem(MyListWidgetItem(q.id, q.text.split("\n")[0], self.ui.questionList))
        # self.ui.questionList.setCurrentItem(self.ui.questionList.item(0))
        self.ui.stackedPages.setCurrentWidget(self.ui.editBankPage)

    def goToEditQuestionPage(self):
        self.ui.questionType.setCurrentIndex(0)
        self.ui.stackedAnswer.setCurrentIndex(0)
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
        result = self.controller.endExam()
        self.ui.questionRightNum.setText(str(result.numOfCorrect))
        self.ui.questionWrongNum.setText(str(result.numOfQ - result.numOfCorrect))
        self.ui.questionShowNum.setText(str(result.numOfPeek))
        self.ui.stackedPages.setCurrentWidget(self.ui.resultPage)

    def setController(self, controller):
        self.controller = controller

    @unused
    def deleteBank(self):
        if self.ui.bankList.currentItem() is None:
            # QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No bank selected!")
            messageBox = QtWidgets.QMessageBox()
            messageBox.setWindowTitle("錯誤訊息")
            messageBox.setText("No bank selected!")
            messageBox.exec_()
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
        if self.ui.bankList.currentItem() is None:
            self.ui.bankName.setText("請輸入題庫名稱")
            self.ui.bankName.setFocus()
            self.ui.bankName.setStyleSheet("color: red")
            return
        self.ui.questionText.setPlainText("")
        self.ui.questionList.setCurrentItem(None)
        self.goToEditQuestionPage()

    def saveQuestion(self):
        bankName = self.ui.bankList.currentItem().text()
        type = self.ui.questionType.currentData()
        question = self.ui.questionText.toPlainText()
        answer = None
        if not question.strip():
            self.ui.questionText.setPlainText("題目不能為空白!")
            self.ui.questionText.setFocus()
            self.ui.questionText.setStyleSheet("color: red")
            return
        if type == QuestionType.CHOICE or type == QuestionType.MULTIPLECHOICE:
            answer = []
            options = []
            for i in self.radioButtons:
                options.append(i.text())
                answer.append(i.isChecked())
            if answer.count(True) == 0:
                self.ui.newOption.setText("請選擇答案!")
                self.ui.newOption.setStyleSheet("color: red")
                return
            question = {"question": question, "options": options}
        elif type == QuestionType.FILL:
            answer = self.ui.shortAnswer_1.toPlainText()
            if not answer.strip():
                self.ui.shortAnswer_1.setPlainText("答案不能為空白!")
                self.ui.shortAnswer_1.setFocus()
                self.ui.shortAnswer_1.setStyleSheet("color: red")
                return
        try:
            self.controller.addQuestion(bankName, type, str(question), str(answer))
        except Exception as e:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", str(e))
        self.goToEditBankPage()

    def changeQuestionType(self):
        type = self.ui.questionType.currentData()
        if type == QuestionType.CHOICE:
            self.ui.stackedAnswer.setCurrentWidget(self.ui.choice)
            for radio in self.radioButtons:
                radio.setChecked(False)
                radio.setAutoExclusive(True)
        elif type == QuestionType.MULTIPLECHOICE:
            self.ui.stackedAnswer.setCurrentWidget(self.ui.choice)
            for radio in self.radioButtons:
                radio.setAutoExclusive(False)
        elif type == QuestionType.FILL:
            self.ui.stackedAnswer.setCurrentWidget(self.ui.shortAnswer)

    def addOption(self):
        text = self.ui.newOption.text()
        if text == "":
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "請輸入選項")
            return
        button = QtWidgets.QRadioButton(text)
        self.radioButtons.append(button)
        self.ui.choice.layout().insertWidget(self.ui.choice.layout().count() - 1, button)
        self.ui.newOption.setText("")

    def enterExam(self):
        if self.ui.bankList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No bank selected!")
            return
        bankName = self.ui.bankList.currentItem().text()
        questionNum = self.controller.enterExam(bankName)
        if questionNum == 0:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "題庫中沒有題目!")
            return
        self.ui.bankName_2.setText(bankName)
        self.ui.questionNum.setText(str(questionNum))
        self.ui.examNum.setMaximum(questionNum)
        self.ui.examNum.setMinimum(1)
        self.ui.examNum.setValue(10)
        self.goToEnterExamPage()

    def beginExam(self):
        bankName = self.ui.bankName_2.text()
        examNum = int(self.ui.examNum.text())
        self.controller.beginExam(bankName, examNum)
        self.ui.stackedPages.setCurrentWidget(self.ui.examPage)
        self.nextQuestion()

    def nextQuestion(self):
        question, idx = self.controller.getNextQuestion()
        if idx == int(self.ui.examNum.text()) - 1:
            self.ui.nextQuestionButton.setText("結束測驗")
        if idx == -1:
            self.goToResultPage()
            self.ui.nextQuestionButton.setText("下一題")
            return
        self.ui.currentNum.setText(str(idx + 1))
        self.ui.examShortAnswer_1.setPlainText("")
        self.ui.examShortAnswer_1.setStyleSheet("color: white")
        self.ui.examShortAnswer_1.setFocus()
        self.ui.examShortAnswer_1.setEnabled(True)
        self.ui.checkAnswerButton.setEnabled(True)
        # TODO: SETUP QUESTION!

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
