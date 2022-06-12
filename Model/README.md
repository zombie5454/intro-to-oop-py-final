# MODEL
## Model class
### attribute
* directory: path where all the question banks locate

### method
1.  to create a model, caller has to pass the directory path where all the question banks locate
    * example:``model = Model("./a")``
2. to add a question bank, caller has to pass the name of that question bank
    * example: ``model.addNewBank("dsa")``
    * if the bank already exists, return false
    * else, return true
3. to get all question banks
    * example: ``qBankList = model.getBanks()``
    * return a list of qBanks objects
4. to get desired question bank, caller has to pass the name of that question bank
    * example: ``qBank = model.getBank("dsa")``
    * if the bank does not exist, return None
    * else, return qBank object
5. to get directory, simply call ``model.directory``
    * we will implement a getter 
    * change directory during runtime **is not allowed**

## QuestionBank class
### attribute
* name: qBank's name
* directory: path where the qBank pickle locates
* issuedID: current Maximum questionID

### method
1. to init bank, caller(addNewBank in Model) has to pass the name, and the directory that **qBank pickle** locates
    * example: ``qBank = QuestionBank("dsa","./a/dsa")``
2. to add question, caller will pass a question object
    * example: `` qBank.addNewQuestion(q)``
    * q is question object
    * here we will change q's ID based on qBank's issuedID
    * controller does not have to set up q's ID
3. to get a list of questions, caller will pass a number, if caller does not pass number or pass a negative number, return list of all questions
    * example1: ``qList = qBank.getQuestionList(3)``
        * return list that contains 3 question objects
    * example2: ``qList = qBank.getQuestionList()``
        * return list of all questions
    * example3: ``qList = qBank.getQuestionList(-1)``
        * return list of all questions
4. to get directory, simply call ``qBank.directory``
    * we will implement a getter 
    * change directory during runtime **is not allowed**
5. to get name, simply call ``qBank.name``
    * we will implement a getter 
    * change name directly outside QuestionBank **is not allowed**
    * if we support editBank, call ``editBank`` to change the name of bank
6. to get issuedID, simply call: ``qBank.issuedID``
    * we will implement a getter 
    * change name directly outside QuestionBank **is not allowed**

## Question class
### attribute
* type: short answer, multiple choice , or choice
* question: question description, **DOES NOT** includes choices
* ans: correct ans, including choices objects
* ID: Id given by qBank

### method
1. to init a question, please refer to question_factory :D
2. to check answer, caller has to pass user's anwer
    * short answer example: ``q.checkAnswer("No, because...")``
        * if answer does not **fully match** with q.ans --> return false
    * multiple choice example: ``q.checkAnswer("0,1")``
        * it means that user choose 0th, 1th choices
        * if answer does not contain all correct choices or contains incorrect choices --> return false
    * choice example: ``q.checkAnswer("0")``
        * it means that user choose 0th choice
        * if answer is not the correct choice --> return false
3. to get/set attribute
    * ``q.ans``
    * ``q.type``
    * ``q.quesetion``
    * ps, if we support editQuestion, user call ``editQuestion`` to change above attributes
    * only getter for ID, change ID during runtime **is not allowed**
    * ``q.ID``

## QuestionFactory
1. Instantiated in main, injected into the controller class
    * Model will not need to be aware of it
2. Abstract class for question creation

### attribute
* qType: str representing the question type

### methods
1. Pass in question description string (qDes) and question answer string (qAns) from View into it
2. Format of the strings differs from type-to-type, the following negoatied format are as thus:
    * ShortAnswer:
        * ``qDes``: simply a string
        * ``qAns``: the answer string to match the whole user-input for in checking their answer
    * Choice:
        * ``qDes``: string representation of dict
            * ``"question"`` key: contains the question string
            * ``"options"`` key: contains the option description strings
        * ``qAns``: string representation of list of bool
            * Index matches with the order of option strings (index 0 represents the first option string)
            * ``True``: is this option is the answer
            * ``False``: otherwise
3. Usage: simply call ``createQuestion(qDes, qAns)`` to obtain the appropriate ``Question`` object
    * see src code for impl details

## NOTE
subclass usage and choice usage are omitted here
