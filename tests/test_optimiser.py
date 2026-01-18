import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.tree_node import TreeNode
from features.optimiser import apply_identity_rules, apply_zero_rules


class TestOptimiser:
    """Test suite for optimiser helpers."""

    def test_apply_identity_rules_add_zero(self):
        node = TreeNode("+", TreeNode("X"), TreeNode("0"))
        result = apply_identity_rules(node, False, True, float)
        assert result.value == "X"

    def test_apply_identity_rules_mul_one(self):
        node = TreeNode("*", TreeNode("1"), TreeNode("Y"))
        result = apply_identity_rules(node, True, False, float)
        assert result.value == "Y"

    def test_apply_identity_rules_div_one(self):
        node = TreeNode("/", TreeNode("Z"), TreeNode("1"))
        result = apply_identity_rules(node, False, True, float)
        assert result.value == "Z"

    def test_apply_identity_rules_pow_one_zero(self):
        node_one = TreeNode("**", TreeNode("A"), TreeNode("1"))
        result_one = apply_identity_rules(node_one, False, True, float)
        assert result_one.value == "A"

        node_zero = TreeNode("**", TreeNode("A"), TreeNode("0"))
        result_zero = apply_identity_rules(node_zero, False, True, float)
        assert result_zero.value == 1

    def test_apply_zero_rules_mul_zero(self):
        node = TreeNode("*", TreeNode("0"), TreeNode("X"))
        result = apply_zero_rules(node, True, False, float)
        assert result.value == 0

    def test_apply_zero_rules_zero_div_nonzero(self):
        node = TreeNode("/", TreeNode("0"), TreeNode("2"))
        result = apply_zero_rules(node, True, True, float)
        assert result.value == 0
