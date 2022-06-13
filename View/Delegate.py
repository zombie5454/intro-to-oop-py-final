from typing import List, Tuple
from Model.question import Question
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
        if(self.controller != None):
            return self.controller.addBank(name)

    def getBanks(self) -> List[QuestionBank]:
        if(self.controller != None):
            return self.controller.getBanks()

    def deleteBank(self, name: str) -> bool:
        if(self.controller != None):
            return self.controller.deleteBank(name)

    def addQuestion(self, name: str, type: str, text: str, ans: str) -> bool:
        if(self.controller != None):
            return self.controller.addNewQuestion(name, type, text, ans)

    def getQuestions(self, name: str) -> List[Question]:
        if(self.controller != None):
            self.questionList = {}
            for question in self.controller.getQuestionList(name):
                self.questionList[question.ID] = question
            return list(self.questionList.values())

    def getQuestion(self, id: int) -> Question:
        return self.questionList[id]

    def deleteQuestion(self, name: str, id: int) -> bool:
        if(self.controller != None):
            return self.controller.deleteQuestion(name, id)

    def enterExam(self, name: str) -> int:
        if(self.controller != None):
            return self.controller.getQuestionCap(name)

    def beginExam(self, name: str, num: int) -> None:
        if(self.controller != None):
            self.controller.beginExam(name, num)

    def getNextQuestion(self) -> Tuple[Question, int]:
        if(self.controller != None):
            return self.controller.getNextExamQuestion()

    def endExam(self) -> Result:
        if(self.controller != None):
            return self.controller.endExam()
