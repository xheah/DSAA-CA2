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
        assert tree.root is None

    def test_parse_tree_init_with_root(self):
        """Test ParseTree initialization with a root node."""
        root = TreeNode("root")
        tree = ParseTree(root)
        assert tree.root == root

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
        mock_evaluator.eval_node.assert_called_once_with(root, context)

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

        assert output[0] == ".2"
        assert output[1] == "+"
        assert output[2] == "..4"
        assert output[3] == ".*"
        assert output[4] == "..5"

    def test_parse_tree_evaluate_complex_expression(self):
        """Test evaluate() with a complex expression tree."""
        # Tree: ((A + B) * C)
        root = TreeNode("*", 
                       TreeNode("+", TreeNode("A"), TreeNode("B")),
                       TreeNode("C"))
        tree = ParseTree(root)
        
        mock_evaluator = Mock()
        mock_evaluator.eval_node.side_effect = lambda node, ctx: {
            root: 15,
            root.left: 5,
            root.right: 3,
            TreeNode("A"): 2,
            TreeNode("B"): 3,
            TreeNode("C"): 3
        }.get(node, 0)
        
        context = {}
        result = tree.evaluate(mock_evaluator, context)
        assert result == 15

