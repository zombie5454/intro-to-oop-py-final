from Controller.controller import Question
from question_bank import QuestionBank
import pickle
from typing import List
# TODO: import anything that needed


class Model:
    def __init__(self,directory: str) -> None:
        self.__directory = directory
        return

    #TODO: getter and setter of __directory
        
    def addNewBank(self, name: str) -> bool:
        if name in self.__qBanks:
            return False
        # TODO: build a bank instance (see question_bank.py)
        # and make a directory called name, and use pickle to dump that bank instance
        # pickle name is same as name
        return True

    def getBanks(self)-> List[QuestionBank] :
        # TODO: read all subdirectory in self.__directory, and load banks' pickle, append them to list
        # return a list of qBanks objects
        return []
    
    def getBank(self, name:str)->QuestionBank:
        # we assume that bank exists
        # TODO: open that subdirectory, and load bank's pickle
        # and return that object
        return None