"""
  INTERPRETER: traverse code and make sense of it
"""
from constrictor.grammar import *


# to traceback context of an error
class Context:
    def __init__(self, display_name, parent=None, parent_entry_pos=None):
        self.display_name = display_name  # displayed name of the context
        self.parent = parent  # parent context of the current context
        self.parent_entry_pos = parent_entry_pos  # entry position of context change


class RuntimeResult:
    def __init__(self):
        self.value = None
        self.error = None

    def register(self, result):
        if result.error:
            self.error = result.error
        return result.value

    def success(self, value):
        self.value = value
        return self

    def failure(self, error):
        self.error = error
        return self


class Number:
    def __init__(self, value):
        self.value = value
        self.set_pos()
        self.set_context()

    def __repr__(self):
        return str(self.value)

    # store position to pin point potential errors
    def set_pos(self, pos_start=None, pos_end=None):
        self.pos_start = pos_start
        self.pos_end = pos_end
        return self

    # store context to traceback potential errors
    def set_context(self, context=None):
        self.context = context
        return self

    # process additions
    def added_to(self, other):
        # make sure the other object is a number
        if isinstance(other, Number):
            return Number(self.value + other.value).set_context(self.context), None

    # process substractions
    def subbed_by(self, other):
        # make sure the other object is a number
        if isinstance(other, Number):
            return Number(self.value - other.value).set_context(self.context), None

    # process multiplications
    def mult_by(self, other):
        # make sure the other object is a number
        if isinstance(other, Number):
            return Number(self.value * other.value).set_context(self.context), None

    # process divisions
    def div_by(self, other):
        # make sure the other object is a number
        if isinstance(other, Number):
            # check for div by 0 error
            if other.value == 0:
                return None, RuntimeError(
                    other.pos_start,
                    other.pos_start,
                    "Cannot divided by 0.",
                    self.context,
                )

            return Number(self.value / other.value).set_context(self.context), None


class Interpreter:
    # process node and visit children node
    def visit(self, node, context):
        # declare a unique method name for each node
        method_name = f"visit_{type(node).__name__}"
        method = getattr(self, method_name, self.no_visit_method)

        return method(node, context)

    def no_visit_method(self, node, context):
        raise Exception(f"No visit_{type(node).__name__} method defined")

    # process number node
    def visit_NumberNode(self, node, context):
        return RuntimeResult().success(
            # turn node into number
            Number(node.token.value)
            .set_context(context)
            .set_pos(node.pos_start, node.pos_end)
        )

    # process binary operation node
    def visit_BinOpNode(self, node, context):
        res = RuntimeResult()
        left = res.register(self.visit(node.left_node, context))
        if res.error:
            return res

        right = res.register(self.visit(node.right_node, context))
        if res.error:
            return res

        # process addition
        if node.operator.type == PLUS:
            result, error = left.added_to(right)

        # process substraction
        if node.operator.type == MINUS:
            result, error = left.subbed_by(right)

        # process multiplication
        if node.operator.type == MUL:
            result, error = left.mult_by(right)

        # process division
        if node.operator.type == DIV:
            result, error = left.div_by(right)

        if error:
            return res.failure(error)
        else:
            return res.success(result.set_pos(node.pos_start, node.pos_end))

    # process unary operation node
    def visit_UnaryOpNode(self, node, context):
        result = RuntimeResult()
        number = result.register(self.visit(node.node, context))
        if result.error:
            return result

        error = None

        # multiply number by -1
        if node.operator.type == MINUS:
            number, error = number.mult_by(Number(-1))

        if error:
            return result.failure(error)
        else:
            return result.success(number.set_pos(node.pos_start, node.pos_end))
