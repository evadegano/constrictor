"""
  INTERPRETER: traverse code and 
"""

class Interpreter:
  # process node and visit children node
  def visit(self, node):
    # visit binary operator node
    method_name = f"visit_{type(node)}"