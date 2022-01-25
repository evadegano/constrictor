"""
  PARSER: organize tokens into AST (abstract syntax tree)
"""
from constrictor.lexer import Lexer
from constrictor.grammar import *



# takes in a token of type number
class NumberNode:
  def __init__(self, token):
    self.token = token
  
  def __repr__(self):
    return f"{self.token}"


# takes in a binary operation
class BinOpNode:
  def __init__(self, left_node, operator, right_node):
    self.left_node = left_node
    self.operator = operator
    self.right_node = right_node

  def __repr__(self):
    return f"({self.left_node}, {self.operator}, {self.right_node})"


class Parser:
  def __init__(self, tokens):
    self.tokens = tokens
    self.token_idx = -1
    self.advance()


  # go through list of tokens, one at a time
  def advance(self):
    self.token_idx += 1

    if self.token_idx < len(self.tokens):
      self.current_token = self.tokens[self.token_idx]
    
    return self.current_token


  def parse(self):
    result = self.expression()
    return result


  # parse factors
  def factor(self):
    token = self.current_token

    # make sure that token is a number and turn into number node
    if token.type in (INT, FLOAT):
      self.advance()
      return NumberNode(token)


  # turn list of tokens into a binary expression
  def binary_expression(self, function, operators):
    left_node = function()

    while self.current_token.type in operators:
      operator = self.current_token
      self.advance()
      right_node = function()
      left_node = BinOpNode(left_node, operator, right_node)

    return left_node


  # parse terms
  def term(self):
    return self.binary_expression(self.factor, (MUL, DIV))


  # parse expressions
  def expression(self):
    return self.binary_expression(self.term, (PLUS, MINUS))



def run(file_name, text):
  # generate tokens
  lexer = Lexer(file_name, text)
  tokens, error = lexer.make_tokens()

  if error: return None, error

  # generate AST
  parser = Parser(tokens)
  ast = parser.parse()

  return ast, None