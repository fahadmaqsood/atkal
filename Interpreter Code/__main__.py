import re
#import os
#import playsound

#current_path = os.path.dirname(__file__)

from interpreter_utils.Tokenizer import Tokenizer


class SimpleLangInterpreter:
    def __init__(self):
        self.tokenizer = Tokenizer()

        self.variables = {}
        self.current_line = 0
        self.lines = []

    def run(self, code):
        self.current_line = 0
        self.lines = code.split('\n')

        while self.current_line < len(self.lines):
            line = self.lines[self.current_line].strip()
            self.execute_line(line)

        
            self.current_line += 1

    def execute_line(self, line):
        if line.strip().startswith("//"):
            return
        
        tokens = self.tokenizer.tokenize(line)
        tokens = [x.strip() for x in tokens]

        if tokens:
            if tokens[0] == "dekhaar":
                self.handle_print(tokens[1:])
            elif tokens[0] == "jekadhen":
                self.handle_if(tokens[1:])
            elif tokens[0] == "jesitaeen":
                self.handle_while(tokens[1:])
            else:
                self.handle_assignment(tokens)


    def evaluate_expression(self, expression):
        # Remove spaces around operators
        expression = re.sub(r'\s*([+\-*/%=<>])\s*', r'\1', expression)

        # # Substitute variable values
        # for var_name in re.findall(r'\b\w+\b', expression):
        #     if not var_name.isnumeric():
        #         expression = expression.replace(var_name, str(self.variables.get(var_name, 0)))
        
        if '+' in expression or '-' in expression or '*' in expression or '/' in expression:
            try:
                return eval(expression, {}, self.variables)
            except TypeError as t:
                #playsound.playsound(current_path + "/audio/bhaan-awwn-cha.mp3")
                raise TypeError("Arre, Bhaan awwn cha 👀")
            except SyntaxError as t:
                raise SyntaxError("Lage tho processor slow athayi 😆")
            
        # if '+' in expression:
        #     try:
        #         return sum(map(int, expression.split('+')))
        #     except ValueError as e:
        #         raise ValueError("Andha, dis ta sahi cha khe tho plus kareen 👀")
        # elif '-' in expression:
        #     operands = map(int, expression.split('-'))
        #     return next(operands) - sum(operands)
        # elif '*' in expression or '/' in expression or '%' in expression:
        #     return eval(expression);
        # elif expression.isdigit():
        #     return int(expression)
        # elif expression.isalpha():
        #     return self.variables.get(expression, 0)
        # elif any(op in expression for op in ('==', '!=', '<=', '>=', '<', '>')):
        #     # Handle comparison operators
        #     return eval(expression, {}, self.variables)
        # else:

        try:
            return eval(expression, {}, self.variables)
        except:
            raise SyntaxError(f"Expression he galat athayi: {expression}")

    def handle_print(self, tokens):
        # for token in tokens:
        #     if token.startswith('"') and token.endswith('"'):
        #         print(token[1:-1], end=" ")
        #     elif token.isalpha():
        #         # Check if the token is a variable
        #         print(self.variables.get(token, token), end=" ")
        #     else:
        #         print(self.evaluate_expression(token.strip()), end=" ")
        try:
            print(self.evaluate_expression(" ".join(tokens)), end=" ")
        except SyntaxError as t:
            raise SyntaxError("Bus yar maana na sikhi saghen na")
            
        print()


    def handle_assignment(self, tokens):
        var_name = tokens[0]
        if '=' in tokens:
            # Explicit assignment
            index = tokens.index('=')
            expression = ' '.join(tokens[index + 1:])

            if expression.startswith('"') and expression.endswith('"'):
                self.variables[var_name] = expression[1:-1]
            else:
                self.variables[var_name] = self.evaluate_expression(expression)
        else:
            # Implicit assignment without '=' sign
            expression = ' '.join(tokens[1:])

            self.variables[var_name] = self.evaluate_expression(expression)

    def handle_if(self, tokens):
        # Find the indices of opening and closing round brackets
        opening_bracket_index = tokens.index('(')
        closing_bracket_index = tokens.index(')')

        # Extract the condition using the round brackets
        condition = ' '.join(tokens[opening_bracket_index + 1:closing_bracket_index])

        if eval(condition, {}, self.variables):
            # Execute lines within the if block
            opening_bracket_index = self.current_line
            while opening_bracket_index < len(self.lines) and "{" not in self.lines[opening_bracket_index]:
                opening_bracket_index += 1

            closing_bracket_index = opening_bracket_index
            while closing_bracket_index < len(self.lines) and "}" not in self.lines[closing_bracket_index]:
                closing_bracket_index += 1

            if opening_bracket_index + 1 == closing_bracket_index:
                # Single-line block, execute it
                self.execute_line(self.lines[opening_bracket_index].strip())
            else:
                # Multi-line block, execute lines within the block
                for i in range(opening_bracket_index + 1, closing_bracket_index):
                    self.execute_line(self.lines[i].strip())

            # Skip lines until '}' is encountered
            while self.current_line < len(self.lines) and not self.lines[self.current_line].strip().startswith('}'):
                self.current_line += 1

            self.handle_else(True)
        else:
            # Execute lines within the else block
            self.handle_else(False)


    def handle_else(self, was_if_true=False):
        # Skip lines until '}' is encountered
        while self.current_line < len(self.lines) and not self.lines[self.current_line].strip().startswith('}'):
            self.current_line += 1

        if "nata" not in self.lines[self.current_line]:

            self.current_line += 1

            # skip empty lines until nata is found
            while self.current_line < len(self.lines) and not self.lines[self.current_line].strip().startswith('nata'):
                
                if self.lines[self.current_line].strip() == "":
                    self.current_line += 1
                else:
                    # possibly there is not else block
                    return

        if not was_if_true:
            # Execute lines within the nata block
            opening_bracket_index = self.current_line
            while opening_bracket_index < len(self.lines) and "{" not in self.lines[opening_bracket_index]:
                opening_bracket_index += 1

            closing_bracket_index = opening_bracket_index
            while closing_bracket_index < len(self.lines) and "}" not in self.lines[closing_bracket_index]:
                closing_bracket_index += 1

            if opening_bracket_index + 1 == closing_bracket_index:
                # Single-line block, execute it
                self.execute_line(self.lines[opening_bracket_index].strip())
            else:
                # Multi-line block, execute lines within the block
                for i in range(opening_bracket_index + 1, closing_bracket_index):
                    self.execute_line(self.lines[i].strip())

        # Skip lines until '}' is encountered
        while self.current_line < len(self.lines) and not self.lines[self.current_line].strip().startswith('}'):
            self.current_line += 1

        

    def handle_while(self, tokens):
        # Find the indices of opening and closing round brackets
        opening_bracket_index = tokens.index('(')
        closing_bracket_index = tokens.index(')')

        # Extract the condition using the round brackets
        condition = ' '.join(tokens[opening_bracket_index + 1:closing_bracket_index])


        # finding opening curly bracket of while loop
        curly_open_index = self.current_line
        while curly_open_index < len(self.lines) and "{" not in self.lines[curly_open_index]:
            curly_open_index += 1

        start_line = curly_open_index + 1

        while self.evaluate_expression(condition):
            # Execute lines inside the while loop
            self.current_line = start_line
            while not self.lines[self.current_line].strip().startswith('}'):
                self.execute_line(self.lines[self.current_line].strip())

                     
                self.current_line += 1

            # Reset the line pointer to the start of the loop for the next iteration
            self.current_line = start_line

            # Re-evaluate the condition after executing the lines in the loop
            condition = ' '.join(tokens[opening_bracket_index + 1:closing_bracket_index])

        # Skip lines until '}' is encountered
        while self.current_line < len(self.lines) and not self.lines[self.current_line].strip().startswith('}'):
            self.current_line += 1


if __name__ == "__main__":
    import argparse
    from pathlib import Path

    parser = argparse.ArgumentParser()
    parser.add_argument("file_path", type=Path)

    p = parser.parse_args()
    #print(p.file_path, type(p.file_path), p.file_path.exists())

    if p.file_path.exists():
        interpreter = SimpleLangInterpreter()

        with open(p.file_path) as f:
            interpreter.run(f.read())
    else:
        print("Code file is required for interpreting.")
        input("Press any key to continue...")
        

