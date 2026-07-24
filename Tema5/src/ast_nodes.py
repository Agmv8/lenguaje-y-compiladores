# src/ast_nodes.py

class ASTNode:
    """Clase base para todos los nodos del AST en UnegScript"""
    pass

class NumNode(ASTNode):
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f"NumNode({self.value})"

class VarNode(ASTNode):
    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return f"VarNode('{self.name}')"

class BinaryOpNode(ASTNode):
    def __init__(self, left, op, right):
        self.left = left    # ASTNode
        self.op = op        # str ('+', '*', '>', etc.)
        self.right = right  # ASTNode

    def __repr__(self):
        return f"BinaryOpNode({self.left}, '{self.op}', {self.right})"

class AssignNode(ASTNode):
    def __init__(self, var_name, expr):
        self.var_name = var_name # str
        self.expr = expr         # ASTNode

    def __repr__(self):
        return f"AssignNode('{self.var_name}', {self.expr})"

class IfNode(ASTNode):
    def __init__(self, condition, then_branch, else_branch=None):
        self.condition = condition    # ASTNode
        self.then_branch = then_branch# ASTNode
        self.else_branch = else_branch# ASTNode

    def __repr__(self):
        return f"IfNode(Cond: {self.condition}, Then: {self.then_branch}, Else: {self.else_branch})"