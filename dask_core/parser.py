"""
Builds parse tree from tokens
"""
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
        
        expr = tokenize(expr)

        operator_stack = Stack()
        node_stack = Stack()
        i = 0
        while i < len(expr):
            if expr[i] == '(':
                pass
            elif expr[i] == ')':
                operator = operator_stack.pop()
                leftnode = node_stack.pop()
                rightnode = node_stack.pop()
            
                subtree = TreeNode(operator, leftnode, rightnode)
                node_stack.push(subtree)
            elif expr[i] in self.operators:
                operator_stack.push(expr[i])
            else:
                node_stack.push(TreeNode(expr[i]))
            i += 1
        return ParseTree(node_stack.pop())
            