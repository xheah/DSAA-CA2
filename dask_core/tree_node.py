"""
TreeNode class (left, right, value/operator)
"""
class TreeNode:
    def __init__(self, value=None, left=None, right=None):
        self._value: str = value
        self._left: TreeNode = left
        self._right: TreeNode = right

    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, new_value):
        self._value = new_value

    @property
    def left(self):
        return self._left

    @left.setter
    def left(self, new_left):
        self._left = new_left

    @property
    def right(self):
        return self._right

    @right.setter
    def right(self, new_right):
        self._right = new_right

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

    def clone(self):
        left_clone = self.left.clone() if self.left else None
        right_clone = self.right.clone() if self.right else None
        return TreeNode(self.value, left_clone, right_clone)
