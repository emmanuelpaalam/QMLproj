import sys
import os
from lexer import Lexer
from parser import Parser
from serializer import Serializer

def main():
    if len(sys.argv) != 2:
        print("Usage: python main.py [input_file]")
        sys.exit(1)
    
    filename = sys.argv[1]

    if not os.path.isfile(filename):
        print(f"Error: file '{filename}' not found.")
        sys.exit(1)

    try:
        with open(filename, "r", encoding="utf-8") as f: 
            text = f.read()

        lexer = Lexer(text)
        parser = Parser(lexer)
        quiz_ast = parser.parse_quiz()

        serializer = Serializer()
        json_output = serializer.to_json(quiz_ast)

        output_filename = os.path.splitext(filename)[0] + ".json"

        with open(output_filename, "w", encoding="utf-8") as f: 
            f.write(json_output)

            print(f"Successfully transpiled '{filename}' to '{output_filename}'.")

    except SyntaxError as e: 
        print(f"syntax error: {e}")
        sys.exit(1)

    except Exception as e: 
        print(f"Error: {e}")
        sys.exit(1)
    
if __name__ == "__main__":
    main()