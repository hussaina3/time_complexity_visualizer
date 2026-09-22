import pytest

from data_structures import ArrayQueue, Queue, Stack


# --------------------------------------------------------------------- Stack
def test_stack_starts_empty():
    s = Stack()
    assert s.is_empty()
    assert len(s) == 0


def test_stack_push_increases_length():
    s = Stack()
    s.push(1)
    s.push(2)
    assert len(s) == 2
    assert not s.is_empty()


def test_stack_pop_is_lifo():
    s = Stack()
    for x in (1, 2, 3):
        s.push(x)
    assert s.pop() == 3
    assert s.pop() == 2
    assert s.pop() == 1
    assert s.is_empty()


def test_stack_peek_does_not_remove():
    s = Stack()
    s.push("a")
    s.push("b")
    assert s.peek() == "b"
    assert len(s) == 2


def test_stack_pop_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.pop()


def test_stack_peek_empty_raises():
    s = Stack()
    with pytest.raises(IndexError):
        s.peek()


def test_stack_mixed_operations():
    s = Stack()
    s.push(1)
    s.push(2)
    assert s.pop() == 2
    s.push(3)
    assert s.pop() == 3
    assert s.pop() == 1
    assert s.is_empty()


# --------------------------------------------------------------------- Queue
def test_queue_starts_empty():
    q = Queue()
    assert q.is_empty()
    assert len(q) == 0


def test_queue_enqueue_increases_length():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    assert len(q) == 2


def test_queue_dequeue_is_fifo():
    q = Queue()
    for x in (1, 2, 3):
        q.enqueue(x)
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.is_empty()


def test_queue_peek_does_not_remove():
    q = Queue()
    q.enqueue("a")
    q.enqueue("b")
    assert q.peek() == "a"
    assert len(q) == 2


def test_queue_dequeue_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.dequeue()


def test_queue_peek_empty_raises():
    q = Queue()
    with pytest.raises(IndexError):
        q.peek()


def test_queue_mixed_operations():
    q = Queue()
    q.enqueue(1)
    q.enqueue(2)
    assert q.dequeue() == 1
    q.enqueue(3)
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.is_empty()


# ---------------------------------------------------------------- ArrayQueue
def test_array_queue_starts_empty():
    q = ArrayQueue()
    assert q.is_empty()
    assert len(q) == 0


def test_array_queue_dequeue_is_fifo():
    q = ArrayQueue()
    for x in (1, 2, 3):
        q.enqueue(x)
    assert q.dequeue() == 1
    assert q.dequeue() == 2
    assert q.dequeue() == 3
    assert q.is_empty()


def test_array_queue_dequeue_empty_raises():
    q = ArrayQueue()
    with pytest.raises(IndexError):
        q.dequeue()


def test_queue_and_array_queue_agree():
    """Both implementations must produce the same FIFO order."""
    q1, q2 = Queue(), ArrayQueue()
    for x in range(50):
        q1.enqueue(x)
        q2.enqueue(x)
    out1 = [q1.dequeue() for _ in range(50)]
    out2 = [q2.dequeue() for _ in range(50)]
    assert out1 == out2 == list(range(50))
