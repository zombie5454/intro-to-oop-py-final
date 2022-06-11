from typing import Tuple
from exam import Exam
from question_bank import QuestionBank

# Placeholders
class Question:
    def getCategory() -> str:
        pass

class Controller:
    def __init__(self):
        self._exam: Exam = Exam()
        self._qBank: QuestionBank = QuestionBank()

    def addNewCategory(self, name: str) -> bool:
        return self._qBank.addNewCategory(name)
    
    def addNewQuestion(self, q: Question) -> bool:
        if self._qBank.categoryIsExist(q.getCategory()):
            return False
        # Add the question
        return self._qBank.addNewQuestion(q)

    def beginExam(self, cat: str, qNum: int) -> Tuple[bool, int]:
        # Validate input
        if not self._qBank.categoryIsExist(cat):
            return False, -1
        if self._qBank.categoryQCount < qNum:
            return False, -1
        # Fetch the questions (shuffled-order)
        # TODO: