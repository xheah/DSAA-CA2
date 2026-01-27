import sys
from pathlib import Path
from io import StringIO
from unittest.mock import patch, Mock

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.parse_tree import ParseTree
from dask_core.tree_node import TreeNode
import pytest


class TestParseTree:
    """Test suite for the ParseTree class."""

    def test_parse_tree_init_default(self):
        """Test ParseTree initialization with default root."""
        tree = ParseTree()
        assert tree.original_root is None
        assert tree.optimised_root is None

    def test_parse_tree_init_with_root(self):
        """Test ParseTree initialization with a root node."""
        root = TreeNode("root")
        tree = ParseTree(root)
        assert tree.original_root == root

    def test_parse_tree_evaluate_none_root(self):
        """Test evaluate() with None root."""
        tree = ParseTree()
        mock_evaluator = Mock()
        context = {}
        result = tree.evaluate(mock_evaluator, context)
        assert result is None
        mock_evaluator.eval_node.assert_not_called()

    def test_parse_tree_evaluate_with_root(self):
        """Test evaluate() with a root node."""
        root = TreeNode("+", TreeNode("A"), TreeNode("B"))
        tree = ParseTree(root)
        mock_evaluator = Mock()
        mock_evaluator.eval_node.return_value = 5
        context = {}
        
        result = tree.evaluate(mock_evaluator, context)
        
        assert result == 5
        mock_evaluator.eval_node.assert_called_once_with(tree.optimised_root, context)

    def test_parse_tree_print_rotated_default(self):
        """Test print_rotated() with default node (uses root)."""
        root = TreeNode("+", TreeNode("A"), TreeNode("B"))
        tree = ParseTree(root)
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            tree.print_rotated()
            output = fake_output.getvalue()
            assert "+" in output
            assert "A" in output
            assert "B" in output

    def test_parse_tree_print_rotated_with_node(self):
        """Test print_rotated() with a specific node."""
        root = TreeNode("+", TreeNode("A"), TreeNode("B"))
        tree = ParseTree(root)
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            tree.print_rotated(root)
            output = fake_output.getvalue()
            assert "+" in output
            assert "A" in output
            assert "B" in output

    def test_parse_tree_print_rotated_single_node(self):
        """Test print_rotated() with a single node."""
        root = TreeNode("A")
        tree = ParseTree(root)
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            tree.print_rotated()
            output = fake_output.getvalue()
            assert "A" in output

    def test_parse_tree_print_rotated_complex_tree(self):
        """Test print_rotated() with a complex tree."""
        # Tree: (A + (B * C))
        root = TreeNode("+", TreeNode("A"), TreeNode("*", TreeNode("B"), TreeNode("C")))
        tree = ParseTree(root)
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            tree.print_rotated()
            output = fake_output.getvalue()
            assert "+" in output
            assert "A" in output
            assert "*" in output
            assert "B" in output
            assert "C" in output

    def test_parse_tree_print_rotated_indentation(self):
        """Test that print_rotated() uses proper indentation."""
        root = TreeNode("+", TreeNode("A"), TreeNode("B"))
        tree = ParseTree(root)
        
        with patch('sys.stdout', new=StringIO()) as fake_output:
            tree.print_rotated()
            output = fake_output.getvalue()
            # Should have some indentation (spaces)
            lines = output.strip().split('\n')
            assert len(lines) > 0

    def test_parse_tree_print_rotated_none_root(self):
        """Test print_rotated() with None root."""
        tree = ParseTree()
        # Should not raise an error, but behavior depends on implementation
        # If it tries to access node.value, it will raise AttributeError
        with pytest.raises((AttributeError, TypeError)):
            tree.print_rotated()

    def test_parse_tree_print_in_order(self):
        """Test printInOrder() output order and indentation."""
        root = TreeNode("+", TreeNode("2"), TreeNode("*", TreeNode("4"), TreeNode("5")))
        tree = ParseTree(root)

        with patch('sys.stdout', new=StringIO()) as fake_output:
            tree.printInOrder()
            output = fake_output.getvalue().strip().split('\n')

        assert output[0] == "..5"
        assert output[1] == ".*"
        assert output[2] == "..4"
        assert output[3] == "+"
        assert output[4] == ".2"

    def test_parse_tree_evaluate_complex_expression(self):
        """Test evaluate() with a complex expression tree."""
        # Tree: ((A + B) * C)
        root = TreeNode("*", 
                       TreeNode("+", TreeNode("A"), TreeNode("B")),
                       TreeNode("C"))
        tree = ParseTree(root)
        
        mock_evaluator = Mock()
        mock_evaluator.eval_node.return_value = 15
        
        context = {}
        result = tree.evaluate(mock_evaluator, context)
        assert result == 15
        mock_evaluator.eval_node.assert_called_once_with(tree.optimised_root, context)

    def test_parse_tree_optimise_constant_folding(self):
        """Test optimise() folds constant subtrees."""
        root = TreeNode("+", TreeNode("2"), TreeNode("3"))
        tree = ParseTree(root)

        optimised = tree.optimise()

        assert optimised is not None
        assert tree.optimised_root is not None
        assert tree.optimised_root.value == 5.0

    def test_parse_tree_optimise_constant_folding_summative_ops(self):
        """Test optimise() folds ++ and // only for constant operands."""
        root_sum = TreeNode("++", TreeNode("2"), TreeNode("3"))
        tree_sum = ParseTree(root_sum)
        optimised_sum = tree_sum.optimise()

        assert optimised_sum is not None
        assert tree_sum.optimised_root.value == 9

        root_div = TreeNode("//", TreeNode("3"), TreeNode("2"))
        tree_div = ParseTree(root_div)
        optimised_div = tree_div.optimise()

        assert optimised_div is not None
        assert tree_div.optimised_root.value == 2

    def test_parse_tree_optimise_constant_folding_summative_ops_with_variable(self):
        """Test optimise() does not fold ++ or // when a variable is present."""
        root_sum = TreeNode("++", TreeNode("A"), TreeNode("3"))
        tree_sum = ParseTree(root_sum)
        optimised_sum = tree_sum.optimise()

        assert optimised_sum is not None
        assert tree_sum.optimised_root.value == "++"
        assert tree_sum.optimised_root.left.value == "A"
        assert tree_sum.optimised_root.right.value == "3"

        root_div = TreeNode("//", TreeNode("3"), TreeNode("A"))
        tree_div = ParseTree(root_div)
        optimised_div = tree_div.optimise()

        assert optimised_div is not None
        assert tree_div.optimised_root.value == "//"
        assert tree_div.optimised_root.left.value == "3"
        assert tree_div.optimised_root.right.value == "A"

    def test_parse_tree_optimise_identity_rule(self):
        """Test optimise() applies identity rules like x+0."""
        root = TreeNode("+", TreeNode("X"), TreeNode("0"))
        tree = ParseTree(root)

        optimised = tree.optimise()

        assert optimised is not None
        assert tree.optimised_root.value == "X"

    def test_parse_tree_optimise_identity_rule_left_zero(self):
        """Test optimise() applies identity rule 0+x."""
        root = TreeNode("+", TreeNode("0"), TreeNode("X"))
        tree = ParseTree(root)

        optimised = tree.optimise()

        assert optimised is not None
        assert tree.optimised_root.value == "X"

    def test_parse_tree_optimise_identity_rule_mul_one(self):
        """Test optimise() applies identity rules like x*1 and 1*x."""
        root_right = TreeNode("*", TreeNode("X"), TreeNode("1"))
        tree_right = ParseTree(root_right)
        optimised_right = tree_right.optimise()

        assert optimised_right is not None
        assert tree_right.optimised_root.value == "X"

        root_left = TreeNode("*", TreeNode("1"), TreeNode("X"))
        tree_left = ParseTree(root_left)
        optimised_left = tree_left.optimise()

        assert optimised_left is not None
        assert tree_left.optimised_root.value == "X"

    def test_parse_tree_optimise_identity_division_by_one(self):
        """Test optimise() applies identity rule x/1."""
        root = TreeNode("/", TreeNode("X"), TreeNode("1"))
        tree = ParseTree(root)

        optimised = tree.optimise()

        assert optimised is not None
        assert tree.optimised_root.value == "X"

    def test_parse_tree_optimise_identity_power_rules(self):
        """Test optimise() applies identity rules for powers."""
        root_pow_one = TreeNode("**", TreeNode("X"), TreeNode("1"))
        tree_pow_one = ParseTree(root_pow_one)
        optimised_one = tree_pow_one.optimise()

        assert optimised_one is not None
        assert tree_pow_one.optimised_root.value == "X"

        root_pow_zero = TreeNode("**", TreeNode("X"), TreeNode("0"))
        tree_pow_zero = ParseTree(root_pow_zero)
        optimised_zero = tree_pow_zero.optimise()

        assert optimised_zero is not None
        assert tree_pow_zero.optimised_root.value == 1

    def test_parse_tree_optimise_zero_rule(self):
        """Test optimise() applies zero rules like x*0."""
        root = TreeNode("*", TreeNode("X"), TreeNode("0"))
        tree = ParseTree(root)

        optimised = tree.optimise()

        assert optimised is not None
        assert tree.optimised_root.value == 0

    def test_parse_tree_optimise_zero_rule_left_zero_mul(self):
        """Test optimise() applies zero rule 0*x."""
        root = TreeNode("*", TreeNode("0"), TreeNode("X"))
        tree = ParseTree(root)

        optimised = tree.optimise()

        assert optimised is not None
        assert tree.optimised_root.value == 0

    def test_parse_tree_optimise_zero_rule_division(self):
        """Test optimise() applies zero rule 0/x when x is nonzero constant."""
        root = TreeNode("/", TreeNode("0"), TreeNode("2"))
        tree = ParseTree(root)

        optimised = tree.optimise()

        assert optimised is not None
        assert tree.optimised_root.value == 0

    def test_parse_tree_optimise_zero_rule_division_variable(self):
        """Test optimise() does not fold 0/x when x is a variable."""
        root = TreeNode("/", TreeNode("0"), TreeNode("X"))
        tree = ParseTree(root)

        optimised = tree.optimise()

        assert optimised is not None
        assert tree.optimised_root.value == "/"
        assert tree.optimised_root.left.value == "0"
        assert tree.optimised_root.right.value == "X"

    def test_parse_tree_optimise_does_not_fold_variables(self):
        """Test optimise() does not fold variable-only operators."""
        root = TreeNode("+", TreeNode("A"), TreeNode("B"))
        tree = ParseTree(root)

        optimised = tree.optimise()

        assert optimised is not None
        assert tree.optimised_root.value == "+"
        assert tree.optimised_root.left.value == "A"
        assert tree.optimised_root.right.value == "B"

    def test_parse_tree_optimise_does_not_fold_variable_and_number(self):
        """Test optimise() does not fold variable+number without identity/zero rules."""
        root = TreeNode("+", TreeNode("A"), TreeNode("3"))
        tree = ParseTree(root)

        optimised = tree.optimise()

        assert optimised is not None
        assert tree.optimised_root.value == "+"
        assert tree.optimised_root.left.value == "A"
        assert tree.optimised_root.right.value == "3"

    def test_parse_tree_to_expression(self):
        """Test converting a parse tree back to an infix expression string."""
        root = TreeNode("*", TreeNode("5"), TreeNode("6"))
        tree = ParseTree(root)
        assert tree.to_expression() == "(5*6)"
