from typing import List, Tuple
from Model.question import Question, QuestionType
from Model.question_bank import QuestionBank
from Controller.controller import Controller
from Controller.exam import Result


class Delegate(object):
    def __init__(self):
        self.controller = None
        self.questionList = {}

    def setController(self, controller: Controller) -> None:
        self.controller = controller

    def addBank(self, name: str) -> bool:
        return self.controller.addBank(name)

    def getBanks(self) -> List[QuestionBank]:
        return self.controller.getBanks()

    def editBank(self, name: str, newName: str) -> bool:
        return self.controller.editBankName(name, newName)

    def deleteBank(self, name: str) -> bool:
        return self.controller.deleteBank(name)

    def addQuestion(self, name: str, type: QuestionType, text: str, ans: str) -> bool:
        return self.controller.addNewQuestion(name, type, text, ans)

    def editQuestion(self, name: str, id: int, type: QuestionType, text: str, ans: str) -> bool:
        return self.controller.editQuestion(name, id, type, text, ans)

    def getQuestions(self, name: str) -> List[Question]:
        self.questionList[name] = {}
        for question in self.controller.getQuestionList(name):
            self.questionList[name][question.ID] = question
        return list(self.questionList[name].values())

    def getQuestion(self, name: str, id: int) -> Question:
        if self.questionList.get(name, None) is None:
            self.getQuestions(name)
        return self.questionList[name][id]

    def deleteQuestion(self, name: str, id: int) -> bool:
        return self.controller.deleteQuestion(name, id)

    def enterExam(self, name: str) -> int:
        return self.controller.getQuestionCap(name)

    def beginExam(self, name: str, num: int) -> None:
        self.controller.beginExam(name, num)

    def getNextQuestion(self) -> Tuple[Question, int]:
        return self.controller.getNextExamQuestion()

    def sendExamInfo(self, correct: bool) -> None:
        self.controller.sigOnUsrAct(correct, False)

    def endExam(self) -> Result:
        return self.controller.endExam()
