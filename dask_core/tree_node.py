"""
TreeNode class (left, right, value/operator)
"""
class TreeNode:
    def __init__(self, value=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right

    def is_leaf(self):
        return self.left is None and self.right is None
    
    def is_operator(self):
        return self.value in {"+", "-", "*", "/", "**", "++", "//"}