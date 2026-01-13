import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from dask_core.data_structures.stack import Stack
import pytest


class TestStack:
    """Test suite for the Stack data structure."""

    def test_stack_init(self):
        """Test that Stack can be initialized."""
        stack = Stack()
        assert stack is not None
        assert stack.is_empty()
        assert stack.size() == 0

    def test_stack_push(self):
        """Test pushing items onto the stack."""
        stack = Stack()
        stack.push(1)
        assert not stack.is_empty()
        assert stack.size() == 1
        assert stack.peek() == 1

    def test_stack_push_multiple(self):
        """Test pushing multiple items onto the stack."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.size() == 3
        assert stack.peek() == 3

    def test_stack_pop(self):
        """Test popping items from the stack."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.pop() == 2
        assert stack.size() == 1
        assert stack.pop() == 1
        assert stack.is_empty()

    def test_stack_pop_empty(self):
        """Test that popping from empty stack raises IndexError."""
        stack = Stack()
        with pytest.raises(IndexError, match="Cannot pop from an empty stack"):
            stack.pop()

    def test_stack_peek(self):
        """Test peeking at the top of the stack."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        assert stack.peek() == 2
        assert stack.size() == 2  # Peek shouldn't remove items

    def test_stack_peek_empty(self):
        """Test peeking at empty stack returns None."""
        stack = Stack()
        assert stack.peek() is None

    def test_stack_is_empty(self):
        """Test checking if stack is empty."""
        stack = Stack()
        assert stack.is_empty()
        stack.push(1)
        assert not stack.is_empty()
        stack.pop()
        assert stack.is_empty()

    def test_stack_size(self):
        """Test getting the size of the stack."""
        stack = Stack()
        assert stack.size() == 0
        stack.push(1)
        assert stack.size() == 1
        stack.push(2)
        assert stack.size() == 2
        stack.pop()
        assert stack.size() == 1

    def test_stack_clear(self):
        """Test clearing the stack."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.size() == 3
        stack.clear()
        assert stack.is_empty()
        assert stack.size() == 0

    def test_stack_lifo_order(self):
        """Test that stack follows LIFO (Last In, First Out) principle."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        assert stack.pop() == 3
        assert stack.pop() == 2
        assert stack.pop() == 1

    def test_stack_str_representation(self):
        """Test string representation of the stack."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.push(3)
        str_repr = str(stack)
        assert "Stack" in str_repr
        assert "1" in str_repr
        assert "2" in str_repr
        assert "3" in str_repr

    def test_stack_len(self):
        """Test using len() function on the stack."""
        stack = Stack()
        assert len(stack) == 0
        stack.push(1)
        assert len(stack) == 1
        stack.push(2)
        assert len(stack) == 2
        stack.pop()
        assert len(stack) == 1

    def test_stack_bool(self):
        """Test using stack in boolean context."""
        stack = Stack()
        assert not bool(stack)
        assert not stack
        stack.push(1)
        assert bool(stack)
        assert stack

    def test_stack_with_different_types(self):
        """Test stack with different data types."""
        stack = Stack()
        stack.push(1)  # int
        stack.push("hello")  # string
        stack.push([1, 2, 3])  # list
        stack.push({"key": "value"})  # dict
        
        assert isinstance(stack.pop(), dict)
        assert isinstance(stack.pop(), list)
        assert isinstance(stack.pop(), str)
        assert isinstance(stack.pop(), int)

    def test_stack_with_none(self):
        """Test stack with None values."""
        stack = Stack()
        stack.push(None)
        stack.push(1)
        assert stack.pop() == 1
        assert stack.pop() is None

    def test_stack_multiple_operations(self):
        """Test complex sequence of operations."""
        stack = Stack()
        # Push some items
        stack.push(1)
        stack.push(2)
        assert stack.peek() == 2
        assert stack.size() == 2
        
        # Pop one
        assert stack.pop() == 2
        assert stack.size() == 1
        
        # Push more
        stack.push(3)
        stack.push(4)
        assert stack.size() == 3
        
        # Pop all
        assert stack.pop() == 4
        assert stack.pop() == 3
        assert stack.pop() == 1
        assert stack.is_empty()

    def test_stack_clear_and_reuse(self):
        """Test clearing stack and reusing it."""
        stack = Stack()
        stack.push(1)
        stack.push(2)
        stack.clear()
        assert stack.is_empty()
        
        stack.push(3)
        stack.push(4)
        assert stack.size() == 2
        assert stack.pop() == 4

    def test_stack_peek_after_operations(self):
        """Test peek after various operations."""
        stack = Stack()
        stack.push(1)
        assert stack.peek() == 1
        stack.push(2)
        assert stack.peek() == 2
        stack.pop()
        assert stack.peek() == 1
        stack.push(3)
        assert stack.peek() == 3

