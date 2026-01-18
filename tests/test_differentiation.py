import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.tree_node import TreeNode
from features.differentiation import differentiate, UnsupportedOperatorError


class TestDifferentiation:
    def test_differentiate_constant(self):
        node = TreeNode("5")
        result = differentiate(node, "x")
        assert result.optimised_root.value == 0

    def test_differentiate_variable(self):
        node = TreeNode("x")
        result = differentiate(node, "x")
        assert result.optimised_root.value == 1

        node_other = TreeNode("y")
        result_other = differentiate(node_other, "x")
        assert result_other.optimised_root.value == 0

    def test_differentiate_addition(self):
        node = TreeNode("+", TreeNode("x"), TreeNode("3"))
        result = differentiate(node, "x")
        assert result.optimised_root.value == 1

    def test_differentiate_product(self):
        node = TreeNode("*", TreeNode("x"), TreeNode("x"))
        result = differentiate(node, "x")
        assert result.optimised_root.value == "+"

    def test_differentiate_quotient(self):
        node = TreeNode("/", TreeNode("x"), TreeNode("2"))
        result = differentiate(node, "x")
        assert result.optimised_root.value == 0.5

    def test_differentiate_power_constant_exponent(self):
        node = TreeNode("**", TreeNode("x"), TreeNode("3"))
        result = differentiate(node, "x")
        assert result.optimised_root.value == "*"
        assert result.optimised_root.left.value == 3.0 or result.optimised_root.left.value == 3

    def test_differentiate_unsupported_operator(self):
        node = TreeNode("++", TreeNode("x"), TreeNode("2"))
        with pytest.raises(UnsupportedOperatorError):
            differentiate(node, "x")

    def test_differentiate_unsupported_power(self):
        node = TreeNode("**", TreeNode("x"), TreeNode("y"))
        with pytest.raises(UnsupportedOperatorError):
            differentiate(node, "x")

    def test_differentiate_non_operator_node(self):
        node = TreeNode("?", TreeNode("x"), TreeNode("2"))
        with pytest.raises(ValueError):
            differentiate(node, "x")

    def test_differentiate_beta_wrt_alpha(self):
        """
        Alpha=(8*4)
        Beta=((4*Alpha*Alpha+Alpha**5)+6)
        Differentiate Beta w.r.t. Alpha
        """
        beta_tree = TreeNode(
            "+",
            TreeNode(
                "+",
                TreeNode(
                    "*",
                    TreeNode("*", TreeNode("4"), TreeNode("Alpha")),
                    TreeNode("Alpha"),
                ),
                TreeNode("**", TreeNode("Alpha"), TreeNode("5")),
            ),
            TreeNode("6"),
        )
        result = differentiate(beta_tree, "Alpha")
        assert result is not None
        assert result.optimised_root is not None
        assert result.count_x_variable("Alpha") > 0
