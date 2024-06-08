"""
history.py

Elise van Iterson, 11907223
05-12-2022

This file contains a History class, to use with Crowthers Adventure game.
The class can be used to keep track of previous moves in the game.
"""

from typing import Any


class History():
    """A stack data structure, also known as
       last in first out (LIFO)"""

    def __init__(self) -> None:
        """post: creates an empty LIFO stack"""
        self.items: list[Any] = []

    def push(self, item: Any) -> None:
        """post: places item on top of the stack"""
        self.items.append(item)

    def pop(self) -> Any:
        """pre: self.size() > 0
           post: removes and returns the top element of the stack"""
        return self.items.pop()

    def top(self) -> Any:
        """pre: self.size() > 0
           post: returns the top element of the stack without
                 removing it"""
        return self.items[-1]

    def size(self) -> int:
        """post: returns the number of elements in the stack"""
        return len(self.items)
