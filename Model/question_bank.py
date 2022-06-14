import os, re, random
import pickle
from typing import List

# Placeholder
from Model.question import Question

# TODO: import anything that needed


class QuestionBank:
    def __init__(self, name: str, directory: str) -> None:
        self.__name = name
        # directory name  == name
        self.__directory = directory
        self.__issuedID = self.find_max()
        # TODO: find the maximum ID in the directory (ex: 1.pickle, 0.pickle, 3.pickle --> maxi ID is 3)

    # TODO: getter of __directory, __name, __issuedID
    # need setter for __name
    @property
    def directory(self):
        return self.__directory

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, newname: str):
        self.__name = newname

    @property
    def issuedID(self):
        return self.__issuedID

    def find_max(self) -> int:
        list_files = os.listdir(self.__directory)
        max_n = -1
        for file in list_files:
            num = int(re.search("(\d*).pickle", file).group(1))
            max_n = num if num > max_n else max_n
        return max_n

    def addQuestion(self, q: Question) -> bool:
        # change the q's ID to issuedID + 1
        # if file already exists, return false
        if "{}.pickle".format(self.__issuedID + 1) in os.listdir(self.__directory):
            return False
        self.__issuedID = self.__issuedID + 1
        q_id = self.__issuedID
        q.ID = q_id

        # TODO: use pickle to dump q in self.directory
        # pickle name = q's ID
        path = os.path.join(self.__directory, "{}.pickle".format(q_id))
        with open(path, "wb") as f:
            pickle.dump(q, f)
        
        return True

    def getQuestionList(self, num=-1) -> List[Question]:
        if num < 0:
            # TODO: append all question in self.directory
            q_list = []
            list_files = os.listdir(self.__directory)

            for file in list_files:
                path = os.path.join(self.__directory, file)
                with open(path, "rb") as f:
                    x = pickle.load(f)
                q_list.append(x)

        else:
            # TODO: pick random num of questions
            q_list = []
            list_files = random.sample(os.listdir(self.__directory), num)

            for file in list_files:
                path = os.path.join(self.__directory, file)
                with open(path, "rb") as f:
                    x = pickle.load(f)
                q_list.append(x)

        # shuffle the list, and return it
        random.shuffle(q_list)

        return q_list

    def editQuestion(self, changed_question: Question) -> bool:
        # TODO: use question object's ID to open that pickle in w/wb mode
        # DNE -> return false
        ch_id = changed_question.ID
        if "{}.pickle".format(ch_id) not in os.listdir(self.__directory):
            return

        path = os.path.join(self.__directory, "{}.pickle".format(ch_id))
        with open(path, "wb") as f:
            pickle.dump(changed_question, f)
        # overwrite the pickle with that objects
        return True

    def deleteQuestion(self, ID: int) -> bool:
        # TODO: use ID to delete that pickle
        if "{}.pickle".format(ID) not in os.listdir(self.__directory):
            return False
        # DNE -> return false
        path = os.path.join(self.__directory, "{}.pickle".format(ID))
        os.remove(path)
        return True


if __name__ == "__main__":
    qBank = QuestionBank()
