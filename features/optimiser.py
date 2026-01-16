"""
Expression Optimisation Engine
"""

from dask_core.tree_node import TreeNode


def apply_identity_rules(node: TreeNode, left_is_num: bool, right_is_num: bool, to_number):
    if node.value == '+':
        if right_is_num and to_number(node.right.value) == 0:
            return node.left
        if left_is_num and to_number(node.left.value) == 0:
            return node.right
    if node.value == '*':
        if left_is_num and to_number(node.left.value) == 1:
            return node.right
        if right_is_num and to_number(node.right.value) == 1:
            return node.left
    if node.value == '/':
        if right_is_num and to_number(node.right.value) == 1:
            return node.left
    if node.value == '**':
        if right_is_num and to_number(node.right.value) == 1:
            return node.left
        if right_is_num and to_number(node.right.value) == 0:
            return TreeNode(1)
    return None


def apply_zero_rules(node: TreeNode, left_is_num: bool, right_is_num: bool, to_number):
    if node.value == '*':
        if (left_is_num and to_number(node.left.value) == 0) or (right_is_num and to_number(node.right.value) == 0):
            return TreeNode(0)
    if node.value == '/':
        if left_is_num and to_number(node.left.value) == 0:
            if not right_is_num or to_number(node.right.value) != 0:
                return TreeNode(0)
    return None