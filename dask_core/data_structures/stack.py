"""
Stack data structure with LIFO (Last In, First Out) principle
"""
from typing import Any, Optional


class Stack:
    """
    A stack implementation using a list as the underlying data structure.
    Follows LIFO (Last In, First Out) principle.
    """
    
    def __init__(self):
        """Initialize an empty stack."""
        self._items = []
    
    def push(self, item: Any) -> None:
        """
        Add an item to the top of the stack.
        
        Args:
            item: The item to add to the stack
        """
        self._items.append(item)
    
    def pop(self) -> Any:
        """
        Remove and return the item at the top of the stack.
        
        Returns:
            The item at the top of the stack
            
        Raises:
            IndexError: If the stack is empty
        """
        if self.is_empty():
            raise IndexError("Cannot pop from an empty stack")
        return self._items.pop()
    
    def peek(self) -> Optional[Any]:
        """
        Return the item at the top of the stack without removing it.
        
        Returns:
            The item at the top of the stack, or None if the stack is empty
        """
        if self.is_empty():
            return None
        return self._items[-1]
    
    def is_empty(self) -> bool:
        """
        Check if the stack is empty.
        
        Returns:
            True if the stack is empty, False otherwise
        """
        return len(self._items) == 0
    
    def size(self) -> int:
        """
        Return the number of items in the stack.
        
        Returns:
            The number of items in the stack
        """
        return len(self._items)
    
    def clear(self) -> None:
        """Remove all items from the stack."""
        self._items.clear()
    
    def __str__(self) -> str:
        """
        Return a string representation of the stack.
        
        Returns:
            String representation showing the stack from bottom to top
        """
        return f"Stack({self._items})"
    
    def __repr__(self) -> str:
        """
        Return a string representation of the stack for debugging.
        
        Returns:
            String representation of the stack
        """
        return f"Stack({self._items!r})"
    
    def __len__(self) -> int:
        """
        Return the number of items in the stack.
        Allows using len() function on the stack.
        
        Returns:
            The number of items in the stack
        """
        return len(self._items)
    
    def __bool__(self) -> bool:
        """
        Return True if the stack is not empty, False otherwise.
        Allows using the stack in boolean contexts.
        
        Returns:
            True if the stack is not empty, False otherwise
        """
        return len(self._items) > 0
