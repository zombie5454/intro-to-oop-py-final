from PyQt5 import QtWidgets, QtCore
from UI.QtUI import Ui_Widget
from Model.question_type import QuestionType
from Model.question import ChoiceOption, Question
from typing import List
from .MyWidgets import MyListWidgetItem, MyRadioButton
from .Delegate import Delegate
from .Util import unused, MyTimer
from .ColorTheme import ColorTheme, Theme
from Controller.controller import Controller


class View(QtWidgets.QWidget):
    def __init__(self):
        super(View, self).__init__()

        # attributes
        self.ui = Ui_Widget()
        self.ui.setupUi(self)
        self.theme = ColorTheme(Theme.LIGHT)
        self.radioButtons: List[MyRadioButton] = []
        self.isAddingBank = False
        self.isAddingQuestion = False
        self.bankTimer = MyTimer()
        self.questionTimer = MyTimer()
        self.question = None
        self.delegate = Delegate()
        self.toggleStylesheet()

        # homePage
        self.ui.enterExamButton.clicked.connect(self.enterExam)
        self.ui.toggleModeButton.clicked.connect(self.toggleStylesheet)
        self.ui.bankList.itemDoubleClicked.connect(self.editBank)
        self.ui.bankList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.bankList.customContextMenuRequested.connect(self.showBankMenu)
        self.ui.deleteBankButton.clicked.connect(self.deleteBank)
        self.ui.deleteBankButton.setStyleSheet(f"color: {self.theme.theme.error_color}")
        self.ui.editBankButton.clicked.connect(self.editBank)
        self.ui.addBankButton.clicked.connect(self.addBank)

        # editBankPage
        self.ui.homeButton.clicked.connect(self.goHome)
        self.ui.bankSaveButton.clicked.connect(self.saveBank)
        self.ui.questionList.itemDoubleClicked.connect(self.editQuestion)
        self.ui.questionList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.questionList.customContextMenuRequested.connect(self.showQuestionMenu)
        self.ui.deleteQuestionButton.clicked.connect(self.deleteQuestion)
        self.ui.deleteQuestionButton.setStyleSheet(f"color: {self.theme.theme.error_color}")
        self.ui.editQuestionButton.clicked.connect(self.editQuestion)
        self.ui.addQuestionButton.clicked.connect(self.addQuestion)
        self.ui.bankName.textChanged.connect(lambda: self.ui.bankName.setStyleSheet(f"color: {self.theme.theme.text_color}"))

        # editQuestionPage
        self.ui.backButton.clicked.connect(self.goToEditBankPage)
        self.ui.saveQuestionButton.clicked.connect(self.saveQuestion)
        self.ui.questionType.currentIndexChanged.connect(self.changeQuestionType)
        self.ui.addOptionButton.clicked.connect(self.addOption)
        self.ui.newOption.returnPressed.connect(self.addOption)
        self.ui.questionText.textChanged.connect(lambda: self.ui.questionText.setStyleSheet(f"color: {self.theme.theme.text_color}"))
        self.ui.newOption.textChanged.connect(lambda: self.ui.newOption.setStyleSheet(f"color: {self.theme.theme.text_color}"))
        self.ui.shortAnswerSheet.textChanged.connect(lambda: self.ui.shortAnswerSheet.setStyleSheet(f"color: {self.theme.theme.text_color}"))

        # enterExamPage
        self.ui.homeButton_2.clicked.connect(self.goHome)
        self.ui.beginExamButton.clicked.connect(self.beginExam)

        # examPage
        self.ui.exitExamButton.clicked.connect(self.exitExam)
        self.ui.nextQuestionButton.clicked.connect(self.nextQuestion)
        self.ui.showAnswerButton.clicked.connect(self.showAnswer)
        self.ui.checkAnswerButton.clicked.connect(self.checkAnswer)

        # resultPage
        self.ui.homeButton_4.clicked.connect(self.goHome)
        self.ui.testAgainButton.clicked.connect(self.testAgain)

        # hide unsupported features
        self.ui.showAnswerButton.setVisible(False)

        # init MyComboBax
        self.ui.questionType.addItem("單選", QuestionType.CHOICE)
        self.ui.questionType.addItem("多選", QuestionType.MULTIPLECHOICE)
        self.ui.questionType.addItem("填空", QuestionType.FILL)

    def setController(self, controller: Controller):
        self.delegate.setController(controller)
        self.goHome()

    def toggleStylesheet(self):
        _translate = QtCore.QCoreApplication.translate
        self.ui.toggleModeButton.setText(_translate("Widget", self.theme.theme.button_text))
        self.theme.toggle_theme()
        self.setStyleSheet(self.theme.style)

    def goHome(self):
        self.ui.bankList.clear()
        for bank in self.delegate.getBanks():
            self.ui.bankList.addItem(MyListWidgetItem(bank.name, bank.name, self.ui.bankList))
        self.ui.bankList.setCurrentItem(None)
        self.ui.stackedPages.setCurrentWidget(self.ui.homePage)

    def goToEditBankPage(self):
        self.ui.questionList.clear()
        if not self.isAddingBank:
            item: MyListWidgetItem = self.ui.bankList.selectedItems()[0]
            self.ui.bankName.setText(item.key)
            for question in self.delegate.getQuestions(item.key):
                self.ui.questionList.addItem(MyListWidgetItem(question, question.question, self.ui.questionList))
        self.ui.stackedPages.setCurrentWidget(self.ui.editBankPage)

    def goToEditQuestionPage(self):
        self.clearRadioButtons()
        self.ui.newOption.setText("")
        if not self.isAddingQuestion:
            item: MyListWidgetItem = self.ui.questionList.selectedItems()[0]
            question: Question = item.key
            self.ui.questionText.setPlainText(question.question)
            if question.type == QuestionType.CHOICE or question.type == QuestionType.MULTIPLECHOICE:
                self.ui.stackedAnswer.setCurrentWidget(self.ui.choice)
                self.ui.questionType.setCurrentIndex(int(question.type == QuestionType.MULTIPLECHOICE))
                choices: List[ChoiceOption] = question.choices
                for choice in choices:
                    button = MyRadioButton(choice.is_true, choice.text)
                    self.radioButtons.append(button)
                    self.ui.radioButtonGroup.addWidget(button)
                    button.setChecked(choice.is_true)
                    button.setAutoExclusive(question.type == QuestionType.CHOICE)
            elif question.type == QuestionType.FILL:
                self.ui.stackedAnswer.setCurrentWidget(self.ui.shortAnswer)
                self.ui.questionType.setCurrentIndex(2)
                self.ui.shortAnswerSheet.setPlainText(question.ans)
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

    def showBankMenu(self, pos):
        menu = QtWidgets.QMenu()
        menu.addAction("編輯題庫", self.editBank)
        menu.addAction("刪除題庫", self.deleteBank)
        menu.exec_(self.ui.bankList.mapToGlobal(pos))

    def removeErrorMessage(self, widget: QtWidgets.QLabel):
        widget.setSizePolicy(QtWidgets.QSizePolicy.Ignored, QtWidgets.QSizePolicy.Ignored)
        widget.setText("")
        widget.setStyleSheet(f"color: {self.theme.theme.text_color}")

    def showErrorMessage(self, widget: QtWidgets.QLabel, message: str):
        widget.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        widget.setText(message)
        widget.setStyleSheet(f"color: {self.theme.theme.error_color}")

    def deleteBank(self):
        if len(self.ui.bankList.selectedItems()) == 0:
            self.showErrorMessage(self.ui.homeErrorMessage, "請先選擇題庫")
            self.bankTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.homeErrorMessage))
            return
        bank = self.ui.bankList.selectedItems()[0]
        reply = QtWidgets.QMessageBox.question(
            None,
            "刪除題庫",
            "確定要刪除題庫「" + bank.key + "」嗎？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            self.delegate.deleteBank(bank.key)
            self.goHome()

    def editBank(self):
        self.isAddingBank = False
        if len(self.ui.bankList.selectedItems()) == 0:
            self.showErrorMessage(self.ui.homeErrorMessage, "請先選擇題庫")
            self.bankTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.homeErrorMessage))
            return
        self.goToEditBankPage()

    def addBank(self):
        self.isAddingBank = True
        self.ui.bankName.setText("")
        self.goToEditBankPage()

    def saveBank(self):
        bankName = self.ui.bankName.text()
        if not bankName.strip():
            self.showErrorMessage(self.ui.editBankErrorMessage, "題庫名稱不可為空")
            self.bankTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.editBankErrorMessage))
            return
        res = False
        if self.isAddingBank:
            res = self.delegate.addBank(bankName)
        else:
            oldBankName = self.ui.bankList.currentItem().text()
            if oldBankName == bankName:
                self.showErrorMessage(self.ui.editBankErrorMessage, "題庫名稱與原本相同")
                self.bankTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.editBankErrorMessage))
                return
            res = self.delegate.editBank(oldBankName, bankName)
        if res:
            self.goHome()  # improve this
        else:
            self.showErrorMessage(self.ui.editBankErrorMessage, "題庫名稱已存在")
            self.bankTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.editBankErrorMessage))

    def showQuestionMenu(self, pos):
        menu = QtWidgets.QMenu()
        menu.addAction("編輯題目", self.editQuestion)
        menu.addAction("刪除題目", self.deleteQuestion)
        menu.exec_(self.ui.questionList.mapToGlobal(pos))

    def deleteQuestion(self):
        if len(self.ui.questionList.selectedItems()) == 0:
            QtWidgets.QMessageBox.critical(None, "錯誤訊息", "No question selected!")
            return
        question: MyListWidgetItem = self.ui.questionList.selectedItems()[0]
        reply = QtWidgets.QMessageBox.question(
            None,
            "刪除題目",
            "確定要刪除題目「" + question.text() + "」嗎？",
            QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No,
            QtWidgets.QMessageBox.No,
        )
        if reply == QtWidgets.QMessageBox.Yes:
            bankName = self.ui.bankList.selectedItems()[0].text()
            self.delegate.deleteQuestion(bankName, question.key.ID)
            self.goToEditBankPage()

    def editQuestion(self):
        self.isAddingQuestion = False
        if len(self.ui.questionList.selectedItems()) == 0:
            self.showErrorMessage(self.ui.editBankErrorMessage, "請先選擇題目")
            self.bankTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.editBankErrorMessage))
            return
        self.goToEditQuestionPage()

    def addQuestion(self):
        if len(self.ui.bankList.selectedItems()) == 0:
            self.showErrorMessage(self.ui.editBankErrorMessage, "請先輸入題庫名稱")
            self.bankTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.editBankErrorMessage))
            return
        self.isAddingQuestion = True
        self.ui.questionType.setCurrentIndex(0)
        self.ui.questionText.setPlainText("")
        self.ui.stackedAnswer.setCurrentIndex(0)
        self.ui.shortAnswerSheet.setPlainText("")
        self.goToEditQuestionPage()

    def saveQuestion(self):
        bankName = self.ui.bankName.text()
        type = self.ui.questionType.currentData()
        question = self.ui.questionText.toPlainText()
        answer = None
        if not question.strip():
            self.showErrorMessage(self.ui.editQuestionErrorMessage, "題目不可為空")
            self.questionTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.editQuestionErrorMessage))
            return
        if type == QuestionType.CHOICE or type == QuestionType.MULTIPLECHOICE:
            answer = []
            options = []
            for i in self.radioButtons:
                options.append(i.text())
                answer.append(i.isChecked())
            if answer.count(True) == 0:
                self.showErrorMessage(self.ui.editQuestionErrorMessage, "請至少選擇一個答案")
                self.questionTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.editQuestionErrorMessage))
                return
            question = {"question": question, "options": options}
            question, answer = str(question), str(answer)
        elif type == QuestionType.FILL:
            answer = self.ui.shortAnswerSheet.toPlainText()
            if not answer.strip():
                self.showErrorMessage(self.ui.editQuestionErrorMessage, "答案不可為空")
                self.questionTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.editQuestionErrorMessage))
                return
        res = False
        if self.isAddingQuestion:
            res = self.delegate.addQuestion(bankName, type, question, answer)
        else:
            item: MyListWidgetItem = self.ui.questionList.selectedItems()[0]
            res = self.delegate.editQuestion(bankName, item.key.ID, type, question, answer)
        if res:
            self.editBank()
        else:
            self.showErrorMessage(self.ui.editQuestionErrorMessage, "儲存錯誤")
            self.questionTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.editQuestionErrorMessage))

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
        if not text.strip():
            self.showErrorMessage(self.ui.editQuestionErrorMessage, "選項不可為空")
            self.questionTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.editQuestionErrorMessage))
            return
        button = MyRadioButton(False, text)
        self.radioButtons.append(button)
        self.ui.radioButtonGroup.addWidget(button)
        self.ui.newOption.setText("")
        self.changeQuestionType()

    def enterExam(self):
        if len(self.ui.bankList.selectedItems()) == 0:
            self.showErrorMessage(self.ui.homeErrorMessage, "請先輸入題庫名稱")
            self.bankTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.homeErrorMessage))
            return
        bankName = self.ui.bankList.currentItem().text()
        questionNum = self.delegate.enterExam(bankName)
        if questionNum == 0:
            self.showErrorMessage(self.ui.homeErrorMessage, "題庫為空")
            self.bankTimer.singleShot(1000, lambda: self.removeErrorMessage(self.ui.homeErrorMessage))
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

    def exitExam(self):
        self.delegate.endExam()
        self.goHome()

    def nextQuestion(self):
        self.ui.nextQuestionButton.setEnabled(False)
        self.ui.checkAnswerButton.setEnabled(True)
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
        self.ui.examShortAnswerSheet.setStyleSheet(f"color: {self.theme.theme.text_color}")
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
        correct = True
        self.ui.checkAnswerButton.setEnabled(False)
        self.ui.nextQuestionButton.setEnabled(True)
        if self.question.type == QuestionType.CHOICE or self.question.type == QuestionType.MULTIPLECHOICE:
            for radio in self.radioButtons:
                if radio.isChecked() and radio.is_true:
                    radio.setStyleSheet(f"color: {self.theme.theme.success_color}")
                elif not radio.isChecked() and not radio.is_true:
                    ...
                else:
                    correct = False
                    radio.setStyleSheet(f"color: {self.theme.theme.error_color}")
        elif self.question.type == QuestionType.FILL:
            answer = self.ui.examShortAnswerSheet.toPlainText()
            self.ui.examShortAnswerSheet.setEnabled(False)
            self.ui.checkAnswerButton.setEnabled(False)
            if self.question.ans == answer:
                self.ui.examShortAnswerSheet.setStyleSheet(f"color: {self.theme.theme.success_color}")
            else:
                correct = False
                self.ui.examShortAnswerSheet.setStyleSheet(f"color: {self.theme.theme.error_color}")
                self.ui.examShortAnswerSheet.setPlainText(answer + "\n\n正確答案:\n" + self.question.ans)
        self.delegate.sendExamInfo(correct)

    def testAgain(self):
        self.goToEnterExamPage()
