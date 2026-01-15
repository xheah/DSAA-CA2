"""
Handles evaluating trees, special ops (++ , //, **)
"""
from dask_core.tree_node import TreeNode
class Evaluator:
    def __init__(self):
        pass

    def _sum_to(self, n: int) -> int:
        return n * (n + 1) // 2
    
    def _apply_operator(self, op, left_val, right_val):
        if left_val is None or right_val is None:
            return None
        if op == '+':
            return left_val + right_val
        if op == '-':
            return left_val - right_val
        if op == '*':
            return left_val * right_val
        if op == '/':
            return left_val / right_val
        if op == '++':
            return self._sum_to(left_val) + self._sum_to(right_val)            
        if op == '//':
            return self._sum_to(left_val) / self._sum_to(right_val)
        if op == '**':
            return left_val**right_val
    
    def eval_node(self, node: TreeNode, context: dict) -> float | None:
        """
        Docstring for eval_node
        
        :param self: Description
        :param node: Root Node to begin evaluating
        :type node: TreeNode
        :param context: dict[var_name, expression]
        :type context: dict
        :return: Description
        :rtype: float | None
        """
        if node.is_leaf():
            if isinstance(node.value, int):
                return node.value
            else:
                expression = context[node.value]
                parse_tree = expression.parse_tree
                node = parse_tree.root
                self.eval_node(node, context)
                
        else:
            return self._apply_operator(node.value, self.eval_node(node.left, context), self.eval_node(node.right, context))

