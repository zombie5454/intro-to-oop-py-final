class ChoiceOption:
    text = 'None'
    is_true = None

# Placeholders
class Question:
    type = 'None'
    question = 'None'
    answer = 'None'
    choices = []       #ChoiceOption[]
    num_of_currect_choices = -1
    category = 'None'

    def getCategory(self) -> str:
        return self.category

    def displayQuestion(self) -> str:   
        ans = 'Q: ' + self.question
        if self.type == 'MultipleChoice' or self.type == 'Choice':
            for i in range(len(self.choices)):
                ans = ans + '\n' + str(i) + '. ' + self.choices[i].text
        
        return ans

    def getAnswer(self) -> str:
        return self.answer
        
    def checkAnswer(self, answer: str) -> bool:
        if self.type == 'ShortAnswer':                  #找到關鍵字就算對
            if answer.find(self.answer) == -1:
                return False
            else:
                return True

        elif self.type == 'MultipleChoice' or self.type == 'Choice':   #如果答對的選項數 = 總共對的選項數
            chosen_dict = {}
            num_correct = 0
            for s in answer:
                if s.isdigit() == True and int(s) <= len(self.choices)-1:
                    if self.choices[int(s)].is_true == True and chosen_dict.get(s) != True:  #確保重複答對選項不算
                        num_correct += 1
                        chosen_dict[s] = True
                    elif self.choices[int(s)].is_true == False:
                        return False
            #print(num_correct)
            if num_correct == self.num_of_currect_choices:
                return True
            else:
                return False
