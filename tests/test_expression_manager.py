import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.expression_manager import ExpressionManager
import pytest


class TestExpressionManager:
    """Test suite for the ExpressionManager class."""

    def test_expression_manager_init(self):
        """Test ExpressionManager initialization."""
        manager = ExpressionManager()
        assert manager is not None
        assert manager.parser is not None
        assert manager.expressions == {}

    def test_expression_manager_expressions_dict(self):
        """Test that expressions is initialized as an empty dict."""
        manager = ExpressionManager()
        assert isinstance(manager.expressions, dict)
        assert len(manager.expressions) == 0

    def test_expression_manager_has_parser(self):
        """Test that parser is initialized."""
        manager = ExpressionManager()
        assert manager.parser is not None
        assert hasattr(manager.parser, 'parse')

    def test_expression_manager_attributes(self):
        """Test that all expected attributes exist."""
        manager = ExpressionManager()
        assert hasattr(manager, 'expressions')
        assert hasattr(manager, 'parser')

    def test_expression_manager_multiple_instances(self):
        """Test creating multiple ExpressionManager instances."""
        manager1 = ExpressionManager()
        manager2 = ExpressionManager()
        
        assert manager1 is not manager2
        assert manager1.expressions is not manager2.expressions
        assert manager1.parser is not manager2.parser

    def test_expression_manager_evaluates_with_existing_variables(self):
        """Test evaluating a=(c+d) when c and d exist in ExpressionManager."""
        manager = ExpressionManager()
        manager.add_expression("c", "5")
        manager.add_expression("d", "3")
        manager.add_expression("a", "(c+d)")

        manager.evaluate_all()

        assert manager.expressions["a"].value == 8

    def test_expression_manager_modify_existing_expression(self):
        """Test modifying an existing expression overwrites the old one."""
        manager = ExpressionManager()
        manager.add_expression("a", "(1+2)")
        manager.evaluate_all()
        first_value = manager.expressions["a"].value

        manager.add_expression("a", "(3+4)")
        manager.evaluate_all()

        assert manager.expressions["a"].expression == "(3+4)"
        assert manager.expressions["a"].value == 7
        assert first_value != manager.expressions["a"].value

    def test_validate_expression_allows_decimals(self):
        """Test that decimal operands are accepted."""
        manager = ExpressionManager()
        message, result, name, expr = manager.validate_expression("a=(1.5+2.25)")
        assert result is True
        assert message == ""
        assert name == "a"
        assert expr == "(1.5+2.25)"

    def test_validate_expression_rejects_negative_numbers(self):
        """Test that negative numbers are rejected."""
        manager = ExpressionManager()
        message, result, _, _ = manager.validate_expression("a=(-1+2)")
        assert result is False
        assert "Negative numbers" in message
