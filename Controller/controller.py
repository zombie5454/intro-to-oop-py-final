from typing import List
from exam import Exam, Result

# Placeholder
class Question:
    pass
class QuestionBank:
    def getName() -> str:
        pass
    def addQuestion(q: Question) -> bool:
        pass
    def getQuestionList() -> List[Question]:
        pass
class Model:
    def getBank(self, name: str) -> QuestionBank:
        pass
    def getBanks(self) -> List[QuestionBank]:
        pass
    def addNewBank(self, name: str) -> bool:
        pass

class Controller:
    def __init__(self, model: Model):
        self._curExam: Exam = None
        self._qBank: QuestionBank = None
        self._model: Model = model
    
    # TODO: may need to return object list instead
    def getBanks(self) -> List[str]:
        return self._model.getBanks()
    
    def addBank(self, name: str) -> bool:
        bankList = self._model.getBanks()
        for bank in bankList:
            if bank.name == name:
                return False
        self._model.addNewBank(name)
        return True
    
    def addNewQuestion(self, bankName: str, qType: str, qDes: str, qAns: str) -> bool:
        tarBank: QuestionBank = self._model.getBank(bankName)
        if tarBank is None:
            return False
        # TODO: pass in clean question
        tarBank.addQuestion(...)
    
    def getQuestionList(self, bankName: str) -> List[Question]:
        tarBank = self._model.getBank(bankName)
        if tarBank is None:
            return None
        return tarBank.getQuestionList()
    
    # Assumes target bank is valid (since we're selecting from dropdown menu)
    def getQuestionCap(self, name: str) -> int:
        # TODO: is it too slow?
        tarBank = self._model.getBank(name)
        return len(tarBank.getQuestionList())

    # Assumes target bank is valid (since we're selecting from dropdown menu)
    def beginExam(self, bank: str, qNum: int) -> List[Question]:
        qBank = self._model.getBank(bank)
        self._curExam = Exam(qNum, qBank)
        return self._curExam.qList
    
    # TODO: somehow there are two methods on fetching questions from exam...?
    def getNextExamQuestion(self) -> Question:
        return self._curExam.getNextQuestion()
    
    def endExam(self) -> Result:
        r =  self._curExam.getResult()
        del self._curExam
        return r