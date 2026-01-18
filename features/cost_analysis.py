"""
Cost Analysis for changes between original tree and optimised tree
Metrics:
    node_count: total nodes
    operator_count: internal operator nodes
    leaf_count: numbers + variables
    tree_height / max_depth
    weighted op cost: 
            +, - -> 1
            *, / -> 2
            ** -> 3
            ++, // -> 3 (summative is heavier)
        not true runtime, just a relative cost model 
"""

from dask_core.tree_node import TreeNode
from dask_core.parse_tree import ParseTree

class CostAnalyser:
    def __init__(self, tree: ParseTree = None):
        self.tree = tree
        self.statistics = {}
        
        # Define metrics to compute for both original and optimised roots
        metrics = [
            ('total_nodes', 'count_nodes', 'all'),
            ('operator_nodes', 'count_nodes', 'operator'),
            ('leaf_nodes', 'count_nodes', 'leaf'),
            ('tree_height', 'count_tree_height'),
            ('weighted_op_cost', 'count_weighted_op_cost'),
        ]
        
        # Compute metrics for both roots
        for root_type in ['original', 'optimised']:
            root = getattr(self.tree, f'{root_type}_root')
            for suffix, method_name, *args in metrics:
                key = f'{root_type}_{suffix}'
                method = getattr(self, method_name)
                self.statistics[key] = method(root, *args)

    def count_nodes(self, root: TreeNode, count_type: str = "all") -> int:
        """
        Count nodes based on type.

        count_type:
            - "all": all nodes
            - "operator": operator nodes only
            - "leaf": leaf nodes only
        """
        if root is None:
            return 0

        match count_type:
            case "all":
                count = 1
            case "operator":
                count = 1 if root.is_operator() else 0
            case "leaf":
                count = 1 if root.is_leaf() else 0
            case _:
                raise ValueError(f"Unknown count_type: {count_type}")

        if root.left:
            count += self.count_nodes(root.left, count_type)
        if root.right:
            count += self.count_nodes(root.right, count_type)
        return count

    def count_tree_height(self, root: TreeNode) -> int:
        """
        Measure the height (max depth) of a tree.
        """
        if root is None:
            return 0
        left_height = self.count_tree_height(root.left)
        right_height = self.count_tree_height(root.right)
        return 1 + max(left_height, right_height)
    
    def count_weighted_op_cost(self, root: TreeNode) -> int:
        if root is None:
            return 0
        
        left_cost = self.count_weighted_op_cost(root.left) if root.left else 0
        right_cost = self.count_weighted_op_cost(root.right) if root.right else 0

        if root.is_operator():
            match root.value:
                case '+' | '-':
                    return 1 + left_cost + right_cost
                case '*' | '/':
                    return 2 + left_cost + right_cost
                case '**':
                    return 3 + left_cost + right_cost
                case '++' | '//':
                    return 3 + left_cost + right_cost
            return left_cost + right_cost
        return left_cost + right_cost