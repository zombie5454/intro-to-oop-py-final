from PyQt5 import QtWidgets, QtCore
from UI.QtUI import Ui_Widget
from Model.question_type import QuestionType
from Model.question import ChoiceOption
from typing import Callable, List
from .MyWidgets import MyListWidgetItem, MyRadioButton
from .Delegate import Delegate
from Controller.controller import Controller


def unused(func: Callable) -> Callable:
    return func


class View(QtWidgets.QWidget):
    def __init__(self):
        super(View, self).__init__()

        # attributes
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.darkMode: bool = False
        self.radioButtons: List[MyRadioButton] = []
        self.question = None
        self.delegate = Delegate()
        self.toggleStylesheet()

        # homePage
        self.ui.enterExamButton.clicked.connect(self.enterExam)
        self.ui.toggleModeButton.clicked.connect(self.toggleStylesheet)
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
        self.ui.bankName.textChanged.connect(lambda: self.ui.bankName.setStyleSheet(self.defaultColor))

        # editQuestionPage
        self.ui.backButton.clicked.connect(self.goToEditBankPage)
        self.ui.saveQuestionButton.clicked.connect(self.saveQuestion)
        self.ui.questionType.currentIndexChanged.connect(self.changeQuestionType)
        self.ui.addOptionButton.clicked.connect(self.addOption)
        self.ui.newOption.returnPressed.connect(self.addOption)
        self.ui.questionText.textChanged.connect(lambda: self.ui.questionText.setStyleSheet(self.defaultColor))
        self.ui.newOption.textChanged.connect(lambda: self.ui.newOption.setStyleSheet(self.defaultColor))
        self.ui.shortAnswerSheet.textChanged.connect(lambda: self.ui.shortAnswerSheet.setStyleSheet(self.defaultColor))

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
        self.ui.showAnswerButton.setVisible(False)

        # init MyComboBax
        self.ui.questionType.addItem("單選", QuestionType.CHOICE)
        self.ui.questionType.addItem("多選", QuestionType.MULTIPLECHOICE)
        self.ui.questionType.addItem("填空", QuestionType.FILL)

        # initialize
        self.goHome()

    def setController(self, controller: Controller):
        self.delegate.setController(controller)

    def toggleStylesheet(self):
        if self.darkMode:
            file = QtCore.QFile("./UI/light.qss")
            self.defaultColor = "color: black"
        else:
            file = QtCore.QFile("./UI/dark.qss")
            self.defaultColor = "color: white"
        self.darkMode = not self.darkMode
        file.open(QtCore.QFile.ReadOnly | QtCore.QFile.Text)
        stream = QtCore.QTextStream(file)
        self.setStyleSheet(stream.readAll())

    def goHome(self):
        self.ui.bankList.clear()
        for bank in self.delegate.getBanks():
            self.ui.bankList.addItem(MyListWidgetItem(bank.name, bank.name, self.ui.bankList))
        # self.ui.bankList.setCurrentItem(self.ui.bankList.item(0))
        self.ui.stackedPages.setCurrentWidget(self.ui.homePage)

    def goToEditBankPage(self):
        self.ui.questionList.clear()
        if self.ui.bankList.currentItem() is not None:
            bankName = self.ui.bankList.currentItem().text()
            self.ui.bankName.setText(bankName)
            for q in self.delegate.getQuestionList(bankName):
                self.ui.questionList.addItem(MyListWidgetItem(q.ID, q.question, self.ui.questionList))
        # self.ui.questionList.setCurrentItem(self.ui.questionList.item(0))
        self.ui.stackedPages.setCurrentWidget(self.ui.editBankPage)

    def goToEditQuestionPage(self):
        self.clearRadioButtons()
        self.ui.questionType.setCurrentIndex(0)
        self.ui.stackedAnswer.setCurrentIndex(0)
        self.ui.questionText.setPlainText("")
        self.ui.newOption.setText("")
        self.ui.shortAnswerSheet.setPlainText("")
        if self.ui.questionList.currentItem() is not None:
            question: MyListWidgetItem = self.ui.questionList.currentItem()
            self.ui.questionText.setPlainText(question.text())
            # self.ui.shortAnswerSheet.setPlainText(self.delegate.getQuestion(question.id))
        self.ui.stackedPages.setCurrentWidget(self.ui.editQuestionPage)

    def goToEnterExamPage(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.enterExamPage)

    def goToExamPage(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.examPage)

    def goToResultPage(self):
        result = self.delegate.endExam()
        self.ui.questionRightNum.setText(str(result.numOfCorrect))
        self.ui.questionWrongNum.setText(str(result.numOfQ - result.numOfCorrect))
        self.ui.questionShowNum.setText(str(result.numOfPeek))
        self.ui.stackedPages.setCurrentWidget(self.ui.resultPage)

    def clearRadioButtons(self):
        for radio in self.radioButtons:
            radio.parentWidget().layout().removeWidget(radio)
            radio.deleteLater()
        self.radioButtons = []

    @unused
    def deleteBank(self):
        if self.ui.bankList.currentItem() is None:
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
        if self.delegate.addBank(bankName):
            self.goHome()
        else:
            self.ui.bankName.setText("題庫名稱重複")
            self.ui.bankName.setFocus()

    @unused
    def deleteQuestion(self):
        if self.ui.questionList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No question selected!")
            return
        question: MyListWidgetItem = self.ui.questionList.currentItem()
        reply = QtWidgets.QMessageBox.question(
            None,
            "刪除題目",
            "確定要刪除題目「" + question.text() + "」嗎？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            bankName = self.ui.bankList.currentItem().text()
            self.delegate.deleteQuestion(bankName, question.id)
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
            answer = self.ui.shortAnswerSheet.toPlainText()
            if not answer.strip():
                self.ui.shortAnswerSheet.setPlainText("答案不能為空白!")
                self.ui.shortAnswerSheet.setFocus()
                self.ui.shortAnswerSheet.setStyleSheet("color: red")
                return
        if self.delegate.addQuestion(bankName, type, question, answer):
            self.goToEditBankPage()
        else:
            self.ui.questionText.setPlainText("儲存錯誤")
            self.ui.questionText.setFocus()

    def changeQuestionType(self):
        type = self.ui.questionType.currentData()
        if type == QuestionType.CHOICE:
            self.ui.stackedAnswer.setCurrentWidget(self.ui.choice)
            hasChecked = False
            for radio in self.radioButtons:
                radio.setAutoExclusive(True)
                if hasChecked:
                    radio.setChecked(False)
                if radio.isChecked():
                    hasChecked = True
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
        button = MyRadioButton(False, text)
        self.radioButtons.append(button)
        self.ui.radioButtonGroup.addWidget(button)
        self.ui.newOption.setText("")
        self.changeQuestionType()

    def enterExam(self):
        if self.ui.bankList.currentItem() is None:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No bank selected!")
            return
        bankName = self.ui.bankList.currentItem().text()
        questionNum = self.delegate.enterExam(bankName)
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
        self.delegate.beginExam(bankName, examNum)
        self.ui.stackedPages.setCurrentWidget(self.ui.examPage)
        self.nextQuestion()

    def nextQuestion(self):
        self.clearRadioButtons()
        self.ui.nextQuestionButton.setText("下一題")
        self.question, idx = self.delegate.getNextQuestion()
        if idx == int(self.ui.examNum.text()) - 1:
            self.ui.nextQuestionButton.setText("結束測驗")
        if idx == -1:
            self.goToResultPage()
            return
        self.ui.currentNum.setText(str(idx + 1))
        self.ui.examShortAnswerSheet.setPlainText("")
        self.ui.examShortAnswerSheet.setStyleSheet(self.defaultColor)
        self.ui.examShortAnswerSheet.setFocus()
        self.ui.examShortAnswerSheet.setEnabled(True)
        self.ui.checkAnswerButton.setEnabled(True)
        self.ui.examQuestionType.setText(self.question.type.value)
        self.ui.examQuestionText.setText(self.question.question)
        if self.question.type == QuestionType.CHOICE or self.question.type == QuestionType.MULTIPLECHOICE:
            self.ui.stackedExamAnswer.setCurrentWidget(self.ui.examChoice)
            choices: List[ChoiceOption] = self.question.choices
            for choice in choices:
                button = MyRadioButton(choice.is_true, choice.text)
                self.radioButtons.append(button)
                self.ui.examRadioButtonGroup.addWidget(button)
                button.setAutoExclusive(self.question.type == QuestionType.CHOICE)
        elif self.question.type == QuestionType.FILL:
            self.ui.stackedExamAnswer.setCurrentWidget(self.ui.examShortAnswer)

    @unused
    def showAnswer(self):
        ...

    def checkAnswer(self):
        if self.question.type == QuestionType.CHOICE or self.question.type == QuestionType.MULTIPLECHOICE:
            for radio in self.radioButtons:
                if radio.isChecked() and radio.is_true:
                    radio.setStyleSheet("color: green")
                elif not radio.isChecked() and not radio.is_true:
                    ...
                else:
                    radio.setStyleSheet("color: red")
        elif self.question.type == QuestionType.FILL:
            answer = self.ui.examShortAnswerSheet.toPlainText()
            self.ui.examShortAnswerSheet.setEnabled(False)
            self.ui.checkAnswerButton.setEnabled(False)
            if self.question.ans == answer:
                self.ui.examShortAnswerSheet.setStyleSheet("color: green")
            else:
                self.ui.examShortAnswerSheet.setStyleSheet("color: red")
                self.ui.examShortAnswerSheet.setPlainText(answer + "\n\n正確答案:\n" + self.question.ans)

    def testAgain(self):
        self.goToEnterExamPage()
