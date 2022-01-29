"""
  LEXER: traverse input character by character and breaks them into tokens
"""
from constrictor.error import IllegalCharError, Position
from constrictor.grammar import *


# token: simple object with a type and value
class Token:
    def __init__(self, type_, value=None, pos_start=None, pos_end=None):
        self.type = type_
        self.value = value

        if pos_start:
            self.pos_start = pos_start.copy()
            self.pos_end = pos_start.copy()
            self.pos_end.advance()

        if pos_end:
            self.pos_end = pos_end

    def __repr__(self):
        # print type and value if token has a value
        if self.value:
            return f"{self.type}:{self.value}"
        # else print token's type
        return f"{self.type}"


class Lexer:
    def __init__(self, file_name, text):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, file_name, text)  # init position out of array
        self.current_char = None
        self.advance()

    # advance character by character
    def advance(self):
        self.pos.advance(self.current_char)
        self.current_char = (
            self.text[self.pos.idx] if self.pos.idx < len(self.text) else None
        )

    # check for char type and turn it into corresponding token
    def make_tokens(self):
        tokens = []

        while self.current_char != None:
            # ignore spaces and tabs
            if self.current_char in " \t":
                self.advance()
            # add digit
            elif self.current_char in DIGITS:
                # create a number
                tokens.append(self.make_number())
                self.advance()
            # add operators
            elif self.current_char == "+":
                tokens.append(Token(PLUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "-":
                tokens.append(Token(MINUS, pos_start=self.pos))
                self.advance()
            elif self.current_char == "*":
                tokens.append(Token(MUL, pos_start=self.pos))
                self.advance()
            elif self.current_char == "/":
                tokens.append(Token(DIV, pos_start=self.pos))
                self.advance()
            elif self.current_char == "(":
                tokens.append(Token(LPAREN, pos_start=self.pos))
                self.advance()
            elif self.current_char == ")":
                tokens.append(Token(RPAREN, pos_start=self.pos))
                self.advance()
            # if char type illegal, return empty list and error
            else:
                pos_start = self.pos.copy()
                char = self.current_char
                self.advance()
                return [], IllegalCharError(pos_start, self.pos, f"'{char}'")

        tokens.append(Token(EOF, pos_start=self.pos))
        return tokens, None

    # turn string input into number
    def make_number(self):
        num_str = ""
        dot_count = 0
        pos_start = self.pos.copy()

        while self.current_char != None and self.current_char in DIGITS + ".":
            if self.current_char == ".":
                # make sure there is only one "." in float number
                if dot_count == 1:
                    break
                dot_count += 1

            num_str += self.current_char
            self.advance()

        # turn number into integer or float
        if dot_count == 0:
            return Token(INT, int(num_str), pos_start, self.pos)
        else:
            return Token(FLOAT, float(num_str), pos_start, self.pos)
