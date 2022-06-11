from Model.question import Choice, ChoiceOption, Question, ShortAnswer
from typing import List


# TODO: validating & cleaning user input
class QuestionFactory():
    def __init__(self, qType: str) -> None:
        self.__qType : str = qType
    def createQuestion(self, qDes: str, qAns: str) -> Question:
        pass
    @property
    def qType(self) -> str:
        return self.qType

class ShortAnswerFactory(QuestionFactory):
    def createQuestion(self, qDes: str, qAns: str) -> Question:
        return ShortAnswer(qDes, qAns)

class ChoiceFactory(QuestionFactory):
    # Expected input format:
    # qDes: 'question_des???option1,option2,option3'
    # qAns: '0' (index of option)
    def createQuestion(self, qDes: str, qAns: str) -> Question:
        components = qDes.split("???")
        qStr = components[0]
        ansIdx = int(qAns)
        # Parse and create ChoiceOption
        optList = components[1].split(",")
        qOptList: List[ChoiceOption] = []
        for i in range(len(optList)):
            qOptList.append(ChoiceOption(optList[i]))
        qOptList[ansIdx].is_true = True
        return Choice(qStr, qOptList)

class MultipleChoiceFactory(QuestionFactory):
    # Expected input format:
    # qDes: 'question_des???option1,option2,option3'
    # qAns: '1,2' (indices of options)
    def createQuestion(self, qDes: str, qAns: str) -> Question:
        components = qDes.split("???")
        qStr = components[0]
        # Parse expected answer index
        qAnsList = sorted([int(ans) for ans in qAns.split(",")])
        # Parse and create ChoiceOption
        optList = components[1].split(",")
        qOptList: List[ChoiceOption] = []
        for i in range(len(optList)):
            qOptList.append(ChoiceOption(optList[i]))
        for i in qAnsList:
            qOptList[i].is_true = True
        return Choice(qStr, qOptList)
