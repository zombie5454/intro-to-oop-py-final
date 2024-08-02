import sys
from PyQt5 import QtWidgets
from Model.Model import Model
from Model.question_type import QuestionType
from Model.question_factory import ShortAnswerFactory, ChoiceFactory, MultipleChoiceFactory
from View.ViewQt_EN import View as View_En      #for English version
from View.ViewQt import View as View_TC         #for Chinese version
from Controller.controller import Controller

class App(QtWidgets.QApplication):
    def __init__(self, args):
        super().__init__(args)

        self.model = Model(path)  # pass in directory path of question banks to constructor

        self.qFactoryDict = {
            QuestionType.FILL: ShortAnswerFactory(),
            QuestionType.CHOICE: ChoiceFactory(),
            QuestionType.MULTIPLECHOICE: MultipleChoiceFactory(),
        }

        self.controller = Controller(self.model, self.qFactoryDict)

        self.view = View(self.controller)
        self.view.setWindowTitle("Question Bank")
        self.view.show()

View = View_TC
path = "./a"

if __name__ == "__main__":  
    for i, arg in enumerate(sys.argv):
        if arg == '-l' and sys.argv[i+1].upper() == "EN":
            View = View_En
            i+=1
        elif arg == '-p' and sys.argv[i+1]:
            path = sys.argv[i+1]
            i+=1

    app = App(sys.argv)
    sys.exit(app.exec_())
