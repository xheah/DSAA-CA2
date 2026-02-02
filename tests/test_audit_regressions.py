import sys
from pathlib import Path

import pytest

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.expression_manager import ExpressionManager
from dask_core.lexer import tokenize
from dask_core.parser import ExpressionParser
from dask_core.evaluator import Evaluator
from dask_core.tree_node import TreeNode
from io_utils.file_handler import FileHandler


def test_happy_path_evaluate_simple_expression():
    em = ExpressionManager()
    em.add_expression("a", "(1+2)")
    em.evaluate_all()
    assert em.expressions["a"].value == 3


def test_validate_rejects_invalid_number_format():
    em = ExpressionManager()
    msg, ok, _, _ = em.validate_expression("a=(1..2+3)")
    assert ok is False
    assert "Invalid number format" in msg


def test_validate_rejects_empty_expression():
    em = ExpressionManager()
    msg, ok, _, _ = em.validate_expression("a= ")
    assert ok is False
    assert "Expression cannot be empty" in msg


def test_tokenize_rejects_invalid_decimal_token():
    with pytest.raises(ValueError):
        tokenize("(1.+2)")


def test_tokenize_supports_underscores_in_variables():
    tokens = tokenize("(a_b+1)")
    assert "a_b" in tokens
    assert "_" not in tokens


def test_parser_rejects_non_fully_parenthesized_expression():
    parser = ExpressionParser()
    with pytest.raises(Exception):
        parser.parse("(1+2*3)")


def test_evaluator_div_by_zero_returns_none():
    evaluator = Evaluator()
    node = TreeNode("/", TreeNode(1), TreeNode(0))
    assert evaluator.eval_node(node, context={}) is None


def test_underscore_variable_name_roundtrip():
    em = ExpressionManager()
    em.add_expression("a_b", "(1+2)")
    em.evaluate_all()
    assert em.expressions["a_b"].value == 3


def test_stress_deeply_nested_parse():
    depth = 200
    expr = "1"
    for _ in range(depth):
        expr = f"({expr}+1)"
    parser = ExpressionParser()
    tree = parser.parse(expr)
    assert tree is not None


def test_file_handler_read_file_mock(monkeypatch):
    fh = FileHandler()

    class FakePath:
        def __init__(self, text):
            self._text = text
            self.name = "mock.txt"

        def read_text(self, encoding=None):
            return self._text

    monkeypatch.setattr("builtins.input", lambda _: "mock.txt")
    monkeypatch.setattr(Path, "rglob", lambda _self, _pattern: [FakePath("a=(1+2)")])
    content = fh.read_file()
    assert content == "a=(1+2)"
