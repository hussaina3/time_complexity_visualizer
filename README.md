# time_complexity_visualizer

Flask endpoint that times algorithms across input sizes, plots the result, saves the PNG to `plots/` and returns it as base64 in the JSON.

## Run
    pip install -r requirements.txt
    python app.py

## Endpoint
    GET http://localhost:8000/analyze?algo=linear_search&step=10&n_max=10000

- `algo`: one or more names, comma separated (or `all`)
- `step`: increment between input sizes (starts at 0)
- `n_max`: largest input size (commas like 10,000 are accepted)

Supported: linear_search, binary_search, bubble_sort, nested_loops, constant_access, selection_sort, insertion_sort, merge_sort, triple_nested_loops

## Tests
    python -m pytest -q
