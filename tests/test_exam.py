import unittest
from Controller.exam import Exam

class TestExam(unittest.TestCase):
    def setUp(self) -> None:
        # TODO: setup question bank
        self.exam = Exam(0, "")
    
    # TODO: teardown testing data
    def tearDown(self) -> None:
        return super().tearDown()