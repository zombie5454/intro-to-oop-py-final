from Model.question import ShortAnswer, Choice, MultipleChoice, ChoiceOption
import unittest

class TestShortAnswer(unittest.TestCase):
    def setUp(self):
        self.ans: str = "There is no answer!"
        self.q = ShortAnswer("Q: Example question!", self.ans)
        self.ansCHI: str = "正確答案，呵呵。"
        self.qCHI = ShortAnswer("Q: 中文問題？", self.ansCHI)

    def test_checkAnswer_success(self):
        res = self.q.checkAnswer(self.ans)
        self.assertTrue(res)
    
    def test_checkAnswer_successCHI(self):
        res = self.qCHI.checkAnswer(self.ansCHI)
        self.assertTrue(res)
    
    def test_checkAnswer_missingChar(self):
        res = self.q.checkAnswer(self.ans[:-1])
        self.assertFalse(res)

    def test_checkAnswer_missingCharCHI(self):
        res = self.qCHI.checkAnswer(self.ansCHI[:-1])
        self.assertFalse(res)
    
    def test_checkAnswer_caseMismatch(self):
        res = self.q.checkAnswer(self.ans.lower())
        self.assertTrue(res)
    
    def test_checkAnswer_caseMismatchCHI(self):
        res = self.qCHI.checkAnswer(self.ansCHI.lower())
        self.assertTrue(res)

class TestMultipleChoice(unittest.TestCase):
    def setUp(self):
        self.qOptList = [
            ChoiceOption("Opt 1", False),
            ChoiceOption("Opt 2", True),
            ChoiceOption("Opt 3", True),
            ChoiceOption("Opt 4", False)
        ]
        self.qAns = "1,2"
        self.qInvalidAns = "0,3"
        self.q = MultipleChoice("Q1: test?", self.qOptList)
    
    def test_checkAnswer_success_ReturnTrue(self):
        res = self.q.checkAnswer(self.qAns)
        self.assertTrue(res)
    
    def test_checkAnswer_invalid_ReturnFalse(self):
        res = self.q.checkAnswer(self.qInvalidAns)
        self.assertFalse(res)

class TestChoice(unittest.TestCase):
    def setUp(self):
        self.qOptList = [
            ChoiceOption("Opt 1", False),
            ChoiceOption("Opt 2", True),
            ChoiceOption("Opt 3", False)
        ]
        self.qAns = "1"
        self.qInvalidAns = "2"
        self.q = Choice("Q1: test?", self.qOptList)
    
    def test_checkAnswer_success_ReturnTrue(self):
        res = self.q.checkAnswer(self.qAns)
        self.assertTrue(res)
    
    def test_checkAnswer_invalid_ReturnFalse(self):
        res = self.q.checkAnswer(self.qInvalidAns)
        self.assertFalse(res)