"""
*Scope*
Supported Operators: + , - , * , / , **
Unsupported Operators: ++ , //

Only differentiation w.r.t. one variable
Power rule only when exponent is a constant number
Does not support differentiation of undefined variables

Derivatives are stored as a new variable
"""
from dask_core.tree_node import TreeNode
from dask_core.parse_tree import ParseTree

class UnsupportedOperatorError(Exception):
    """Exception raised for unsupported operators (++, //) in differentiation function"""
    pass

def _is_constant(node: TreeNode) -> bool:
    return node is not None and node.is_leaf() and node.is_number()


def _constant_value(node: TreeNode) -> float:
    return float(node.value)


def _differentiate_node(node: TreeNode, wrt: str):
    if node is None:
        return None

    # Leaf cases
    if node.is_leaf():
        if node.is_number():
            return TreeNode(0)
        if node.is_variable():
            return TreeNode(1 if node.value == wrt else 0)
        return None

    if not node.is_operator():
        raise ValueError("Non-leaf is not an operator.")

    op = node.value
    left = node.left
    right = node.right

    # Unsupported operators
    if op in {"++", "//"}:
        raise UnsupportedOperatorError("++ and // are not supported for differentation.")

    # Recursive rules
    if op == "+":
        left_d = _differentiate_node(left, wrt)
        right_d = _differentiate_node(right, wrt)
        if left_d is None or right_d is None:
            return None
        result = TreeNode("+", left_d, right_d)
    elif op == "-":
        left_d = _differentiate_node(left, wrt)
        right_d = _differentiate_node(right, wrt)
        if left_d is None or right_d is None:
            return None
        result = TreeNode("-", left_d, right_d)
    elif op == "*":
        # Product rule: (u*v)' = u'*v + u*v'
        left_d = _differentiate_node(left, wrt)
        right_d = _differentiate_node(right, wrt)
        if left_d is None or right_d is None:
            return None
        result = TreeNode(
            "+",
            TreeNode("*", left_d, right),
            TreeNode("*", left, right_d),
        )
    elif op == "/":
        # Quotient rule: (u/v)' = (u'*v - u*v') / v**2
        left_d = _differentiate_node(left, wrt)
        right_d = _differentiate_node(right, wrt)
        if left_d is None or right_d is None:
            return None
        numerator = TreeNode(
            "-",
            TreeNode("*", left_d, right),
            TreeNode("*", left, right_d),
        )
        denominator = TreeNode("**", right, TreeNode(2))
        result = TreeNode("/", numerator, denominator)
    elif op == "**":
        # Power rule only when exponent is a constant number
        if _is_constant(right):
            n = _constant_value(right)
            left_d = _differentiate_node(left, wrt)
            if left_d is None:
                return None
            result = TreeNode(
                "*",
                TreeNode(n),
                TreeNode("*", TreeNode("**", left, TreeNode(n - 1)), left_d),
            )
        else:
            raise UnsupportedOperatorError("Power rule only supports constant exponents.")
    else:
        return None

    return result


def differentiate(node: TreeNode, wrt: str):
    """
    Differentiate a parse tree rooted at node with respect to wrt.
    Returns an optimised ParseTree, or None if unsupported.
    """
    result = _differentiate_node(node, wrt)
    if result is None:
        return None

    tree = ParseTree(result)
    tree.optimise()
    if tree.optimised_root is None:
        tree.optimised_root = tree.original_root
    return tree
    