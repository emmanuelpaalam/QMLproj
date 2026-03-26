import sys

# Import modules once properly created
# from tokens import Token
# from lexer import Lexer
# from parser import Parser
# from serializer import Serializer

def main():
    # Placeholder for main function
    print("Main function is not yet implemented.")

    if len(sys.argv) != 2:
        print("Usage: python main.py [input_file]")
        sys.exit(1)
    
    filename = sys.argv[1]
    print(f"Target: {filename}")
    # then call components to process target file into JSON
    # remember to check if second argument is a valid file before processing
    
if __name__ == "__main__":
    main()