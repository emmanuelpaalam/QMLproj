import re
from models import Token

class Lexer:
    def __init__(self, text: str):
        self.text = text

        token_specs = [
            ('TAG_OPEN_ATTR', r'<[a-zA-Z]+\s+[a-zA-Z]+="[a-zA-Z]+">'),
            ('TAG_CLOSE', r'</[a-zA-Z]+>'),
            ('TAG_OPEN', r'<[a-zA-Z]+>'),
            ('TEXT', r'[^<>]+')
        ]

        regex_string = '|'.join(f'(?P<{name}>{pattern})' for name, pattern in token_specs)
        self.pattern = re.compile(regex_string)

        self.match_iterator = self.pattern.finditer(self.text)

        self.next_token_buffer = None

    def get_next_token(self) -> Token:
        if self.next_token_buffer: # if we already peeked ahead, return that token
            token = self.next_token_buffer
            self.next_token_buffer = None
            return token

        for match in self.match_iterator:
            kind = match.lastgroup
            value = match.group()
            if kind == 'TEXT':
                value = value.strip() # removes leading and trailing whitespace
                if not value: # if the text is empty after stripping, skip it
                    continue
            return Token(kind, value)
        
        return Token('EOF', '') # end of file token
    
    def peek(self) -> Token:
        if not self.next_token_buffer: # if we haven't peeked ahead yet, get the next token and store it
            self.next_token_buffer = self.get_next_token()
        return self.next_token_buffer

# test code
if __name__ == "__main__":
    text = '''
    <quiz>
    <title>Sample</title>
        <question>
            <text>One</text>
            <option correct="true">A</option>
            <option>B</option>
        </question>
        <question>
            <text>Two</text>
            <option>A</option>
            <option correct="true">B</option>
        </question>
    </quiz>
    '''

    my_lexer = Lexer(text)
    print("Tokens found:")
    while True:
        token = my_lexer.get_next_token()
        if token.type == 'EOF':
            print("End of file reached.")
            break
        print(f"  {token.type}: {token.value}")