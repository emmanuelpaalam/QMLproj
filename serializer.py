import json
from models import QuizNode

class Serializer:
    def serialize(self, quiz_node: QuizNode) -> dict:
        return {
            "title": quiz_node.title,
            "questions": [
                {
                    "text": question.text,
                    "options": [
                        {
                            "text": option.text,
                            "is_correct": option.is_correct
                        }
                        for option in question.options
                    ]
                }
                for question in quiz_node.questions
            ]
        }

    def to_json(self, quiz_node: QuizNode, indent: int = 2) -> str:
        return json.dumps(self.serialize(quiz_node), indent=indent)