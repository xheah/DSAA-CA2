import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.tree_node import TreeNode
from dask_core.evaluator import Evaluator
import pytest


class TestEvaluator:
    """Test suite for the Evaluator class."""

    @pytest.fixture
    def evaluator(self):
        """Fixture to create an Evaluator instance."""
        return Evaluator()

    def test_evaluator_init(self):
        """Test Evaluator initialization."""
        evaluator = Evaluator()
        assert evaluator is not None

    def test_sum_to_zero(self, evaluator):
        """Test _sum_to() with 0."""
        result = evaluator._sum_to(0)
        assert result == 0

    def test_sum_to_one(self, evaluator):
        """Test _sum_to() with 1."""
        result = evaluator._sum_to(1)
        assert result == 1

    def test_sum_to_five(self, evaluator):
        """Test _sum_to() with 5."""
        result = evaluator._sum_to(5)
        assert result == 15  # 1+2+3+4+5 = 15

    def test_sum_to_ten(self, evaluator):
        """Test _sum_to() with 10."""
        result = evaluator._sum_to(10)
        assert result == 55  # 1+2+...+10 = 55

    def test_sum_to_negative(self, evaluator):
        """Test _sum_to() with negative number."""
        result = evaluator._sum_to(-5)
        assert result == 10  # -5 * (-5 + 1) / 2 = -10

    def test_apply_operator_addition(self, evaluator):
        """Test _apply_operator() with +."""
        result = evaluator._apply_operator('+', 5, 3)
        assert result == 8

    def test_apply_operator_subtraction(self, evaluator):
        """Test _apply_operator() with -."""
        result = evaluator._apply_operator('-', 5, 3)
        assert result == 2

    def test_apply_operator_multiplication(self, evaluator):
        """Test _apply_operator() with *."""
        result = evaluator._apply_operator('*', 5, 3)
        assert result == 15

    def test_apply_operator_division(self, evaluator):
        """Test _apply_operator() with /."""
        result = evaluator._apply_operator('/', 10, 2)
        assert result == 5.0

    def test_apply_operator_double_plus(self, evaluator):
        """Test _apply_operator() with ++."""
        # ++ means sum_to(left) + sum_to(right)
        # sum_to(3) = 6, sum_to(4) = 10, so 6 + 10 = 16
        result = evaluator._apply_operator('++', 3, 4)
        assert result == 16

    def test_apply_operator_double_slash(self, evaluator):
        """Test _apply_operator() with //."""
        # // means sum_to(left) / sum_to(right)
        # sum_to(3) = 6, sum_to(2) = 3, so 6 / 3 = 2.0
        result = evaluator._apply_operator('//', 3, 2)
        assert result == 2.0

    def test_apply_operator_double_star(self, evaluator):
        """Test _apply_operator() with **."""
        result = evaluator._apply_operator('**', 2, 3)
        assert result == 8  # 2^3 = 8

    def test_apply_operator_none_left(self, evaluator):
        """Test _apply_operator() with None as left value."""
        result = evaluator._apply_operator('+', None, 5)
        assert result is None

    def test_apply_operator_none_right(self, evaluator):
        """Test _apply_operator() with None as right value."""
        result = evaluator._apply_operator('+', 5, None)
        assert result is None

    def test_apply_operator_both_none(self, evaluator):
        """Test _apply_operator() with both values None."""
        result = evaluator._apply_operator('+', None, None)
        assert result is None

    def test_eval_node_leaf_integer(self, evaluator):
        """Test eval_node() with a leaf node containing an integer."""
        node = TreeNode(5)
        context = {}
        result = evaluator.eval_node(node, context)
        assert result == 5

    def test_eval_node_leaf_float_string(self, evaluator):
        """Test eval_node() with a leaf node containing a float string."""
        node = TreeNode("3.5")
        context = {}
        result = evaluator.eval_node(node, context)
        assert result == 3.5

    def test_eval_node_leaf_string(self, evaluator):
        """Test eval_node() with a leaf node containing a string variable."""
        # Create a mock expression for the context
        from dask_core.expression import DaskExpression
        
        # Use variable names, not numbers, since numbers in parse tree are strings
        # and the evaluator tries to look them up in context
        # Also need to provide values for nested variables
        expr = DaskExpression("Alpha", "(X+Y)")
        # Create nested expressions for X and Y
        expr_x = DaskExpression("X", "5")
        expr_y = DaskExpression("Y", "3")
        context = {"Alpha": expr, "X": expr_x, "Y": expr_y}
        
        node = TreeNode("Alpha")
        result = evaluator.eval_node(node, context)
        assert result == 8

    def test_eval_node_operator_addition(self, evaluator):
        """Test eval_node() with an addition operator."""
        node = TreeNode("+", TreeNode(5), TreeNode(3))
        context = {}
        result = evaluator.eval_node(node, context)
        assert result == 8

    def test_eval_node_operator_subtraction(self, evaluator):
        """Test eval_node() with a subtraction operator."""
        node = TreeNode("-", TreeNode(10), TreeNode(3))
        context = {}
        result = evaluator.eval_node(node, context)
        assert result == 7

    def test_eval_node_operator_multiplication(self, evaluator):
        """Test eval_node() with a multiplication operator."""
        node = TreeNode("*", TreeNode(5), TreeNode(4))
        context = {}
        result = evaluator.eval_node(node, context)
        assert result == 20

    def test_eval_node_operator_division(self, evaluator):
        """Test eval_node() with a division operator."""
        node = TreeNode("/", TreeNode(15), TreeNode(3))
        context = {}
        result = evaluator.eval_node(node, context)
        assert result == 5.0

    def test_eval_node_operator_double_plus(self, evaluator):
        """Test eval_node() with ++ operator."""
        node = TreeNode("++", TreeNode(3), TreeNode(4))
        context = {}
        result = evaluator.eval_node(node, context)
        assert result == 16  # sum_to(3) + sum_to(4) = 6 + 10 = 16

    def test_eval_node_operator_double_slash(self, evaluator):
        """Test eval_node() with // operator."""
        node = TreeNode("//", TreeNode(3), TreeNode(2))
        context = {}
        result = evaluator.eval_node(node, context)
        assert result == 2.0  # sum_to(3) / sum_to(2) = 6 / 3 = 2.0

    def test_eval_node_operator_double_star(self, evaluator):
        """Test eval_node() with ** operator."""
        node = TreeNode("**", TreeNode(2), TreeNode(3))
        context = {}
        result = evaluator.eval_node(node, context)
        assert result == 8  # 2^3 = 8

    def test_eval_node_nested_expression(self, evaluator):
        """Test eval_node() with a nested expression."""
        # Tree: (5 + (3 * 2))
        node = TreeNode("+", TreeNode(5), TreeNode("*", TreeNode(3), TreeNode(2)))
        context = {}
        result = evaluator.eval_node(node, context)
        assert result == 11  # 5 + (3 * 2) = 5 + 6 = 11

    def test_eval_node_complex_expression(self, evaluator):
        """Test eval_node() with a complex expression."""
        # Tree: ((10 + 5) * (20 / 4))
        node = TreeNode("*",
                        TreeNode("+", TreeNode(10), TreeNode(5)),
                        TreeNode("/", TreeNode(20), TreeNode(4)))
        context = {}
        result = evaluator.eval_node(node, context)
        assert result == 75.0  # (10 + 5) * (20 / 4) = 15 * 5 = 75

    def test_eval_node_with_variable_reference(self, evaluator):
        """Test eval_node() with variable references in context."""
        from dask_core.expression import DaskExpression

        expr_a = DaskExpression("A", "(X+Y)")
        expr_b = DaskExpression("B", "(Z*W)")

        context = {"A": expr_a, "B": expr_b}
        node = TreeNode("+", TreeNode("A"), TreeNode("B"))
        result = evaluator.eval_node(node, context)
        assert result is None

    def test_eval_node_missing_variables_returns_none(self, evaluator):
        """Test eval_node() returns None when variables are missing."""
        from dask_core.expression import DaskExpression

        expr_a = DaskExpression("A", "(C+D)")
        context = {"A": expr_a}
        node = TreeNode("A")

        result = evaluator.eval_node(node, context)
        assert result is None

