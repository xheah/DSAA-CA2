"""
Builds parse tree from tokens
"""
import re
from dask_core.lexer import tokenize
from dask_core.parse_tree import ParseTree
from dask_core.data_structures.stack import Stack
from dask_core.tree_node import TreeNode
class ExpressionParser:
    """
    ExpressionParser to turn a string (2+(4*5)) into a ParseTree
    """
    def __init__(self):
        self.operators = ['+', '-', '*', '/', '++', '**', '//']
    
    def parse(self, expr: str = None) -> ParseTree:
        if expr is None:
            return None
        expr = expr.strip()
        if expr == "":
            raise ValueError("Invalid expression format.")

        def wraps_entire(s: str) -> bool:
            depth = 0
            for i, ch in enumerate(s):
                if ch == '(':
                    depth += 1
                elif ch == ')':
                    depth -= 1
                    if depth == 0 and i != len(s) - 1:
                        return False
                if depth < 0:
                    return False
            return depth == 0

        def is_single_value(s: str) -> bool:
            s = s.strip()
            if re.fullmatch(r"[a-zA-Z_]+", s):
                return True
            if re.fullmatch(r"(\d+(\.\d*)?|\.\d+)", s):
                return True
            if s.startswith("(") and s.endswith(")") and wraps_entire(s):
                return is_single_value(s[1:-1])
            return False

        def unwrap_single_value(s: str) -> str:
            s = s.strip()
            if s.startswith("(") and s.endswith(")") and wraps_entire(s):
                return unwrap_single_value(s[1:-1])
            return s

        if is_single_value(expr):
            value = unwrap_single_value(expr)
            return ParseTree(TreeNode(value))

        expr = tokenize(expr)

        operator_stack = Stack()
        node_stack = Stack()
        i = 0
        while i < len(expr):
            if expr[i] == '(':
                pass
            elif expr[i] == ')':
                try:
                    operator = operator_stack.pop()
                    rightnode = node_stack.pop()
                    leftnode = node_stack.pop()
                except IndexError as exc:
                    raise ValueError("Invalid expression format.") from exc

                if operator in {'/', '//'} and rightnode.is_leaf() and rightnode.is_number():
                    if float(rightnode.value) == 0:
                        raise ZeroDivisionError("Division by zero.")
            
                subtree = TreeNode(operator, leftnode, rightnode)
                node_stack.push(subtree)
            elif expr[i] in self.operators:
                operator_stack.push(expr[i])
            else:
                node_stack.push(TreeNode(expr[i]))
            i += 1
        if operator_stack.size() != 0 or node_stack.size() != 1:
            raise ValueError("Invalid expression format.")
        return ParseTree(node_stack.pop())
            