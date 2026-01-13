import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.lexer import tokenize
import pytest


class TestLexer:
    """Test suite for the tokenize function."""

    def test_tokenize_example_from_docstring(self):
        """Test the example from the lexer docstring."""
        expr = "(Alpha+(Delta+(Pi*(Beta*(Gamma/Sigma)))))"
        expected = ["(", "Alpha", "+", "(", "Delta", "+", "(", "Pi", "*", "(", "Beta", "*", "(", "Gamma", "/", "Sigma", ")", ")", ")", ")", ")"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_simple_addition(self):
        """Test tokenizing a simple addition expression."""
        expr = "Alpha+Beta"
        expected = ["Alpha", "+", "Beta"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_simple_subtraction(self):
        """Test tokenizing a simple subtraction expression."""
        expr = "Alpha-Beta"
        expected = ["Alpha", "-", "Beta"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_simple_multiplication(self):
        """Test tokenizing a simple multiplication expression."""
        expr = "Alpha*Beta"
        expected = ["Alpha", "*", "Beta"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_simple_division(self):
        """Test tokenizing a simple division expression."""
        expr = "Alpha/Beta"
        expected = ["Alpha", "/", "Beta"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_with_parentheses(self):
        """Test tokenizing expression with parentheses."""
        expr = "(Alpha+Beta)"
        expected = ["(", "Alpha", "+", "Beta", ")"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_nested_parentheses(self):
        """Test tokenizing expression with nested parentheses."""
        expr = "((Alpha+Beta))"
        expected = ["(", "(", "Alpha", "+", "Beta", ")", ")"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_complex_expression(self):
        """Test tokenizing a complex expression with multiple operations."""
        expr = "Alpha+Beta*Gamma/Delta"
        expected = ["Alpha", "+", "Beta", "*", "Gamma", "/", "Delta"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_single_variable(self):
        """Test tokenizing a single variable."""
        expr = "Alpha"
        expected = ["Alpha"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_single_operator(self):
        """Test tokenizing a single operator."""
        expr = "+"
        expected = ["+"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_empty_string(self):
        """Test tokenizing an empty string."""
        expr = ""
        expected = []
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_only_operators(self):
        """Test tokenizing only operators."""
        expr = "++--**//"
        # Now ++, **, // should be recognized as multi-character operators
        expected = ["++", "-", "-", "**", "//"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_only_parentheses(self):
        """Test tokenizing only parentheses."""
        expr = "((()))"
        expected = ["(", "(", "(", ")", ")", ")"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_long_variable_name(self):
        """Test tokenizing long variable names."""
        expr = "VeryLongVariableName+AnotherLongName"
        expected = ["VeryLongVariableName", "+", "AnotherLongName"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_single_letter_variables(self):
        """Test tokenizing single letter variables."""
        expr = "A+B*C"
        expected = ["A", "+", "B", "*", "C"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_whitespace_in_expression(self):
        """Test tokenizing expression with whitespace (should be treated as non-letters)."""
        expr = "Alpha + Beta"
        expected = ["Alpha", " ", "+", " ", "Beta"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_numbers(self):
        """Test tokenizing expression with numbers (should be treated as non-letters)."""
        expr = "Alpha123+Beta456"
        expected = ["Alpha", "1", "2", "3", "+", "Beta", "4", "5", "6"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_mixed_case_variables(self):
        """Test tokenizing mixed case variable names."""
        expr = "Alpha+BeTa+GaMmA"
        expected = ["Alpha", "+", "BeTa", "+", "GaMmA"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_all_operators(self):
        """Test tokenizing all basic operators."""
        expr = "A+B-C*D/E"
        expected = ["A", "+", "B", "-", "C", "*", "D", "/", "E"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_consecutive_operators(self):
        """Test tokenizing consecutive operators - ++ should be recognized as single operator."""
        expr = "A++B--C"
        # ++ should be recognized as a multi-character operator
        expected = ["A", "++", "B", "-", "-", "C"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_variable_at_end(self):
        """Test tokenizing expression ending with a variable."""
        expr = "(Alpha+Beta)"
        expected = ["(", "Alpha", "+", "Beta", ")"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_variable_ends_string(self):
        """Test tokenizing when string ends with a variable."""
        expr = "Alpha+Beta"
        expected = ["Alpha", "+", "Beta"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_complex_nested_expression(self):
        """Test tokenizing a deeply nested expression."""
        expr = "((A+(B*(C/D)))+E)"
        expected = ["(", "(", "A", "+", "(", "B", "*", "(", "C", "/", "D", ")", ")", ")", "+", "E", ")"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_unicode_characters(self):
        """Test tokenizing with unicode characters (should treat as non-letters)."""
        expr = "Alpha+中文"
        # Unicode characters are not in ascii_letters, so should be separate tokens
        result = tokenize(expr)
        assert "Alpha" in result
        assert "+" in result
        # The unicode characters should be added as separate tokens

    # New tests for multi-character operators
    def test_tokenize_double_plus_operator(self):
        """Test tokenizing the ++ operator."""
        expr = "Alpha++Beta"
        expected = ["Alpha", "++", "Beta"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_double_star_operator(self):
        """Test tokenizing the ** operator."""
        expr = "Alpha**Beta"
        expected = ["Alpha", "**", "Beta"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_double_slash_operator(self):
        """Test tokenizing the // operator."""
        expr = "Alpha//Beta"
        expected = ["Alpha", "//", "Beta"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_all_multi_char_operators(self):
        """Test tokenizing all multi-character operators in one expression."""
        expr = "A++B**C//D"
        expected = ["A", "++", "B", "**", "C", "//", "D"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_multi_char_operators_with_parentheses(self):
        """Test tokenizing multi-character operators with parentheses."""
        expr = "(Alpha++Beta)**(Gamma//Delta)"
        expected = ["(", "Alpha", "++", "Beta", ")", "**", "(", "Gamma", "//", "Delta", ")"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_mixed_single_and_multi_char_operators(self):
        """Test tokenizing mixed single and multi-character operators."""
        expr = "A+B++C*D**E/F//G"
        expected = ["A", "+", "B", "++", "C", "*", "D", "**", "E", "/", "F", "//", "G"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_single_plus_vs_double_plus(self):
        """Test that single + and double ++ are distinguished correctly."""
        expr = "A+B++C"
        expected = ["A", "+", "B", "++", "C"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_single_star_vs_double_star(self):
        """Test that single * and double ** are distinguished correctly."""
        expr = "A*B**C"
        expected = ["A", "*", "B", "**", "C"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_single_slash_vs_double_slash(self):
        """Test that single / and double // are distinguished correctly."""
        expr = "A/B//C"
        expected = ["A", "/", "B", "//", "C"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_multi_char_operator_at_start(self):
        """Test tokenizing expression starting with multi-character operator."""
        expr = "++Alpha"
        expected = ["++", "Alpha"]
        result = tokenize(expr)
        assert result == expected

    def test_tokenize_multi_char_operator_at_end(self):
        """Test tokenizing expression ending with multi-character operator."""
        expr = "Alpha++"
        expected = ["Alpha", "++"]
        result = tokenize(expr)
        assert result == expected
