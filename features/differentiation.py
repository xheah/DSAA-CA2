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


def _is_constant(node: TreeNode) -> bool:
    return node is not None and node.is_leaf() and node.is_number()


def _constant_value(node: TreeNode) -> float:
    return float(node.value)


def differentiate(node: TreeNode, wrt: str):
    """
    Differentiate a parse tree rooted at node with respect to wrt.
    Returns the optimised derivative TreeNode, or None if unsupported.
    """
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
        return None

    op = node.value
    left = node.left
    right = node.right

    # Unsupported operators
    if op in {"++", "//"}:
        return None

    # Recursive rules
    if op == "+":
        result = TreeNode("+", differentiate(left, wrt), differentiate(right, wrt))
    elif op == "-":
        result = TreeNode("-", differentiate(left, wrt), differentiate(right, wrt))
    elif op == "*":
        # Product rule: (u*v)' = u'*v + u*v'
        left_d = differentiate(left, wrt)
        right_d = differentiate(right, wrt)
        result = TreeNode(
            "+",
            TreeNode("*", left_d, right),
            TreeNode("*", left, right_d),
        )
    elif op == "/":
        # Quotient rule: (u/v)' = (u'*v - u*v') / v**2
        left_d = differentiate(left, wrt)
        right_d = differentiate(right, wrt)
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
            left_d = differentiate(left, wrt)
            result = TreeNode(
                "*",
                TreeNode(n),
                TreeNode("*", TreeNode("**", left, TreeNode(n - 1)), left_d),
            )
        else:
            return None
    else:
        return None

    # Optimise the derivative tree before returning
    tree = ParseTree(result)
    tree.optimise()
    return tree.optimised_root
    