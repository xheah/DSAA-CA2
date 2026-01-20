"""
ParseTree class + methods (evaluate, print)
"""
from dask_core.tree_node import TreeNode
from dask_core.evaluator import Evaluator
from features.optimiser import apply_identity_rules, apply_zero_rules
class ParseTree:
    def __init__(self, root=None):
        self.original_root = root
        self.optimised_root = self.optimise()
    
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
        if is_root_call:
            node = node.clone()

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

            # Identity and zero rules
            identity_replacement = apply_identity_rules(node, left_is_num, right_is_num, to_number)
            if identity_replacement is not None:
                if is_root_call:
                    self.optimised_root = identity_replacement
                return identity_replacement

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

    def count_x_variable(self, x, node: TreeNode = None):
        if node is None:
            node = self.optimised_root if self.optimised_root is not None else self.original_root
        if node is None:
            return 0

        count = 1 if node.is_variable() and node.value == x else 0
        if node.left:
            count += self.count_x_variable(x, node.left)
        if node.right:
            count += self.count_x_variable(x, node.right)

        return count

    def to_expression(self, root: str = "original") -> str:
        """
        Convert the parse tree back into its infix string format.

        root:
            - "original": original_root
            - "optimised": optimised_root
        """
        if root not in ["original", "optimised"]:
            raise ValueError("root must be original or optimised")

        node = self.original_root if root == "original" else self.optimised_root
        if node is None:
            return ""

        def _to_expr(n: TreeNode) -> str:
            if n is None:
                return ""
            if n.is_leaf():
                return str(n.value)
            left = _to_expr(n.left)
            right = _to_expr(n.right)
            return f"({left}{n.value}{right})"

        return _to_expr(node)