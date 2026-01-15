import sys
from pathlib import Path
from unittest.mock import Mock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.expression import DaskExpression
from dask_core.parser import ExpressionParser
import pytest


class TestDaskExpression:
    """Test suite for the DaskExpression class."""

    def test_dask_expression_init(self):
        """Test DaskExpression initialization."""
        expr = DaskExpression("Alpha", "(A+B)")
        assert expr.name == "Alpha"
        assert expr.expression == "(A+B)"
        # Note: build_tree() is called automatically in __init__, so parse_tree is not None
        assert expr.parse_tree is not None
        assert expr.value is None

    def test_dask_expression_init_different_names(self):
        """Test DaskExpression initialization with different variable names."""
        expr1 = DaskExpression("Beta", "(C+D)")
        assert expr1.name == "Beta"
        
        expr2 = DaskExpression("Gamma", "(E*F)")
        assert expr2.name == "Gamma"

    def test_dask_expression_init_different_expressions(self):
        """Test DaskExpression initialization with different expressions."""
        expr1 = DaskExpression("Alpha", "(A+B)")
        assert expr1.expression == "(A+B)"
        
        expr2 = DaskExpression("Beta", "(C*D)")
        assert expr2.expression == "(C*D)"

    def test_dask_expression_build_tree_default_parser(self):
        """Test build_tree() with default parser."""
        expr = DaskExpression("Alpha", "(A+B)")
        expr.build_tree()
        assert expr.parse_tree is not None
        assert expr.parse_tree.root is not None
        assert expr.parse_tree.root.value == "+"

    def test_dask_expression_build_tree_custom_parser(self):
        """Test build_tree() with a custom parser."""
        parser = ExpressionParser()
        expr = DaskExpression("Alpha", "(A+B)")
        expr.build_tree(parser)
        assert expr.parse_tree is not None
        assert expr.parse_tree.root.value == "+"

    def test_dask_expression_build_tree_simple_expression(self):
        """Test build_tree() with a simple expression."""
        expr = DaskExpression("Alpha", "(5+3)")
        expr.build_tree()
        assert expr.parse_tree.root.value == "+"
        assert expr.parse_tree.root.left.value == "5"
        assert expr.parse_tree.root.right.value == "3"

    def test_dask_expression_build_tree_complex_expression(self):
        """Test build_tree() with a complex expression."""
        expr = DaskExpression("Beta", "(A+(B*C))")
        expr.build_tree()
        assert expr.parse_tree.root.value == "+"
        assert expr.parse_tree.root.left.value == "A"
        assert expr.parse_tree.root.right.value == "*"

    def test_dask_expression_build_tree_with_numbers(self):
        """Test build_tree() with numbers in expression."""
        expr = DaskExpression("Gamma", "(100+200)")
        expr.build_tree()
        assert expr.parse_tree.root.value == "+"
        assert expr.parse_tree.root.left.value == "100"
        assert expr.parse_tree.root.right.value == "200"

    def test_dask_expression_build_tree_with_multi_char_operators(self):
        """Test build_tree() with multi-character operators."""
        expr = DaskExpression("Delta", "(A++B)")
        expr.build_tree()
        assert expr.parse_tree.root.value == "++"

    def test_dask_expression_build_tree_multiple_times(self):
        """Test building tree multiple times (should overwrite)."""
        expr = DaskExpression("Alpha", "(A+B)")
        expr.build_tree()
        first_tree = expr.parse_tree
        
        expr.expression = "(C*D)"
        expr.build_tree()
        second_tree = expr.parse_tree
        
        assert first_tree != second_tree
        assert second_tree.root.value == "*"

    def test_dask_expression_evaluate_not_implemented(self):
        """Test evaluate() method (currently not implemented)."""
        expr = DaskExpression("Alpha", "(A+B)")
        expr.build_tree()
        
        # evaluate() is not implemented, so it should do nothing
        # Note: evaluate() now only takes evaluator parameter, no context
        from dask_core.evaluator import Evaluator
        evaluator = Evaluator()
        result = expr.evaluate(evaluator)
        assert result is None

    def test_dask_expression_value_initialized_as_none(self):
        """Test that value is initialized as None."""
        expr = DaskExpression("Alpha", "(A+B)")
        assert expr.value is None

    def test_dask_expression_parse_tree_initialized_as_none(self):
        """Test that parse_tree is built automatically on initialization."""
        expr = DaskExpression("Alpha", "(A+B)")
        # Note: build_tree() is called in __init__, so parse_tree is built automatically
        assert expr.parse_tree is not None
        assert expr.parse_tree.root is not None

    def test_dask_expression_attributes_accessible(self):
        """Test that all attributes are accessible."""
        expr = DaskExpression("Alpha", "(A+B)")
        assert hasattr(expr, 'name')
        assert hasattr(expr, 'expression')
        assert hasattr(expr, 'parse_tree')
        assert hasattr(expr, 'value')

    def test_dask_expression_multiple_instances(self):
        """Test creating multiple DaskExpression instances."""
        expr1 = DaskExpression("Alpha", "(A+B)")
        expr2 = DaskExpression("Beta", "(C*D)")
        expr3 = DaskExpression("Gamma", "(E/F)")
        
        assert expr1.name == "Alpha"
        assert expr2.name == "Beta"
        assert expr3.name == "Gamma"
        
        assert expr1.expression == "(A+B)"
        assert expr2.expression == "(C*D)"
        assert expr3.expression == "(E/F)"

