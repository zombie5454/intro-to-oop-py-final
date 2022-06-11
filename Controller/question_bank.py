import os
import pickle

# Placeholder
from Controller.controller import Question

class QuestionBank:
    def __init__(self) -> None:
        # Pathname of where our pickle files are saved
        self._db_path = os.path.join(os.getcwd(), "db")
        # List of category strings
        self._cache = []
        self._initCache()

    def addNewCategory(self, name: str) -> bool:
        dir = os.listdir(self._db_path)
        if dir.count(name):
            return False
        # Add the category into cache
        self._cache.append(name)
        # Create a folder in db
        os.mkdir(os.path.join(self._db_path, name))
        return True

    def categoryIsExist(self, name: str) -> bool:
        if self._cache.count(name):
            return True
        return False
    
    def categoryQCount(self, name: str) -> int:
        catDir = os.path.join(self._db_path, name)
        return len(os.listdir(catDir))
    
    def _initCache(self) -> None:
        catList = os.listdir(self._db_path)
        self._cache.extend(catList)

    def addNewQuestion(self, q: Question) -> bool:
        if self._cache.count(q.getCategory()):
            return False
        catDir = os.path.join(self._db_path, q.getCategory())
        # ID increases only
        savedFiles = sorted(os.listdir(catDir))
        curIdx = int(savedFiles[-1])
        pickle.dump(q, open(os.path.join(catDir, str(curIdx + 1)), "wb"))
        return True

if __name__ == "__main__":
    qBank = QuestionBank()
    qBank.addNewCategory("hey")