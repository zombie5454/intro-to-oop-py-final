import os
import pickle
from typing import List

# Placeholder
from question import Question
# TODO: import anything that needed

class QuestionBank:
    def __init__(self, name: str, directory: str) -> None:
        self.__name = name
        # directory name  == name 
        self.__directory = directory

    #TODO: getter and setter of __directory, __name

    def addQuestion(self, q: Question) -> bool:
        # TODO: use pickle to dump q in self.directory
        return True
    
    def getQuestionList(num=-1)-> List[Question]:
        if num == -1:
            # TODO: append all question in self.directory
            pass
        else:
            # TODO: pick random num of questions
            pass
    
        # shuffle the list, and return it
        return []


if __name__ == "__main__":
    qBank = QuestionBank()
    qBank.addNewCategory("hey")