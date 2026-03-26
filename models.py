from dataclasses import dataclass
from typing import List

@dataclass
class Token:
    type: str
    value: str

@dataclass
class OptionNode:
    is_correct: bool
    text: str

@dataclass
class QuestionNode:
    text: str
    options: List[OptionNode]

@dataclass
class QuizNode:
    title: str
    questions: List[QuestionNode]