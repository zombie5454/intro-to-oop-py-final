from .question_bank import QuestionBank
import pickle
from typing import List
import os, sys
from os import listdir
import shutil
# TODO: import anything that needed


class Model:
    def __init__(self,directory: str) -> None:
        self.__directory = directory
        if not os.path.isdir(directory):
            os.mkdir(directory)
        return

    #TODO: getter of __directory
    # NO need for setter, we don't want to change directory during runtime
    @property
    def directory(self):
        return self.__directory
    def addNewBank(self, name: str) -> bool:
        # TODO: make a directory called name, if the directory already exists, return false
        # build a bank instance (see question_bank.py)
        # and use pickle to dump that bank instance in that directory
        # pickle name is same as name
        path =  os.path.join(self.directory,name) 
        if not os.path.isdir(path):
            os.mkdir(path)
            NewBank = QuestionBank(name,path)
            with open(f'{path}.pickle', 'wb') as f:
                pickle.dump(NewBank, f)
            return True
        else:
            return False

    def getBanks(self)-> List[QuestionBank] :
        # TODO: read all subdirectory in self.__directory, and load banks' pickle, append them to list
        # return a list of qBanks objects
        files = listdir(self.directory)
        files = [file for file in files if os.path.isdir(file)]
        QuestionBanks = []
        for name in files:
            path =  os.path.join(self.directory,name) 
            with open(f'{path}.pickle', 'rb') as f:
                Target_Bank = pickle.load(f)
                QuestionBanks.append(Target_Bank)
        return QuestionBanks
    
    def getBank(self, name:str)->QuestionBank:
        # TODO: open that subdirectory, if the open operation failed (ex: dir does not exist), return None
        # and load bank's pickle
        # and return that object
        path =  os.path.join(self.directory,name) 
        if not os.path.isdir(path):
            return None
        else:
            with open(f'{path}.pickle', 'rb') as f:
                Target_Bank = pickle.load(f)
            return Target_Bank

    def editBankName(self,oldname:str, newname:str)->bool:
        # TODO: open the directory called oldname, if failed (ex: dir does not exist), return false
        # also, try to open the directory called newname, if success (new dir already exist), return false
        # load qBanks object from the pickle called oldname
        # modify the objects name, and its directory (ex: ./a/dsa_old -> ./a/dsa_new)
        # delete old pickle, dump a new pickle named newname
        # change directory's name
        old_path = os.path.join(self.directory,oldname) 
        new_path = os.path.join(self.directory,newname) 
        if not os.path.isdir(old_path):
            return False
        elif os.path.isdir(new_path):
            return False
        else:
            with open(f'{new_path}.pickle', 'wb') as f:
                NewBank = QuestionBank(newname,new_path)
                pickle.dump(NewBank, f)
            os.remove(f'{old_path}.pickle')
            os.rename(old_path,new_path)
            return True
                
    def deleteBank(self, name:str)->bool:
        # TODO: delete the directory called name (also delete all files in the directory)
        # if failed -> return false
        path = os.path.join(self.directory,name) 
        if not os.path.isdir(path):
            return False
        else:
            os.remove(path + ".pickle")
            try:
                shutil.rmtree(path)
                return True
            except:
                return False
