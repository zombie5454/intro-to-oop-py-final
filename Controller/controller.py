from typing import List, Dict
from Model.Model import Model
from Model.question import Question
from Model.question_bank import QuestionBank
from Model.question_factory import QuestionFactory
from exam import Exam, Result

class Controller:
    def __init__(self, model: Model, qFactoryListDict: Dict[str, QuestionFactory]):
        self.__model: Model = model
        self.__qFactoryList: Dict[str, QuestionFactory] = qFactoryListDict
        self.__curExam: Exam = None
        self.__qBank: QuestionBank = None
    
    def getBanks(self) -> List[QuestionBank]:
        return self.__model.getBanks()
    
    def addBank(self, name: str) -> bool:
        return self.__model.addNewBank(name)
    
    def addNewQuestion(self, bankName: str, qType: str, qDes: str, qAns: str) -> bool:
        tarBank: QuestionBank = self.__model.getBank(bankName)
        if tarBank is None:
            return False
        q = self.__qFactoryList[qType].createQuestion(qDes, qAns)
        # TOOD: Model's README.md says addNewQuestion, but the code is currently addQuestion
        tarBank.addQuestion(q)
        return True
    
    def getQuestionList(self, bankName: str) -> List[Question]:
        tarBank = self.__model.getBank(bankName)
        if tarBank is None:
            return None
        return tarBank.getQuestionList()
    
    # Assumes target bank is valid (since we're selecting from dropdown menu)
    def getQuestionCap(self, name: str) -> int:
        # TODO: is it too slow?
        tarBank = self.__model.getBank(name)
        return len(tarBank.getQuestionList())

    # Assumes target bank is valid (since we're selecting from dropdown menu)
    def beginExam(self, bank: str, qNum: int) -> List[Question]:
        qBank = self.__model.getBank(bank)
        self.__curExam = Exam(qNum, qBank)
        return self.__curExam.qList
    
    # TODO: somehow there are two methods on fetching questions from exam...?
    def getNextExamQuestion(self) -> Question:
        return self.__curExam.getNextQuestion()
    
    def endExam(self) -> Result:
        r =  self.__curExam.getResult()
        del self.__curExam
        return r
    
    # TODO: no-op if there's no currently ongoing exam
    def sigOnUsrAct(self, correct: bool, peek: bool) -> None:
        if self.__curExam is None:
            pass
        if correct:
            self.__curExam.correct += 1
        if peek:
            self.__curExam.peekAnsCount += 1
