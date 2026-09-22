"""Stack and Queue data structures.

Two queue implementations are provided on purpose:
  - Queue:      backed by collections.deque, O(1) enqueue and dequeue
  - ArrayQueue: backed by a plain Python list, O(1) enqueue but O(n)
                dequeue (list.pop(0) has to shift every remaining item)

Comparing the two is the point of this assignment: the "obvious" list
implementation is quietly O(n) per dequeue, so a loop of n enqueues and
n dequeues costs O(n^2) overall, while the deque-based version costs O(n).
"""
from collections import deque


class Stack:
    """LIFO stack backed by a Python list. All operations are O(1)."""

    def __init__(self):
        self._items = []

    def push(self, item):
        self._items.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("pop from empty stack")
        return self._items.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty stack")
        return self._items[-1]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Stack({self._items})"


class Queue:
    """FIFO queue backed by collections.deque. Enqueue and dequeue are O(1)."""

    def __init__(self):
        self._items = deque()

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.popleft()

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"Queue({list(self._items)})"


class ArrayQueue:
    """FIFO queue backed by a plain Python list.

    Enqueue is O(1) (append to the end), but dequeue is O(n) because
    list.pop(0) has to shift every remaining element down by one index.
    Kept here specifically to contrast with the deque-based Queue above.
    """

    def __init__(self):
        self._items = []

    def enqueue(self, item):
        self._items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("dequeue from empty queue")
        return self._items.pop(0)

    def peek(self):
        if self.is_empty():
            raise IndexError("peek from empty queue")
        return self._items[0]

    def is_empty(self):
        return len(self._items) == 0

    def __len__(self):
        return len(self._items)

    def __repr__(self):
        return f"ArrayQueue({self._items})"
