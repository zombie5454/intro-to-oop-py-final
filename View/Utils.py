import json
from Model.question_type import QuestionType
from Controller.controller import Controller

qdict = {"單選": QuestionType.CHOICE, "多選": QuestionType.MULTIPLECHOICE, "填充": QuestionType.FILL}


def save_data(controller: Controller, filepath: str):
    if not controller or not filepath:
        return
    data = []
    with open(filepath, "r") as f:
        data = json.load(f)
    for bank in data:
        controller.addBank(bank["bankName"])
        for question in bank["questions"]:
            questionText = question["question"]
            questionType = qdict[question["type"]]
            if questionType == QuestionType.CHOICE or questionType == QuestionType.MULTIPLECHOICE:
                choices = []
                questionAns = []
                for choice in question["choices"]:
                    choices.append(choice[0])
                    questionAns.append(choice[1])
                questionText = {"question": questionText, "options": choices}
                questionText, questionAns = str(questionText), str(questionAns)
            elif questionType == QuestionType.FILL:
                questionText = question["question"]
                questionAns = question["answer"]
            controller.addNewQuestion(bank["bankName"], questionType, questionText, questionAns)
