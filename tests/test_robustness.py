import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.expression_manager import ExpressionManager
from dask_core.parser import ExpressionParser


class TestRobustness:
    def test_division_by_zero_returns_none(self):
        em = ExpressionManager()
        em.add_expression("b", "1")
        em.add_expression("c", "0")
        em.add_expression("a", "(b/c)")
        em.evaluate_all()
        assert em.expressions["a"].value is None

    def test_empty_variable_name_rejected(self):
        em = ExpressionManager()
        msg, ok, _, _ = em.validate_expression("=(1+2)")
        assert ok is False
        assert "Invalid variable name" in msg

    def test_expression_with_extra_spaces(self):
        em = ExpressionManager()
        msg, ok, name, expr = em.validate_expression(" a = ( 1 + 2 ) ")
        assert ok is True
        assert name == "a"
        assert expr == "(1+2)"

    def test_max_nesting_depth_50(self):
        expr = "1"
        for _ in range(50):
            expr = f"({expr}+1)"
        parser = ExpressionParser()
        tree = parser.parse(expr)
        assert tree is not None
