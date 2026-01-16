"""
ParseTree class + methods (evaluate, print)
"""
from dask_core.tree_node import TreeNode
from dask_core.evaluator import Evaluator
from features.optimiser import apply_identity_rules, apply_zero_rules
class ParseTree:
    def __init__(self, root=None):
        self.original_root = root
        self.optimised_root = None
    
    def evaluate(self, evaluator = Evaluator(), context = None):
        root = self.optimised_root if self.optimised_root is not None else self.original_root
        if root is None:
            return None
        
        return evaluator.eval_node(root, context)
    
    def print_rotated(self, node: TreeNode = None, level: int = 0):
        if node is None:
            node = self.original_root

        if node.right:
            self.print_rotated(node.right, level + 1)
        print("    " * level + str(node.value))
        if node.left:
            self.print_rotated(node.left, level + 1)

    def printInOrder(self, node: TreeNode = None, level: int = 0):
        if node is None:
            node = self.original_root
        if node is None:
            return
        if node.right:
            self.printInOrder(node.right, level + 1)
        print(str('.'*level) + str(node.value))
        if node.left:
            self.printInOrder(node.left, level + 1)

    def optimise(self, node: TreeNode = None):
        evaluator = Evaluator()

        def to_number(value):
            return float(value) if isinstance(value, str) else float(value)

        # Use post-order traversal to simplify each subtree
        is_root_call = node is None
        if node is None:
            node = self.original_root
        if node is None:
            self.optimised_root = None
            return None

        if node.left is not None:
            node.left = self.optimise(node.left)
        if node.right is not None:
            node.right = self.optimise(node.right)

        if node.is_leaf():
            return node

        if node.is_operator():
            left = node.left
            right = node.right
            left_is_num = left is not None and left.is_leaf() and left.is_number()
            right_is_num = right is not None and right.is_leaf() and right.is_number()

            # Constant folding (only when both are numbers)
            if left_is_num and right_is_num:
                folded = evaluator._apply_operator(node.value, to_number(left.value), to_number(right.value))
                result = TreeNode(folded)
                if is_root_call:
                    self.optimised_root = result
                return result

            # Identity rules
            identity_replacement = apply_identity_rules(node, left_is_num, right_is_num, to_number)
            if identity_replacement is not None:
                if is_root_call:
                    self.optimised_root = identity_replacement
                return identity_replacement

            # Zero rules
            zero_replacement = apply_zero_rules(node, left_is_num, right_is_num, to_number)
            if zero_replacement is not None:
                if is_root_call:
                    self.optimised_root = zero_replacement
                return zero_replacement

        if is_root_call:
            self.optimised_root = node
        return node
    
    def display_optimised_root(self, node: TreeNode = None, level: int = 0):
        if node is None:
            node = self.optimised_root
        if node is None:
            return
        if node.left:
            self.display_optimised_root(node.left, level + 1)
        print(str('.'*level) + str(node.value))
        if node.right:
            self.display_optimised_root(node.right, level + 1)
