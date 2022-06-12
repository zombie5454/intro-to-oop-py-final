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
        self.__issuedID = -1
        # TODO: find the maximum ID in the directory (ex: 1.pickle, 0.pickle, 3.pickle --> maxi ID is 3)
        
    #TODO: getter of __directory, __name, __issuedID
    #need setter for __name

    def addQuestion(self, q: Question) -> bool:
        # change the q's ID to issuedID + 1
        # TODO: use pickle to dump q in self.directory
        # pickle name = q's ID
        # if file already exists, return false
        return True
    
    def getQuestionList(num=-1)-> List[Question]:
        if num < 0:
            # TODO: append all question in self.directory
            pass
        else:
            # TODO: pick random num of questions
            pass
    
        # shuffle the list, and return it
        return []

    def editQuestion(changed_question: Question)->bool:
        # TODO: use question object's ID to open that pickle in w/wb mode
        # DNE -> return false
        # overwrite the pickle with that objects
        return False

    def deleteQuestion(ID: int)->bool:
        # TODO: use ID to delete that pickle
        # DNE -> return false
        return False

if __name__ == "__main__":
    qBank = QuestionBank()