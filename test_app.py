import base64
import os

import pytest

import app as app_module
from algorithms import ALGORITHMS, bubble_sort, binary_search, linear_search, merge_sort


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr(app_module, "PLOTS_DIR", str(tmp_path))
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_required_algorithms_registered():
    for name in ("linear_search", "bubble_sort", "binary_search", "nested_loops"):
        assert name in ALGORITHMS
    assert len(ALGORITHMS) >= 4


def test_sorting_and_search_correctness():
    assert bubble_sort([3, 1, 2]) == [1, 2, 3]
    assert merge_sort([5, 4, 1, 3]) == [1, 3, 4, 5]
    assert linear_search([1, 2, 3]) == -1
    assert binary_search([1, 2, 3]) == -1


def test_analyze_basic(client, tmp_path):
    res = client.get("/analyze?algo=linear_search&step=10&n_max=100")
    assert res.status_code == 200
    body = res.get_json()
    assert body["sizes"][0] == 0 and body["sizes"][-1] == 100
    assert len(body["runtimes_ms"]["linear_search"]) == len(body["sizes"])
    png = base64.b64decode(body["image_base64"])
    assert png.startswith(b"\x89PNG")
    assert len(os.listdir(tmp_path)) == 1  # image saved locally


def test_quoted_algo_and_comma_number(client):
    res = client.get("/analyze?algo=%27linear_search%27&step=1000&n_max=10,000")
    assert res.status_code == 200
    assert res.get_json()["n_max"] == 10000


def test_multiple_algos(client):
    res = client.get("/analyze?algo=linear_search,bubble_sort,binary_search,nested_loops&step=50&n_max=200")
    assert res.status_code == 200
    assert set(res.get_json()["algorithms"]) == {
        "linear_search", "bubble_sort", "binary_search", "nested_loops"}


@pytest.mark.parametrize("query", [
    "step=10&n_max=100",                              # missing algo
    "algo=nope&step=10&n_max=100",                    # unknown algo
    "algo=linear_search&n_max=100",                   # missing step
    "algo=linear_search&step=abc&n_max=100",          # bad step
    "algo=linear_search&step=0&n_max=100",            # zero step
    "algo=bubble_sort&step=10&n_max=100000",          # too big for O(n^2)
    "algo=linear_search&step=1&n_max=100000",         # too many points
])
def test_bad_requests(client, query):
    res = client.get(f"/analyze?{query}")
    assert res.status_code == 400
    assert "error" in res.get_json()


def test_handout_example_url(client):
    res = client.get("/analyze?algo=%27linear_search%27&step=10&n_max=10,000")
    assert res.status_code == 200
    body = res.get_json()
    assert len(body["sizes"]) == 1001
    assert body["truncated"]["linear_search"] is False
