from Model.question import Choice, ChoiceOption, MultipleChoice, ShortAnswer
from Model.question_factory import ShortAnswerFactory, MultipleChoiceFactory, ChoiceFactory, QuestionFactory
import unittest

class TestShortAnswerFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.qFactory = ShortAnswerFactory()
        self.qDes = "Q: What time is it?"
        self.qAns = "5:50PM"
        self.qShortAns = ShortAnswer(self.qDes, self.qAns)
    
    def test_create_success(self):
        qObj: ShortAnswer = self.qFactory.createQuestion(self.qDes, self.qAns)
        self.assertEqual(qObj.question, self.qDes)
        self.assertEqual(qObj.ans, self.qAns)


class TestChoiceFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.qFactory = ChoiceFactory()
        self.qDes = "Q: What time is it?"
        self.optList = [
            ChoiceOption("Opt 1", False),
            ChoiceOption("Opt 2", True),
            ChoiceOption("Opt 3", False),
        ]
        self.qAns = self.optList[1]
        self.q = Choice(self.qDes, self.qAns)
    
    def test_create_success(self):
        _optList = [opt.text for opt in self.optList]
        _optAns = [opt.is_true for opt in self.optList]
        qDesDict = {"question": self.qDes, "options": _optList}
        qAnsDict = _optAns
        qObj: Choice = self.qFactory.createQuestion(str(qDesDict), str(qAnsDict))
        self.assertEqual(qObj.question, self.qDes)
        for optTest, optBase in zip(qObj.choices, self.optList):
            self.assertEqual(optTest.is_true, optBase.is_true)
            self.assertEqual(optTest.text, optBase.text)


class TestMultipleChoiceFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.qFactory = MultipleChoiceFactory()
        self.qDes = "Q: Smth with multiple answers?"
        self.optList = [
            ChoiceOption("Opt 1", False),
            ChoiceOption("Opt 2", True),
            ChoiceOption("Opt 3", False),
            ChoiceOption("Opt 4", False),
            ChoiceOption("Opt 5", True),
        ]
        self.qAns = [self.optList[1], self.optList[4]]
        self.q = MultipleChoice(self.qDes, self.qAns)
    
    def test_create_success(self):
        _optList = [opt.text for opt in self.optList]
        _optAns = [opt.is_true for opt in self.optList]
        qDesDict = {"question": self.qDes, "options": _optList}
        qAnsDict = _optAns
        qObj: MultipleChoice = self.qFactory.createQuestion(str(qDesDict), str(qAnsDict))
        self.assertEqual(qObj.question, self.qDes)
        for optTest, optBase in zip(qObj.choices, self.optList):
            self.assertEqual(optTest.is_true, optBase.is_true)
            self.assertEqual(optTest.text, optBase.text)