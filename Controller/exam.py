from typing import List, Tuple
import random
from Model.question import Question
from Model.question_bank import QuestionBank

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
        self.shuffleQuestionList()
    
    def shuffleQuestionList(self) -> None:
        random.shuffle(self.__qList)
        # Shuffles the answer
        # - short answer: no effect
        # - choice & multiple choice: ChoiceOption list is shuffled
        for q in self.__qList:
            random.shuffle(q.ans)

    # Returns None if index out of range
    def getNextQuestion(self) -> Tuple[Question, int]:
        try:
            q = self.__qList.pop(0)
            self.__curQNum += 1
            return q, self.__curQNum - 1
        except IndexError:
            return None, -1
    
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
