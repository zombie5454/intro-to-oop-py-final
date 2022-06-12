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
        # TODO: make a directory called name, if the directory already exists, return false
        # build a bank instance (see question_bank.py)
        # and use pickle to dump that bank instance in that directory
        # pickle name is same as name
        return True

    def getBanks(self)-> List[QuestionBank] :
        # TODO: read all subdirectory in self.__directory, and load banks' pickle, append them to list
        # return a list of qBanks objects
        return []
    
    def getBank(self, name:str)->QuestionBank:
        # TODO: open that subdirectory, if the open operation failed (ex: dir does not exist), return None
        # and load bank's pickle
        # and return that object
        return None