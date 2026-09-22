"""Algorithms measured by the time complexity visualizer.

Each algorithm is registered with:
  - run:      function that executes the algorithm on prepared input
  - prepare:  function that builds a worst-case input of size n
  - label:    human readable name
  - big_o:    expected worst-case complexity
  - max_n:    largest n we allow (keeps pure-Python O(n^2)/O(n^3) runs sane)
"""
import time

from data_structures import ArrayQueue, Queue, Stack


# ---------------------------------------------------------------- algorithms
def linear_search(data):
    target = -1  # never present -> worst case, scans everything
    for i, value in enumerate(data):
        if value == target:
            return i
    return -1


def binary_search(data):
    target = -1  # smaller than everything -> worst case, log2(n) steps
    low, high = 0, len(data) - 1
    while low <= high:
        mid = (low + high) // 2
        if data[mid] == target:
            return mid
        if data[mid] < target:
            low = mid + 1
        else:
            high = mid - 1
    return -1


def bubble_sort(data):
    arr = list(data)
    n = len(arr)
    for i in range(n):
        for j in range(0, n - i - 1):
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
    return arr


def selection_sort(data):
    arr = list(data)
    n = len(arr)
    for i in range(n):
        smallest = i
        for j in range(i + 1, n):
            if arr[j] < arr[smallest]:
                smallest = j
        arr[i], arr[smallest] = arr[smallest], arr[i]
    return arr


def insertion_sort(data):
    arr = list(data)
    for i in range(1, len(arr)):
        key = arr[i]
        j = i - 1
        while j >= 0 and arr[j] > key:
            arr[j + 1] = arr[j]
            j -= 1
        arr[j + 1] = key
    return arr


def merge_sort(data):
    arr = list(data)
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left, right = merge_sort(arr[:mid]), merge_sort(arr[mid:])
    merged, i, j = [], 0, 0
    while i < len(left) and j < len(right):
        if left[i] <= right[j]:
            merged.append(left[i])
            i += 1
        else:
            merged.append(right[j])
            j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    return merged


def nested_loops(data):
    count = 0
    n = len(data)
    for _ in range(n):
        for _ in range(n):
            count += 1
    return count


def triple_nested_loops(data):
    count = 0
    n = len(data)
    for _ in range(n):
        for _ in range(n):
            for _ in range(n):
                count += 1
    return count


def constant_access(data):
    return data[0] if data else None


# --------------------------------------------------------- stack / queue ops
def stack_push_pop(data):
    """Push every item, then pop every item. Stack ops are O(1) each."""
    s = Stack()
    for x in data:
        s.push(x)
    while not s.is_empty():
        s.pop()


def queue_enqueue_dequeue(data):
    """Enqueue every item, then dequeue every item, using the deque-backed
    Queue. Both operations are O(1) each, so this is O(n) overall."""
    q = Queue()
    for x in data:
        q.enqueue(x)
    while not q.is_empty():
        q.dequeue()


def queue_enqueue_dequeue_array(data):
    """Same as above, but using the list-backed ArrayQueue. dequeue() is
    O(n) here (list.pop(0) shifts everything down), so n dequeues cost
    O(n^2) overall even though enqueue is still O(1)."""
    q = ArrayQueue()
    for x in data:
        q.enqueue(x)
    while not q.is_empty():
        q.dequeue()


def balanced_brackets(data):
    """Classic stack application: check that a bracket string is balanced.
    Each character is pushed or popped at most once, so this is O(n)."""
    s = Stack()
    for ch in data:
        if ch == "(":
            s.push(ch)
        else:
            if s.is_empty():
                return False
            s.pop()
    return s.is_empty()


# ------------------------------------------------------------ input builders
def _ascending(n):
    return list(range(n))


def _descending(n):
    return list(range(n, 0, -1))  # worst case for the simple sorts


def _balanced_bracket_string(n):
    # n '(' followed by n ')': the stack fills all the way to n before
    # it ever empties, which is the worst case for this check.
    return "(" * n + ")" * n


ALGORITHMS = {
    "constant_access": dict(run=constant_access, prepare=_ascending,
                            label="Constant access", big_o="O(1)", max_n=1_000_000),
    "binary_search": dict(run=binary_search, prepare=_ascending,
                          label="Binary search", big_o="O(log n)", max_n=1_000_000),
    "linear_search": dict(run=linear_search, prepare=_ascending,
                          label="Linear search", big_o="O(n)", max_n=1_000_000),
    "merge_sort": dict(run=merge_sort, prepare=_descending,
                       label="Merge sort", big_o="O(n log n)", max_n=100_000),
    "bubble_sort": dict(run=bubble_sort, prepare=_descending,
                        label="Bubble sort", big_o="O(n^2)", max_n=5_000),
    "selection_sort": dict(run=selection_sort, prepare=_descending,
                           label="Selection sort", big_o="O(n^2)", max_n=5_000),
    "insertion_sort": dict(run=insertion_sort, prepare=_descending,
                           label="Insertion sort", big_o="O(n^2)", max_n=5_000),
    "nested_loops": dict(run=nested_loops, prepare=_ascending,
                         label="Nested loops (2 levels)", big_o="O(n^2)", max_n=5_000),
    "triple_nested_loops": dict(run=triple_nested_loops, prepare=_ascending,
                                label="Nested loops (3 levels)", big_o="O(n^3)", max_n=300),
    "stack_push_pop": dict(run=stack_push_pop, prepare=_ascending,
                           label="Stack push/pop", big_o="O(n)", max_n=1_000_000),
    "queue_enqueue_dequeue": dict(run=queue_enqueue_dequeue, prepare=_ascending,
                                  label="Queue enqueue/dequeue (deque)", big_o="O(n)", max_n=1_000_000),
    "queue_enqueue_dequeue_array": dict(run=queue_enqueue_dequeue_array, prepare=_ascending,
                                        label="Queue enqueue/dequeue (array-based)", big_o="O(n^2)", max_n=5_000),
    "balanced_brackets": dict(run=balanced_brackets, prepare=_balanced_bracket_string,
                              label="Balanced brackets (stack)", big_o="O(n)", max_n=1_000_000),
}


# ------------------------------------------------------------------- timing
def measure(algo_name, n, repeats=3):
    """Return the best-of-`repeats` runtime in milliseconds for input size n."""
    spec = ALGORITHMS[algo_name]
    data = spec["prepare"](n)
    best = float("inf")
    for _ in range(repeats):
        start = time.perf_counter()
        spec["run"](data)
        elapsed = time.perf_counter() - start
        best = min(best, elapsed)
    return best * 1000.0


def analyze(algo_name, sizes, time_budget=15.0):
    """Time one algorithm across the input sizes.

    Returns (times_ms, truncated). If the algorithm has used more than
    `time_budget` seconds, we stop early (truncated=True) so a slow
    O(n^2) or O(n^3) run cannot hang the server.
    """
    times = []
    spent = 0.0
    for n in sizes:
        t = measure(algo_name, n)
        times.append(t)
        spent += (t * 3) / 1000.0  # 3 repeats, ms -> seconds
        if spent > time_budget and n != sizes[-1]:
            return times, True
    return times, False
