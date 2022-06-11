from typing import List
# Placeholders
from controller import QuestionBank, Question

# Takes in:
# - qCount number of questions in this exam
# - cCount: number of correctly answered questions
# - pCount: number of questions where user peeked at answer
class Result:
    def __init__(self, qCount: int, cCount: int, pCount: int) -> None:
        self._numOfQ = qCount
        self._numOfCorrect = cCount
        self._numOfPeek = pCount
    @property
    def numOfQ(self) -> int:
        return self._numOfQ
    @property
    def numOfCorrect(self) -> int:
        return self._numOfCorrect
    @property
    def numOfPeek(self) -> int:
        return self._numOfPeek
    

class Exam:
    def __init__(self, total: int, qB: QuestionBank) -> None:
        self._total = total
        self._correct = 0
        self._curQNum = 0
        self._peekAnsCount = 0
        self._qList: List[Question] = qB.getQuestionList(total)

    @property
    def qList(self) -> List[Question]:
        return self._qList
    
    # Returns None if index out of range
    def getNextQuestion(self) -> Question:
        try:
            q = self._qList.pop(0)
            self._curQNum += 1
            return q
        except IndexError:
            return None
    
    def getResult(self) -> Result:
        return Result(
            self._total,
            self._correct,
            self._peekAnsCount
        )
    
    # TODO: exam needs to be notified when the user
    # a) answered correctly,
    # b) peeked at an answer