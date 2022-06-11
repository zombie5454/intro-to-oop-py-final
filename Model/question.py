# TODO: import anything that needed

class Question:
    def __init__(self, type:str, question: str, ans) -> None:
        self.__type = type
        self.__question = question
        # for short answer, ans is str
        # for multiple choice and choice, ans is list of choice options
        self.__ans = ans
        return
    
    
    # TODO: getter and setter 


    def checkAnswer(answer: str) -> bool:
    # multiple choice -> one wrong, all wrong
    # TODO: for multiple choice, split answer to get choice list
    # short answer -> answer == ans?
    # choice: is ans[answer[i]].is_true == true?
    # multiple choice: is i in answer (ans[i].is_true == true)? is ans[answer[i]].is_true == true?
        return True


class ShortAnswer(Question):
    def __init__(self, question: str, ans: str) -> None:
        super().__init__("short_answer", question,ans)
    
class MultipleChoice(Question):
    def __init__(self, question: str, choice: list) -> None:
        super().__init__("multiple_choice", question, choice)

class Choice(Question):
    def __init__(self, question: str, choice: list) -> None: 
        super().__init__("choice", question, choice)


class ChoiceOption:
    def __init__(self, text="", is_true=False) -> None:
        self.__text = text
        self.__is_true = is_true
        pass

    # TODO: getter and setter