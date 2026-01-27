import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.tree_node import TreeNode
from dask_core.parse_tree import ParseTree
from features.cost_analysis import CostAnalyser


class TestCostAnalyser:
    """Test suite for the CostAnalyser class."""

    def test_cost_analysis_counts(self):
        # Tree: (A + (B * C))
        root = TreeNode("+", TreeNode("A"), TreeNode("*", TreeNode("B"), TreeNode("C")))
        tree = ParseTree(root)
        analyser = CostAnalyser(tree)

        stats = analyser.statistics
        assert stats["original_total_nodes"] == 5
        assert stats["original_operator_nodes"] == 2
        assert stats["original_leaf_nodes"] == 3
        assert stats["original_tree_height"] == 3
        assert stats["original_weighted_op_cost"] == 3  # + (1) + * (2)

        assert stats["optimised_total_nodes"] == 5
        assert stats["optimised_operator_nodes"] == 2
        assert stats["optimised_leaf_nodes"] == 3
        assert stats["optimised_tree_height"] == 3
        assert stats["optimised_weighted_op_cost"] == 3

    def test_cost_analysis_optimised_root_counts(self):
        # Tree: (2 + 3) -> should fold to 5
        root = TreeNode("+", TreeNode("2"), TreeNode("3"))
        tree = ParseTree(root)
        tree.optimise()
        analyser = CostAnalyser(tree)

        stats = analyser.statistics
        assert stats["original_total_nodes"] == 3
        assert stats["original_operator_nodes"] == 1
        assert stats["original_leaf_nodes"] == 2
        assert stats["original_weighted_op_cost"] == 1

        assert stats["optimised_total_nodes"] == 1
        assert stats["optimised_operator_nodes"] == 0
        assert stats["optimised_leaf_nodes"] == 1
        assert stats["optimised_weighted_op_cost"] == 0
