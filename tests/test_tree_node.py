import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.tree_node import TreeNode
import pytest


class TestTreeNode:
    """Test suite for the TreeNode class."""

    def test_tree_node_init_default(self):
        """Test TreeNode initialization with default values."""
        node = TreeNode()
        assert node.value is None
        assert node.left is None
        assert node.right is None

    def test_tree_node_init_with_value(self):
        """Test TreeNode initialization with a value."""
        node = TreeNode(value="A")
        assert node.value == "A"
        assert node.left is None
        assert node.right is None

    def test_tree_node_init_with_all_params(self):
        """Test TreeNode initialization with all parameters."""
        left = TreeNode("left")
        right = TreeNode("right")
        node = TreeNode("root", left, right)
        assert node.value == "root"
        assert node.left == left
        assert node.right == right

    def test_tree_node_is_leaf_single_node(self):
        """Test is_leaf() for a single node."""
        node = TreeNode("A")
        assert node.is_leaf() is True

    def test_tree_node_is_leaf_with_left_child(self):
        """Test is_leaf() for a node with left child."""
        left = TreeNode("left")
        node = TreeNode("root", left=left)
        assert node.is_leaf() is False

    def test_tree_node_is_leaf_with_right_child(self):
        """Test is_leaf() for a node with right child."""
        right = TreeNode("right")
        node = TreeNode("root", right=right)
        assert node.is_leaf() is False

    def test_tree_node_is_leaf_with_both_children(self):
        """Test is_leaf() for a node with both children."""
        left = TreeNode("left")
        right = TreeNode("right")
        node = TreeNode("root", left, right)
        assert node.is_leaf() is False

    def test_tree_node_is_operator_plus(self):
        """Test is_operator() for + operator."""
        node = TreeNode("+")
        assert node.is_operator() is True

    def test_tree_node_is_operator_minus(self):
        """Test is_operator() for - operator."""
        node = TreeNode("-")
        assert node.is_operator() is True

    def test_tree_node_is_operator_multiply(self):
        """Test is_operator() for * operator."""
        node = TreeNode("*")
        assert node.is_operator() is True

    def test_tree_node_is_operator_divide(self):
        """Test is_operator() for / operator."""
        node = TreeNode("/")
        assert node.is_operator() is True

    def test_tree_node_is_operator_double_plus(self):
        """Test is_operator() for ++ operator."""
        node = TreeNode("++")
        assert node.is_operator() is True

    def test_tree_node_is_operator_double_star(self):
        """Test is_operator() for ** operator."""
        node = TreeNode("**")
        assert node.is_operator() is True

    def test_tree_node_is_operator_double_slash(self):
        """Test is_operator() for // operator."""
        node = TreeNode("//")
        assert node.is_operator() is True

    def test_tree_node_is_operator_variable(self):
        """Test is_operator() for a variable (not an operator)."""
        node = TreeNode("Alpha")
        assert node.is_operator() is False

    def test_tree_node_is_operator_number(self):
        """Test is_operator() for a number (not an operator)."""
        node = TreeNode(100)
        assert node.is_operator() is False

    def test_tree_node_is_operator_none(self):
        """Test is_operator() for None value."""
        node = TreeNode(None)
        assert node.is_operator() is False

    def test_tree_node_binary_tree_structure(self):
        """Test creating a binary tree structure."""
        left_left = TreeNode("A")
        left_right = TreeNode("B")
        right_left = TreeNode("C")
        right_right = TreeNode("D")
        
        left = TreeNode("+", left_left, left_right)
        right = TreeNode("*", right_left, right_right)
        root = TreeNode("root", left, right)
        
        assert root.value == "root"
        assert root.left.value == "+"
        assert root.left.left.value == "A"
        assert root.left.right.value == "B"
        assert root.right.value == "*"
        assert root.right.left.value == "C"
        assert root.right.right.value == "D"

    def test_tree_node_modify_value(self):
        """Test modifying a node's value."""
        node = TreeNode("A")
        node.value = "B"
        assert node.value == "B"

    def test_tree_node_modify_children(self):
        """Test modifying a node's children."""
        node = TreeNode("root")
        left = TreeNode("left")
        right = TreeNode("right")
        
        node.left = left
        node.right = right
        
        assert node.left == left
        assert node.right == right
        assert node.is_leaf() is False

