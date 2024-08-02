import sys
from PyQt5 import QtWidgets
from Model.Model import Model
from Model.question_type import QuestionType
from Model.question_factory import ShortAnswerFactory, ChoiceFactory, MultipleChoiceFactory
from View.ViewQt_EN import View as View_En      #for English version
from View.ViewQt import View as View_TC         #for Chinese version
from Controller.controller import Controller

View = View_TC
class App(QtWidgets.QApplication):
    def __init__(self, args):
        super().__init__(args)

        self.model = Model("./a")  # pass in directory path of question banks to constructor

        self.qFactoryDict = {
            QuestionType.FILL: ShortAnswerFactory(),
            QuestionType.CHOICE: ChoiceFactory(),
            QuestionType.MULTIPLECHOICE: MultipleChoiceFactory(),
        }

        self.controller = Controller(self.model, self.qFactoryDict)

        self.view = View(self.controller)
        self.view.setWindowTitle("Question Bank")
        self.view.show()


if __name__ == "__main__":  
    for i, arg in enumerate(sys.argv):
        if arg == '-l' and sys.argv[i+1].upper() == "EN":
            View = View_En

    app = App(sys.argv)
    sys.exit(app.exec_())
