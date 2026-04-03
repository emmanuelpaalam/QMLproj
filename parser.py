from models import QuizNode, QuestionNode, OptionNode
from lexer import Lexer


class Parser:
    def __init__(self, lexer: Lexer):
        self.lexer = lexer
        self.current_token = self.lexer.get_next_token()

    def eat(self, token_type: str, token_value: str = ""):
        if self.current_token.type != token_type:
            raise SyntaxError(f"Expected token type '{token_type}' but found '{self.current_token.type}' ('{self.current_token.value}')")
        if token_value and self.current_token.value != token_value:
            raise SyntaxError(f"Expected '{token_value}' but found '{self.current_token.value}'")
        consumed = self.current_token
        self.current_token = self.lexer.get_next_token()
        return consumed

    def parse_quiz(self) -> QuizNode:
        self.eat('TAG_OPEN', '<quiz>')

        self.eat('TAG_OPEN', '<title>')
        title_token = self.eat('TEXT')
        self.eat('TAG_CLOSE', '</title>')

        questions = []
        while self.current_token.value == '<question>':
            questions.append(self.parse_question())

        if len(questions) < 1:
            raise SyntaxError("A <quiz> must contain one or more <question> blocks")

        self.eat('TAG_CLOSE', '</quiz>')
        self.eat('EOF')

        return QuizNode(title=title_token.value, questions=questions)

    def parse_question(self) -> QuestionNode:
        self.eat('TAG_OPEN', '<question>')

        self.eat('TAG_OPEN', '<text>')
        text_token = self.eat('TEXT')
        self.eat('TAG_CLOSE', '</text>')

        options = []
        while self.current_token.value in ('<option>', '<option correct="true">'):
            options.append(self.parse_option())

        if len(options) < 2:
            raise SyntaxError("A <question> must contain two or more <option> blocks")

        # Additional check to ensure at least one option is marked as correct
        if not any(option.is_correct for option in options):
            raise SyntaxError("A <question> must contain at least one correct <option>")

        self.eat('TAG_CLOSE', '</question>')

        return QuestionNode(text=text_token.value, options=options)

    def parse_option(self) -> OptionNode:
        if self.current_token.type == 'TAG_OPEN_ATTR':
            self.eat('TAG_OPEN_ATTR', '<option correct="true">')
            is_correct = True
        else:
            self.eat('TAG_OPEN', '<option>')
            is_correct = False

        text_token = self.eat('TEXT')
        self.eat('TAG_CLOSE', '</option>')

        return OptionNode(is_correct=is_correct, text=text_token.value)


if __name__ == "__main__":
    text = '''
    <quiz>
        <title>Sample Quiz</title>
        <question>
            <text>What is 1+1?</text>
            <option correct="true">2</option>
            <option>3</option>
        </question>
        <question>
            <text>What color is the sky?</text>
            <option>Green</option>
            <option correct="true">Blue</option>
        </question>
    </quiz>
    '''

    lexer = Lexer(text)
    parser = Parser(lexer)
    ast = parser.parse_quiz()
    print(ast)