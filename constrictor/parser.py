"""
  PARSER: organize tokens into AST (abstract syntax tree)
"""
from ast import Expression
from constrictor.lexer import Lexer
from constrictor.error import InvalidSyntaxError
from constrictor.grammar import *



class ParseResult():
  def __init__(self):
    self.error = None
    self.node = None


  # 
  def register(self, result):
    # if result is a parse result, return its node
    if isinstance(result, ParseResult):
      if result.error: self.error = result.error
      return result.node
    
    return result


  def success(self, node):
    self.node = node
    return self


  def failure(self, error):
    self.error = error
    return self



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


class UnaryOpNode:
  def __init__(self, operator, node):
    self.operator = operator
    self.node = node

  def __repr__(self):
    return f"({self.operator}, {self.node})"


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

    if not result.error and self.current_token.type != EOF: 
      return result.failure(InvalidSyntaxError(
        self.current_token.pos_start,
        self.current_token.pos_end,
        "Expected '+', '-', '*' or '/'"
      ))

    return result


  # parse factors
  def factor(self):
    result = ParseResult()
    token = self.current_token

    # if token is a plus/minus operator, return unary expression
    if token.type in (PLUS, MINUS):
      result.register(self.advance())
      factor = result.register(self.factor())

      if result.error: return result
      return result.success(UnaryOpNode(token, factor))


    # if token is a number, return number node
    elif token.type in (INT, FLOAT):
      result.register(self.advance())
      return result.success(NumberNode(token))

    # if token is a "(", return an expression
    elif token.type == LPAREN:
      result.register(self.advance())
      expression = result.register(self.expression())

      if result.error: return result

      # look for a closing ")"
      if self.current_token.type == RPAREN:
        result.register(self.advance())
        return result.success(expression)
      else:
        return result.failure(InvalidSyntaxError(
          self.current_token.pos_start, 
          self.current_token.pos_end, 
          "Expected ')'"
          ))

    return result.failure(InvalidSyntaxError(
      token.pos_start, 
      token.pos_end, 
      "Expected integer or float"
      ))

  # turn list of tokens into a binary expression
  def binary_expression(self, function, operators):
    result = ParseResult()
    # assign left_node to a node instead of the whole parse result
    left_node = result.register(function())
    if result.error: return result

    while self.current_token.type in operators:
      operator = self.current_token
      result.register(self.advance())

      right_node = result.register(function())
      if result.error: return result

      left_node = BinOpNode(left_node, operator, right_node)

    return result.success(left_node)


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

  return ast.node, ast.error