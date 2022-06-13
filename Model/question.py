# TODO: import anything that needed
from typing import List
from Model.question_type import QuestionType

class Question:
    def __init__(self, type:QuestionType, question: str) -> None:
        self.__type = type
        self.__question = question
        # for short answer, ans is str
        # for multiple choice and choice, ans is list of choice options
        #self.__ans = ans
        #我把題目的ans放在sub class裡面
        self.__ID = -1
        return
    
    
    # TODO: getter and setter 
    # NO setter for ID
    @property
    def type(self):
        return self.__type
    @type.setter
    def type(self, newtype: QuestionType):
        self.__type = newtype
    
    @property
    def question(self):
        return self.__question
    @question.setter
    def question(self, newquestion: str):
        self.__question = newquestion
    
    @property
    def ID(self):
        return self.__ID
    @ID.setter
    def ID(self, newID: int):
        self.__ID = newID
    


    def checkAnswer(answer: str) -> bool:
    # multiple choice -> one wrong, all wrong
    # TODO: for multiple choice, split answer to get choice list
    # short answer -> answer == ans?
    # choice: is ans[answer[i]].is_true == true?
    # multiple choice: is i in answer (ans[i].is_true == true)? is ans[answer[i]].is_true == true?
    #    return True
    #我把checkAnswer放在subclass下面
        pass

class ChoiceOption:
    def __init__(self, text : str, is_true : bool):
        self.__text = text
        self.__is_true = is_true

    # TODO: getter and setter
    @property
    def text(self) -> str:
        return self.__text
    @property
    def is_true(self) -> bool:
        return self.__is_true
    

class ShortAnswer(Question):
    def __init__(self, question: str, ans: str):
        super().__init__(QuestionType.FILL, question)
        self.__ans = ans
    @property
    def ans(self):
        return self.__ans
    '''
    def checkAnswer(self , answer: str) -> bool:
        answer=answer.upper()
        if answer.find(self.__ans.upper()) ==-1:
            return False
        else:
            return True
    '''

class MultipleChoice(Question):
    def __init__(self, question: str, choices: List[ChoiceOption]):
        super().__init__(QuestionType.MULTIPLECHOICE, question)
        self.__choices=choices
    @property
    def choices(self):
        return self.__choices
    '''
    def checkAnswer(self , answer) -> bool:
        #該answer成員為包含is_true、selected跟text的class
        for i in answer:
            if i.selected != i.is_true:
                return False
        return True
    '''

class Choice(Question):
    def __init__(self, question: str, choices: List[ChoiceOption]): 
        super().__init__(QuestionType.CHOICE, question)
        self.__choices=choices
    @property
    def choices(self):
        return self.__choices
    '''
    def checkAnswer(self , answer) -> bool:
        #該answer成員為包含is_true、selected跟text的class
        for i in answer:
            if i.selected != i.is_true:
                return False
        return True
    '''



