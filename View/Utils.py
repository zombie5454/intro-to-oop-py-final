import json
from typing import List
from Model.question_type import QuestionType
from Controller.controller import Controller
from View.MyWidgets import BankListWidgetItem

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
                questionAns = question["answer"]
            controller.addNewQuestion(bank["bankName"], questionType, questionText, questionAns)


def export_data(controller: Controller, bankList: List[BankListWidgetItem], filepath: str):
    if not controller or not bankList or not filepath:
        return
    data = []
    for bank in bankList:
        bankData = {"bankName": bank.bankName, "questions": []}
        questions = controller.getQuestionList(bank.bankName)
        for question in questions:
            questionData = {"question": question.question, "type": question.type.value}
            if question.type == QuestionType.CHOICE or question.type == QuestionType.MULTIPLECHOICE:
                questionData["choices"] = [[choice.text, choice.is_true] for choice in question.choices]
            elif question.type == QuestionType.FILL:
                questionData["answer"] = question.ans
            bankData["questions"].append(questionData)
        data.append(bankData)
    with open(filepath, "w") as f:
        json.dump(data, f)
