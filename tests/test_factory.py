from Model.question import Choice, ChoiceOption, ShortAnswer
from Model.question_factory import ShortAnswerFactory, MultipleChoiceFactory, ChoiceFactory, QuestionFactory
from Model.question_type import QuestionType
import unittest

class TestShortAnswerFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.qFactory = ShortAnswerFactory()
        self.qDes = "Q: What time is it?"
        self.qAns = "5:50PM"
        self.qShortAns = ShortAnswer(self.qDes, self.qAns)
    
    def test_create_success(self):
        qDesDict = {"question": self.qDes}
        qAnsDict = self.qAns
        qObj: ShortAnswer = self.qFactory.createQuestion(str(qDesDict), str(qAnsDict))
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
    
    # TODO: fix
    # def test_create_success(self):
    #     _optList = [opt.text for opt in self.optList]
    #     _optAns = [opt.is_true for opt in self.optList]
    #     qDesDict = {"question": self.qDes, "options": self.optList[0].text}
    #     qAnsDict = self.qAns
    #     qObj: ShortAnswer = self.qFactory.createQuestion(str(qDesDict), str(qAnsDict))
    #     self.assertEqual(qObj.question, self.qDes)
    #     self.assertEqual(qObj.ans, self.qAns)
