"""
Handles evaluating trees, special ops (++ , //, **)
"""
import re
from dask_core.tree_node import TreeNode
class Evaluator:
    def __init__(self):
        pass

    def _sum_to(self, n: float) -> float:
        return n * (n + 1) / 2
    
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
        number_re = re.compile(r'(\d+(\.\d*)?|\.\d+)$')
        if node.is_leaf():
            if isinstance(node.value, (int, float)):
                return node.value
            if isinstance(node.value, str):
                if number_re.fullmatch(node.value):
                    return float(node.value)
                if context is None:
                    return None
                if node.value not in context:
                    return None
                expression = context[node.value]
                if expression.parse_tree is None or expression.parse_tree.root is None:
                    return None
                return self.eval_node(expression.parse_tree.root, context)
            return None

        return self._apply_operator(
            node.value,
            self.eval_node(node.left, context),
            self.eval_node(node.right, context),
        )

