from typing import List
# Placeholders
from controller import QuestionBank, Question

# Takes in:
# - qCount number of questions in this exam
# - cCount: number of correctly answered questions
# - pCount: number of questions where user peeked at answer
class Result:
    def __init__(self, qCount: int, cCount: int, pCount: int) -> None:
        self.__numOfQ = qCount
        self.__numOfCorrect = cCount
        self.__numOfPeek = pCount
    @property
    def numOfQ(self) -> int:
        return self.__numOfQ
    @property
    def numOfCorrect(self) -> int:
        return self.__numOfCorrect
    @property
    def numOfPeek(self) -> int:
        return self.__numOfPeek
    

class Exam:
    def __init__(self, total: int, qB: QuestionBank) -> None:
        self.__total = total
        self.__correct = 0
        self.__curQNum = 0
        self.__peekAnsCount = 0
        self.__qList: List[Question] = qB.getQuestionList(total)

    # Returns None if index out of range
    def getNextQuestion(self) -> Question:
        try:
            q = self.__qList.pop(0)
            self.__curQNum += 1
            return q
        except IndexError:
            return None
    
    def getResult(self) -> Result:
        return Result(
            self.__total,
            self.__correct,
            self.__peekAnsCount
        )
    
    @property
    def qList(self) -> List[Question]:
        return self.__qList
    
    @property
    def correct(self) -> int:
        return self.__correct
    @correct.setter
    def correct(self, newValue: int) -> None:
        self.__correct = newValue

    @property
    def peekAnsCount(self) -> int:
        return self.__peekAnsCount
    @peekAnsCount.setter
    def peekAnsCount(self, newValue: int) -> None:
        self.__peekAnsCount = newValue
