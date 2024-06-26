from PyQt5 import QtWidgets, QtCore, QtGui
from typing import List
from UI.QtUI import Ui_Widget
from Model.question_type import QuestionType
from Model.question import ChoiceOption, Question
from Controller.controller import Controller
from .Utils import export_data, save_data
from .MyWidgets import QuestionListWidgetItem, BankListWidgetItem, MyRadioButton, MyTimer
from .ColorTheme import ColorTheme, Theme


class View(QtWidgets.QWidget):
    def __init__(self, controller: Controller):
        super(View, self).__init__()

        # attributes
        self.ui: Ui_Widget = Ui_Widget()
        self.theme: ColorTheme = ColorTheme(Theme.LIGHT)
        self.radioButtons: List[MyRadioButton] = []
        self.isAddingBank: bool = False
        self.isAddingQuestion: bool = False
        self.bankTimer: MyTimer = MyTimer()
        self.questionTimer: MyTimer = MyTimer()
        self.examTimer: MyTimer = MyTimer()
        self.showAnswerNum: int = 0
        self.question: Question = None
        self.controller: Controller = None

        # set up
        self.ui.setupUi(self, EN=True)      # set UI to English version
        self.setController(controller)
        self.toggleStylesheet()

        # homePage
        self.ui.enterExamButton.clicked.connect(self.enterExam)
        self.ui.toggleModeButton.clicked.connect(self.toggleStylesheet)
        self.ui.importBankButton.clicked.connect(self.importBank)
        self.ui.bankList.setMouseTracking(True)
        self.ui.bankList.itemDoubleClicked.connect(self.enterExam)
        self.ui.bankList.itemEntered.connect(lambda: self.ui.bankList.setCursor(QtCore.Qt.PointingHandCursor))
        self.ui.bankList.viewportEntered.connect(lambda: self.ui.bankList.setCursor(QtCore.Qt.ArrowCursor))
        self.ui.bankList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.bankList.customContextMenuRequested.connect(self.showBankMenu)
        self.ui.homeErrorMessage.setVisible(False)
        self.ui.deleteBankButton.clicked.connect(self.deleteBank)
        self.ui.editBankButton.clicked.connect(self.editBank)
        self.ui.addBankButton.clicked.connect(self.addBank)

        # editBankPage
        self.ui.homeButton.clicked.connect(self.goHome)
        self.ui.bankName.returnPressed.connect(lambda: self.saveBank(self.ui.bankName.text()))
        self.ui.bankSaveButton.clicked.connect(lambda: self.saveBank(self.ui.bankName.text()))
        self.ui.questionList.setMouseTracking(True)
        self.ui.questionList.itemDoubleClicked.connect(self.editQuestion)
        self.ui.questionList.itemEntered.connect(lambda: self.ui.questionList.setCursor(QtCore.Qt.PointingHandCursor))
        self.ui.questionList.viewportEntered.connect(lambda: self.ui.questionList.setCursor(QtCore.Qt.ArrowCursor))
        self.ui.questionList.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.ui.questionList.customContextMenuRequested.connect(self.showQuestionMenu)
        self.ui.editBankErrorMessage.setVisible(False)
        self.ui.deleteQuestionButton.clicked.connect(self.deleteQuestion)
        self.ui.editQuestionButton.clicked.connect(self.editQuestion)
        self.ui.addQuestionButton.clicked.connect(self.addQuestion)
        self.ui.bankName.textChanged.connect(lambda: self.ui.bankName.setStyleSheet("color: " + self.theme.theme.text_color))

        # editQuestionPage
        self.ui.backButton.clicked.connect(self.goToEditBankPage)
        self.ui.saveQuestionButton.clicked.connect(self.saveQuestion)
        self.ui.questionType.currentIndexChanged.connect(self.changeQuestionType)
        self.ui.questionText.textChanged.connect(lambda: self.ui.questionText.setStyleSheet("color: " + self.theme.theme.text_color))
        self.ui.addOptionButton.clicked.connect(self.addOption)
        self.ui.newOption.returnPressed.connect(self.addOption)
        self.ui.newOption.textChanged.connect(lambda: self.ui.newOption.setStyleSheet("color: " + self.theme.theme.text_color))
        self.ui.shortAnswerSheet.textChanged.connect(lambda: self.ui.shortAnswerSheet.setStyleSheet("color: " + self.theme.theme.text_color))
        self.ui.editQuestionErrorMessage.setVisible(False)

        # enterExamPage
        self.ui.homeButton_2.clicked.connect(self.goHome)
        self.ui.beginExamButton.clicked.connect(self.beginExam)

        # examPage
        self.ui.exitExamButton.clicked.connect(self.exitExam)
        self.ui.nextQuestionButton.clicked.connect(self.nextQuestion)
        self.ui.showAnswerButton.clicked.connect(self.showAnswer)
        self.ui.checkAnswerButton.clicked.connect(self.checkAnswer)
        self.ui.examMessage.setVisible(False)

        # resultPage
        self.ui.homeButton_4.clicked.connect(self.goHome)
        self.ui.testAgainButton.clicked.connect(self.testAgain)

        # init MyComboBax
        self.ui.questionType.addItem("MC", QuestionType.CHOICE)
        self.ui.questionType.addItem("MC (may be more than one answer)", QuestionType.MULTIPLECHOICE)
        self.ui.questionType.addItem("Fill in the Blanks", QuestionType.FILL)

    def setController(self, controller: Controller):
        self.controller = controller
        self.goHome()

    def toggleStylesheet(self):
        _translate = QtCore.QCoreApplication.translate
        self.ui.toggleModeButton.setText(_translate("Widget", self.theme.theme.button_text_EN))
        self.theme.toggle_theme()
        self.setStyleSheet(self.theme.style)

    def importBank(self):
        fname = QtWidgets.QFileDialog.getOpenFileName(self, "Import file", "./", "JSON files (*.json)")
        try:
            save_data(self.controller, fname[0])
        except Exception as e:
            self.showMessage(self.ui.homeErrorMessage, "Import error " + str(e.__class__.__name__) + ": " + str(e), self.theme.theme.error_color)
            self.bankTimer.singleShot(10000, lambda: self.removeMessage(self.ui.homeErrorMessage))
        self.goHome()

    def exportBank(self):
        fname = QtWidgets.QFileDialog.getSaveFileName(self, "Export file", "./", "JSON files (*.json)")
        try:
            export_data(self.controller, self.ui.bankList.selectedItems(), fname[0])
        except Exception as e:
            self.showMessage(self.ui.homeErrorMessage, "Export error" + str(e.__class__.__name__) + ": " + str(e), self.theme.theme.error_color)
            self.bankTimer.singleShot(10000, lambda: self.removeMessage(self.ui.homeErrorMessage))
        self.goHome()

    def goHome(self):
        self.ui.bankList.clear()
        for bank in self.controller.getBanks():
            self.ui.bankList.addItem(BankListWidgetItem(bank, self.ui.bankList))
        self.ui.bankList.setCurrentItem(None)
        self.ui.stackedPages.setCurrentWidget(self.ui.homePage)

    def goToEditBankPage(self):
        self.ui.questionList.clear()
        if not self.isAddingBank:
            bank: BankListWidgetItem = self.ui.bankList.selectedItems()[0]
            self.ui.bankName.setText(bank.bankName)
            for question in self.controller.getQuestionList(bank.bankName):
                self.ui.questionList.addItem(QuestionListWidgetItem(question, self.ui.questionList))
        self.ui.stackedPages.setCurrentWidget(self.ui.editBankPage)

    def goToEditQuestionPage(self):
        self.clearRadioButtons()
        self.ui.newOption.setText("")
        if not self.isAddingQuestion:
            question: QuestionListWidgetItem = self.ui.questionList.selectedItems()[0]
            self.ui.questionText.setPlainText(question.questionText)
            if question.questionType == QuestionType.CHOICE or question.questionType == QuestionType.MULTIPLECHOICE:
                self.ui.stackedAnswer.setCurrentWidget(self.ui.choice)
                self.ui.questionType.setCurrentIndex(int(question.questionType == QuestionType.MULTIPLECHOICE))
                choices: List[ChoiceOption] = question.questionChoices
                for choice in choices:
                    button = MyRadioButton(choice.is_true, choice.text)
                    self.radioButtons.append(button)
                    self.ui.radioButtonGroup.addWidget(button)
                    button.setChecked(choice.is_true)
                    button.setAutoExclusive(question.type == QuestionType.CHOICE)
            elif question.type == QuestionType.FILL:
                self.ui.stackedAnswer.setCurrentWidget(self.ui.shortAnswer)
                self.ui.questionType.setCurrentIndex(2)
                self.ui.shortAnswerSheet.setPlainText(question.questionAns)
        self.ui.stackedPages.setCurrentWidget(self.ui.editQuestionPage)

    def goToEnterExamPage(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.enterExamPage)

    def goToExamPage(self):
        self.ui.stackedPages.setCurrentWidget(self.ui.examPage)

    def goToResultPage(self):
        result = self.controller.endExam()
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
        menu.addAction("Enter Exam", self.enterExam)
        menu.addAction("Add Question", self.addQuestion)
        menu.addAction("Edit Bank", self.editBank)
        menu.addAction("Export Bank", self.exportBank)
        menu.addAction("Delete Bank", self.deleteBank)
        menu.setStyleSheet(self.theme.style)
        menu.exec_(self.ui.bankList.mapToGlobal(pos))

    def removeMessage(self, widget: QtWidgets.QLabel):
        widget.setVisible(False)
        widget.setText("")
        widget.setStyleSheet("color: " + self.theme.theme.text_color)

    def showMessage(self, widget: QtWidgets.QLabel, message: str, color: str):
        widget.setVisible(True)
        widget.setText(message)
        widget.setStyleSheet("color: " + color)

    def showDeleteMessageBox(self, title: str, message: str) -> bool:
        messageBox = QtWidgets.QMessageBox()
        messageBox.setWindowTitle(title)
        messageBox.setText(message)
        messageBox.setStandardButtons(QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        messageBox.setDefaultButton(QtWidgets.QMessageBox.No)
        messageBox.button(QtWidgets.QMessageBox.Yes).setText("Confirm")
        messageBox.button(QtWidgets.QMessageBox.Yes).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        messageBox.button(QtWidgets.QMessageBox.No).setText("Cancel")
        messageBox.button(QtWidgets.QMessageBox.No).setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        # messageBox.setStyleSheet(self.theme.style)
        reply = messageBox.exec_()
        return reply == QtWidgets.QMessageBox.Yes

    def deleteBank(self):
        if len(self.ui.bankList.selectedItems()) == 0:
            self.showMessage(self.ui.homeErrorMessage, "Select a bank first", self.theme.theme.error_color)
            self.bankTimer.singleShot(1000, lambda: self.removeMessage(self.ui.homeErrorMessage))
            return
        bank: BankListWidgetItem = self.ui.bankList.selectedItems()[0]
        reply = self.showDeleteMessageBox("Delete Bank", "Are you sure about deleting the bank '" + bank.bankName + "' ?")
        if reply:
            self.controller.deleteBank(bank.bankName)
            self.goHome()

    def editBank(self):
        self.isAddingBank = False
        if len(self.ui.bankList.selectedItems()) == 0:
            self.showMessage(self.ui.homeErrorMessage, "Select a bank first", self.theme.theme.error_color)
            self.bankTimer.singleShot(1000, lambda: self.removeMessage(self.ui.homeErrorMessage))
            return
        self.goToEditBankPage()

    def addBank(self):
        self.isAddingBank = True
        self.ui.bankName.setText("")
        self.goToEditBankPage()

    def saveBank(self, bankName: str):
        if not bankName.strip():
            self.showMessage(self.ui.editBankErrorMessage, "Bank name can't be empty", self.theme.theme.error_color)
            self.bankTimer.singleShot(1000, lambda: self.removeMessage(self.ui.editBankErrorMessage))
            return
        res = False
        if self.isAddingBank:
            res = self.controller.addBank(bankName)
            self.isAddingBank = False
        else:
            oldBank: BankListWidgetItem = self.ui.bankList.selectedItems()[0]
            oldBankName = oldBank.bankName
            if oldBankName == bankName:
                self.showMessage(self.ui.editBankErrorMessage, "Please type a different bank name", self.theme.theme.error_color)
                self.bankTimer.singleShot(1000, lambda: self.removeMessage(self.ui.editBankErrorMessage))
                return
            res = self.controller.editBankName(oldBankName, bankName)
        if res:
            self.goHome()  # improve this
        else:
            self.showMessage(self.ui.editBankErrorMessage, "Bank name exists", self.theme.theme.error_color)
            self.bankTimer.singleShot(1000, lambda: self.removeMessage(self.ui.editBankErrorMessage))

    def showQuestionMenu(self, pos):
        menu = QtWidgets.QMenu()
        menu.addAction("Edit Question", self.editQuestion)
        menu.addAction("Delete Question", self.deleteQuestion)
        menu.setStyleSheet(self.theme.style)
        menu.exec_(self.ui.questionList.mapToGlobal(pos))

    def deleteQuestion(self):
        if len(self.ui.questionList.selectedItems()) == 0:
            self.showMessage(self.ui.editBankErrorMessage, "Select a question first", self.theme.theme.error_color)
            self.questionTimer.singleShot(1000, lambda: self.removeMessage(self.ui.editBankErrorMessage))
            return
        question: QuestionListWidgetItem = self.ui.questionList.selectedItems()[0]
        reply = self.showDeleteMessageBox("Delete Question", "Are you sure about deleting the question '" + question.questionText[:20] + "' ?")
        if reply:
            bank: BankListWidgetItem = self.ui.bankList.selectedItems()[0]
            self.controller.deleteQuestion(bank.bankName, question.id)
            self.goToEditBankPage()

    def editQuestion(self):
        self.isAddingQuestion = False
        if len(self.ui.questionList.selectedItems()) == 0:
            self.showMessage(self.ui.editBankErrorMessage, "Select a question first", self.theme.theme.error_color)
            self.bankTimer.singleShot(1000, lambda: self.removeMessage(self.ui.editBankErrorMessage))
            return
        self.goToEditQuestionPage()

    def addQuestion(self):
        self.isAddingBank = False
        if len(self.ui.bankList.selectedItems()) == 0:
            self.showMessage(self.ui.editBankErrorMessage, "Type a bank name first", self.theme.theme.error_color)
            self.bankTimer.singleShot(1000, lambda: self.removeMessage(self.ui.editBankErrorMessage))
            return
        self.isAddingQuestion = True
        self.ui.questionType.setCurrentIndex(0)
        self.ui.questionText.setPlainText("")
        self.ui.stackedAnswer.setCurrentIndex(0)
        self.ui.shortAnswerSheet.setPlainText("")
        self.goToEditQuestionPage()

    def saveQuestion(self):
        bankName = self.ui.bankName.text()
        questionType = self.ui.questionType.currentData()
        questionText = self.ui.questionText.toPlainText()
        questionAns = None
        if not questionText.strip():
            self.showMessage(self.ui.editQuestionErrorMessage, "Question can't be empty", self.theme.theme.error_color)
            self.questionTimer.singleShot(1000, lambda: self.removeMessage(self.ui.editQuestionErrorMessage))
            return
        if questionType == QuestionType.CHOICE or questionType == QuestionType.MULTIPLECHOICE:
            answer = []
            options = []
            for i in self.radioButtons:
                options.append(i.text())
                answer.append(i.isChecked())
            if answer.count(True) == 0:
                self.showMessage(self.ui.editQuestionErrorMessage, "Please select at least one option", self.theme.theme.error_color)
                self.questionTimer.singleShot(1000, lambda: self.removeMessage(self.ui.editQuestionErrorMessage))
                return
            questionText = {"question": questionText, "options": options}
            questionText, questionAns = str(questionText), str(answer)
        elif questionType == QuestionType.FILL:
            questionAns = self.ui.shortAnswerSheet.toPlainText()
            if not questionAns.strip():
                self.showMessage(self.ui.editQuestionErrorMessage, "Answer can't be empty", self.theme.theme.error_color)
                self.questionTimer.singleShot(1000, lambda: self.removeMessage(self.ui.editQuestionErrorMessage))
                return
        res = False
        if self.isAddingQuestion:
            res = self.controller.addNewQuestion(bankName, questionType, questionText, questionAns)
        else:
            question: QuestionListWidgetItem = self.ui.questionList.selectedItems()[0]
            res = self.controller.editQuestion(bankName, question.id, questionType, questionText, questionAns)
        if res:
            self.editBank()
        else:
            self.showMessage(self.ui.editQuestionErrorMessage, "Save error", self.theme.theme.error_color)
            self.questionTimer.singleShot(1000, lambda: self.removeMessage(self.ui.editQuestionErrorMessage))

    def changeQuestionType(self):
        questionType = self.ui.questionType.currentData()
        if questionType == QuestionType.CHOICE:
            self.ui.stackedAnswer.setCurrentWidget(self.ui.choice)
            hasChecked = False
            for radio in self.radioButtons:
                radio.setAutoExclusive(True)
                if hasChecked:
                    radio.setChecked(False)
                if radio.isChecked():
                    hasChecked = True
        elif questionType == QuestionType.MULTIPLECHOICE:
            self.ui.stackedAnswer.setCurrentWidget(self.ui.choice)
            for radio in self.radioButtons:
                radio.setAutoExclusive(False)
        elif questionType == QuestionType.FILL:
            self.ui.stackedAnswer.setCurrentWidget(self.ui.shortAnswer)

    def addOption(self):
        optionText = self.ui.newOption.text()
        if not optionText.strip():
            self.showMessage(self.ui.editQuestionErrorMessage, "Option can't be empty", self.theme.theme.error_color)
            self.questionTimer.singleShot(1000, lambda: self.removeMessage(self.ui.editQuestionErrorMessage))
            return
        button = MyRadioButton(False, optionText)
        self.radioButtons.append(button)
        self.ui.radioButtonGroup.addWidget(button)
        self.ui.newOption.setText("")
        self.changeQuestionType()

    def enterExam(self):
        if len(self.ui.bankList.selectedItems()) == 0:
            self.showMessage(self.ui.homeErrorMessage, "Type a bank name first", self.theme.theme.error_color)
            self.bankTimer.singleShot(1000, lambda: self.removeMessage(self.ui.homeErrorMessage))
            return
        bank: BankListWidgetItem = self.ui.bankList.selectedItems()[0]
        questionNum = self.controller.getQuestionCap(bank.bankName)
        if questionNum == 0:
            self.showMessage(self.ui.homeErrorMessage, "Bank is empty", self.theme.theme.error_color)
            self.bankTimer.singleShot(1000, lambda: self.removeMessage(self.ui.homeErrorMessage))
            return
        self.ui.bankName_2.setText(bank.bankName)
        self.ui.questionNum.setText(str(questionNum))
        self.ui.examNum.setRange(1, questionNum)
        self.ui.examNum.setValue(10)
        self.goToEnterExamPage()

    def beginExam(self):
        bankName = self.ui.bankName_2.text()
        examNum = int(self.ui.examNum.text())
        self.controller.beginExam(bankName, examNum)
        self.ui.stackedPages.setCurrentWidget(self.ui.examPage)
        self.nextQuestion()

    def exitExam(self):
        self.controller.endExam()
        self.goHome()

    def nextQuestion(self):
        self.showAnswerNum = 0
        self.ui.nextQuestionButton.setEnabled(False)
        self.ui.checkAnswerButton.setEnabled(True)
        self.removeMessage(self.ui.examMessage)
        self.clearRadioButtons()
        self.ui.nextQuestionButton.setText("next")
        self.question, idx = self.controller.getNextExamQuestion()
        if idx == int(self.ui.examNum.text()) - 1:
            self.ui.nextQuestionButton.setText("end")
        if idx == -1:
            self.goToResultPage()
            return
        self.ui.currentNum.setText(str(idx + 1))
        self.ui.examShortAnswerSheet.setPlainText("")
        self.ui.examShortAnswerSheet.setStyleSheet("color: " + self.theme.theme.text_color)
        self.ui.examShortAnswerSheet.setFocus()
        self.ui.examShortAnswerSheet.setEnabled(True)
        self.ui.checkAnswerButton.setEnabled(True)
        self.ui.examQuestionType.setText(self.question.type.value)
        questionText = self.question.question
        questionText = [q.replace("<", "&lt;").replace(">", "&gt;") for q in questionText.split("\n")]
        questionText = "<p>" + "</p><p>".join(questionText) + "</p>"
        self.ui.examQuestionText.setText(questionText)
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

    def showAnswer(self):
        self.showAnswerNum += 1
        correct = True
        if self.question.type == QuestionType.CHOICE or self.question.type == QuestionType.MULTIPLECHOICE:
            for radio in self.radioButtons:
                if radio.isChecked() != radio.is_true:
                    correct = False
                    break
        elif self.question.type == QuestionType.FILL:
            if self.ui.examShortAnswerSheet.toPlainText() != self.question.ans:
                correct = False
        if correct:
            self.showMessage(self.ui.examMessage, "Correct", self.theme.theme.success_color)
            self.examTimer.singleShot(1000, lambda: self.removeMessage(self.ui.examMessage))
        else:
            self.showMessage(self.ui.examMessage, "Wrong", self.theme.theme.error_color)
            self.examTimer.singleShot(1000, lambda: self.removeMessage(self.ui.examMessage))

    def checkAnswer(self):
        correct = True
        self.ui.checkAnswerButton.setEnabled(False)
        self.ui.nextQuestionButton.setEnabled(True)
        if self.question.type == QuestionType.CHOICE or self.question.type == QuestionType.MULTIPLECHOICE:
            for radio in self.radioButtons:
                if radio.isChecked() and radio.is_true:
                    radio.setStyleSheet("color: " + self.theme.theme.success_color)
                elif not radio.isChecked() and not radio.is_true:
                    ...
                else:
                    correct = False
                    radio.setStyleSheet("color: " + self.theme.theme.error_color)
        elif self.question.type == QuestionType.FILL:
            answer = self.ui.examShortAnswerSheet.toPlainText()
            self.ui.examShortAnswerSheet.setEnabled(False)
            self.ui.checkAnswerButton.setEnabled(False)
            if self.question.ans == answer:
                self.ui.examShortAnswerSheet.setStyleSheet("color: " + self.theme.theme.success_color)
            else:
                correct = False
                self.showMessage(self.ui.examMessage, "Correct Answer: " + self.question.ans, self.theme.theme.error_color)
        self.controller.sigOnUsrAct(correct, self.showAnswerNum)

    def testAgain(self):
        self.goToEnterExamPage()

    def keyPressEvent(self, a0: QtGui.QKeyEvent) -> None:
        if a0.matches(QtGui.QKeySequence.Delete):
            if self.ui.stackedPages.currentWidget() == self.ui.homePage:
                self.deleteBank()
            elif self.ui.stackedPages.currentWidget() == self.ui.editBankPage:
                self.deleteQuestion()
        elif a0.matches(QtGui.QKeySequence.Open):
            if self.ui.stackedPages.currentWidget() == self.ui.homePage:
                self.editBank()
            elif self.ui.stackedPages.currentWidget() == self.ui.editBankPage:
                self.editQuestion()
        elif a0.matches(QtGui.QKeySequence.New):
            if self.ui.stackedPages.currentWidget() == self.ui.homePage:
                self.addBank()
            elif self.ui.stackedPages.currentWidget() == self.ui.editBankPage:
                self.addQuestion()
        elif a0.matches(QtGui.QKeySequence.Save):
            if self.ui.stackedPages.currentWidget() == self.ui.editBankPage:
                self.saveBank(self.ui.bankName.text())
            elif self.ui.stackedPages.currentWidget() == self.ui.editQuestionPage:
                self.saveQuestion()
        elif a0.matches(QtGui.QKeySequence.SaveAs):
            if self.ui.stackedPages.currentWidget() == self.ui.homePage:
                self.exportBank()
        elif a0.matches(QtGui.QKeySequence.Forward):
            if self.ui.stackedPages.currentWidget() == self.ui.examPage:
                if self.ui.nextQuestionButton.isEnabled():
                    self.ui.nextQuestionButton.click()
        elif a0.matches(QtGui.QKeySequence.InsertParagraphSeparator):
            if self.ui.stackedPages.currentWidget() == self.ui.enterExamPage:
                self.beginExam()
        elif a0.matches(QtGui.QKeySequence.Cancel):
            if self.ui.stackedPages.currentWidget() == self.ui.editBankPage:
                self.goHome()
            elif self.ui.stackedPages.currentWidget() == self.ui.editQuestionPage:
                self.goToEditBankPage()
            elif self.ui.stackedPages.currentWidget() == self.ui.enterExamPage:
                self.goHome()
            elif self.ui.stackedPages.currentWidget() == self.ui.examPage:
                self.goToEnterExamPage()
            elif self.ui.stackedPages.currentWidget() == self.ui.resultPage:
                self.goHome()
        return super().keyPressEvent(a0)
