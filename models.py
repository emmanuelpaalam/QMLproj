from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type: str
    value: str

@dataclass
class OptionNode:
    pass

@dataclass
class QuestionNode:
    pass

@dataclass
class QuizNode:
    pass