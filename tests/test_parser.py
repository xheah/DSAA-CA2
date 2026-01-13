import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.lexer import Lexer
import pytest


@pytest.fixture
def lexer():
    """Fixture to create a Lexer instance."""
    return Lexer()


class TestLexer:
    """Test suite for the Lexer class."""

    def test_lexer_init(self, lexer):
        """Test that Lexer can be initialized."""
        assert lexer is not None
        assert isinstance(lexer, Lexer)

    def test_lexer_tokenize_example_from_docstring(self, lexer):
        """Test the example from the lexer docstring."""
        expr = "(Alpha+(Delta+(Pi*(Beta*(Gamma/Sigma)))))"
        expected = ["(", "Alpha", "+", "(", "Delta", "+", "(", "Pi", "*", "(", "Beta", "*", "(", "Gamma", "/", "Sigma", ")", ")", ")", ")", ")"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_simple_addition(self, lexer):
        """Test tokenizing a simple addition expression."""
        expr = "Alpha+Beta"
        expected = ["Alpha", "+", "Beta"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_simple_subtraction(self, lexer):
        """Test tokenizing a simple subtraction expression."""
        expr = "Alpha-Beta"
        expected = ["Alpha", "-", "Beta"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_simple_multiplication(self, lexer):
        """Test tokenizing a simple multiplication expression."""
        expr = "Alpha*Beta"
        expected = ["Alpha", "*", "Beta"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_simple_division(self, lexer):
        """Test tokenizing a simple division expression."""
        expr = "Alpha/Beta"
        expected = ["Alpha", "/", "Beta"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_with_parentheses(self, lexer):
        """Test tokenizing expression with parentheses."""
        expr = "(Alpha+Beta)"
        expected = ["(", "Alpha", "+", "Beta", ")"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_nested_parentheses(self, lexer):
        """Test tokenizing expression with nested parentheses."""
        expr = "((Alpha+Beta))"
        expected = ["(", "(", "Alpha", "+", "Beta", ")", ")"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_complex_expression(self, lexer):
        """Test tokenizing a complex expression with multiple operations."""
        expr = "Alpha+Beta*Gamma/Delta"
        expected = ["Alpha", "+", "Beta", "*", "Gamma", "/", "Delta"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_single_variable(self, lexer):
        """Test tokenizing a single variable."""
        expr = "Alpha"
        # Note: This might expose a bug - trailing variables aren't added
        # If this test fails, we need to fix the lexer
        expected = ["Alpha"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_single_operator(self, lexer):
        """Test tokenizing a single operator."""
        expr = "+"
        expected = ["+"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_empty_string(self, lexer):
        """Test tokenizing an empty string."""
        expr = ""
        expected = []
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_only_operators(self, lexer):
        """Test tokenizing only operators."""
        expr = "++--**//"
        expected = ["+", "+", "-", "-", "*", "*", "/", "/"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_only_parentheses(self, lexer):
        """Test tokenizing only parentheses."""
        expr = "((()))"
        expected = ["(", "(", "(", ")", ")", ")"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_long_variable_name(self, lexer):
        """Test tokenizing long variable names."""
        expr = "VeryLongVariableName+AnotherLongName"
        expected = ["VeryLongVariableName", "+", "AnotherLongName"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_single_letter_variables(self, lexer):
        """Test tokenizing single letter variables."""
        expr = "A+B*C"
        expected = ["A", "+", "B", "*", "C"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_whitespace_in_expression(self, lexer):
        """Test tokenizing expression with whitespace (should be treated as non-letters)."""
        expr = "Alpha + Beta"
        expected = ["Alpha", " ", "+", " ", "Beta"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_numbers(self, lexer):
        """Test tokenizing expression with numbers (should be treated as non-letters)."""
        expr = "Alpha123+Beta456"
        expected = ["Alpha", "1", "2", "3", "+", "Beta", "4", "5", "6"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_mixed_case_variables(self, lexer):
        """Test tokenizing mixed case variable names."""
        expr = "Alpha+BeTa+GaMmA"
        expected = ["Alpha", "+", "BeTa", "+", "GaMmA"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_all_operators(self, lexer):
        """Test tokenizing all basic operators."""
        expr = "A+B-C*D/E"
        expected = ["A", "+", "B", "-", "C", "*", "D", "/", "E"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_consecutive_operators(self, lexer):
        """Test tokenizing consecutive operators."""
        expr = "A++B--C"
        expected = ["A", "+", "+", "B", "-", "-", "C"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_variable_at_end(self, lexer):
        """Test tokenizing expression ending with a variable."""
        expr = "(Alpha+Beta)"
        expected = ["(", "Alpha", "+", "Beta", ")"]
        result = lexer.tokenize(expr)
        assert result == expected
        # This should work since it ends with ')'

    def test_lexer_tokenize_variable_ends_string(self, lexer):
        """Test tokenizing when string ends with a variable (may expose bug)."""
        expr = "Alpha+Beta"
        expected = ["Alpha", "+", "Beta"]
        result = lexer.tokenize(expr)
        assert result == expected
        # This should work since it ends with a letter, but lexer may have bug

    def test_lexer_tokenize_complex_nested_expression(self, lexer):
        """Test tokenizing a deeply nested expression."""
        expr = "((A+(B*(C/D)))+E)"
        expected = ["(", "(", "A", "+", "(", "B", "*", "(", "C", "/", "D", ")", ")", ")", "+", "E", ")"]
        result = lexer.tokenize(expr)
        assert result == expected

    def test_lexer_tokenize_unicode_characters(self, lexer):
        """Test tokenizing with unicode characters (should treat as non-letters)."""
        expr = "Alpha+中文"
        # Unicode characters are not in ascii_letters, so should be separate tokens
        result = lexer.tokenize(expr)
        assert "Alpha" in result
        assert "+" in result
        # The unicode characters should be added as separate tokens

