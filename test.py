from tests.test_question import TestShortAnswer, TestMultipleChoice, TestChoice
from tests.test_factory import TestShortAnswerFactory, TestChoiceFactory, TestMultipleChoiceFactory
from tests.test_exam import TestExamShortAnswerOnly
import unittest

# the average coverage for target class is 86.3%
# the total coverage for Model is 47%, because we haven't test model and bank
# the total coverage for Controller is 35%, because we haven't test controller

if __name__ == "__main__":
    unittest.main()