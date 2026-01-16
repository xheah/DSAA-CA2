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

    def is_number(self):
        num = isinstance(self.value, (int, float))
        if isinstance(self.value, str):
            try:
                float(self.value)
                num_str = True
            except ValueError:
                num_str = False
        else:
            num_str = False
        return num or num_str
    
    def is_variable(self):
        if isinstance(self.value, str):
            return self.value.isalpha()
        
        return False