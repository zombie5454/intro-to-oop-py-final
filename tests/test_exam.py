import unittest
from unittest.mock import Mock
from Controller.exam import Exam
from Model.question import ShortAnswer
from Model.question_factory import ShortAnswerFactory

class TestExamShortAnswerOnly(unittest.TestCase):
    def setUp(self) -> None:
        self.qNum = 5
        factory = ShortAnswerFactory()
        self.qList = [
            factory.createQuestion(str(i), str(i)) for i in range(self.qNum)
        ]
        self.bank = Mock()
        self.bank.getQuestionList.return_value = self.qList
        self.exam = Exam(self.qNum, self.bank)
    
    def test_getNextQuestion_success(self):
        for i in range(self.qNum):
            peekQ: ShortAnswer = self.exam.qList[0]
            q, idx = self.exam.getNextQuestion()
            q: ShortAnswer = q
            self.assertEqual(peekQ.question, q.question)
            self.assertEqual(peekQ.ans, q.ans)
            self.assertEqual(i, idx)
    
    def test_getNextQuestion_oob_err(self):
        for i in range(self.qNum):
            q, idx = self.exam.getNextQuestion()
        q, idx = self.exam.getNextQuestion()
        self.assertIsNone(q)
        self.assertEqual(idx, -1)
    
    # NOTE: since result tracking is done via controller, it isn't included here