from constrictor.lexer import Lexer
from constrictor.parser import Parser
from constrictor.interpreter import Interpreter, Context


def run(file_name, text):
    # generate tokens
    lexer = Lexer(file_name, text)
    tokens, error = lexer.make_tokens()
    if error:
        return None, error

    # generate AST
    parser = Parser(tokens)
    ast = parser.parse()
    if ast.error:
        return None, ast.error

    # run program
    interpreter = Interpreter()
    context = Context("<program>")  # root context
    result = interpreter.visit(ast.node, context)

    return result.value, result.error
