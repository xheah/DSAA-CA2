"""
TreeNode class (left, right, value/operator)
"""
class TreeNode:
    def __init__(self, value=None, left=None, right=None):
        self.value: str = value
        self.left: TreeNode = left
        self.right: TreeNode = right

    def is_leaf(self):
        return self.left is None and self.right is None
    
    def is_operator(self):
        return self.value in {"+", "-", "*", "/", "**", "++", "//"}