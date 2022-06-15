import sys
from PyQt5 import QtWidgets
from Model.Model import Model
from Model.question_type import QuestionType
from Model.question_factory import QuestionFactory, ShortAnswerFactory, ChoiceFactory, MultipleChoiceFactory
from View import View
from Controller.controller import Controller


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

        self.view = View()
        self.view.show()
        self.view.setController(self.controller)


if __name__ == "__main__":
    app = App(sys.argv)
    sys.exit(app.exec_())
