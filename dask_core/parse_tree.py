"""
ParseTree class + methods (evaluate, print)
"""
from dask_core.tree_node import TreeNode
from dask_core.evaluator import Evaluator
class ParseTree:
    def __init__(self, root=None):
        self.root = root
    
    def evaluate(self, evaluator = Evaluator(), context = None):
        if self.root is None:
            return None
        
        return evaluator.eval_node(self.root, context)
    
    def print_rotated(self, node: TreeNode = None, level: int = 0):
        if node is None:
            node = self.root

        if node.right:
            self.print_rotated(node.right, level + 1)
        print("    " * level + str(node.value))
        if node.left:
            self.print_rotated(node.left, level + 1)
