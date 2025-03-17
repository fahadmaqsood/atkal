import re


class Tokenizer:
    def tokenize(self, line):
        
        # Split the line into tokens, considering operators, parentheses, and quotes
        tokens = re.findall(r'\b\w+\b|[-+*/%=<>!&|(){},;]=?|"[^"]*"', line)

        # Combine consecutive operators
        combined_tokens = []
        i = 0
        while i < len(tokens):
            if re.match(r'[-+*/%=<>!&|]=?', tokens[i]):
                combined_token = tokens[i]
                i += 1
                while i < len(tokens) and re.match(r'[-+*/%=<>!&|]=?', tokens[i]):
                    combined_token += tokens[i]
                    i += 1
                combined_tokens.append(combined_token)
            else:
                combined_tokens.append(tokens[i])
                i += 1

        return combined_tokens
