from enum import Enum


class QuestionType(Enum):
    CHOICE = "choice"
    MULTIPLECHOICE = "multiple_choice"
    FILL = "fill_in_the_blank"