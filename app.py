"""Flask server for the time_complexity_visualizer.

Run:  python app.py
Then: http://localhost:8000/analyze?algo=linear_search&step=10&n_max=10000
"""
import base64
import os
import re
from datetime import datetime

import matplotlib
matplotlib.use("Agg")  # no display needed, we only save images
import matplotlib.pyplot as plt
from flask import Flask, jsonify, request

from algorithms import ALGORITHMS, analyze

app = Flask(__name__)

PLOTS_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plots")
MAX_POINTS = 1500  # cap on how many input sizes we time per algorithm


class BadRequest(Exception):
    pass


def _clean(value):
    """Strip quotes, brackets, spaces so ?algo=['linear_search'] still works."""
    return re.sub(r"[\[\]'\"\s]", "", value)


def parse_algos():
    raw_values = request.args.getlist("algo")
    if not raw_values:
        raise BadRequest("Missing required query parameter 'algo'.")
    names = []
    for raw in raw_values:
        for part in _clean(raw).split(","):
            if part:
                names.append(part.lower())
    if "all" in names:
        return list(ALGORITHMS)
    unknown = [n for n in names if n not in ALGORITHMS]
    if unknown:
        raise BadRequest(
            f"Unknown algorithm(s): {', '.join(unknown)}. "
            f"Supported: {', '.join(ALGORITHMS)}"
        )
    # keep order, drop duplicates
    return list(dict.fromkeys(names))


def parse_int(name, default=None):
    raw = request.args.get(name)
    if raw is None:
        if default is None:
            raise BadRequest(f"Missing required query parameter '{name}'.")
        return default
    cleaned = _clean(raw).replace(",", "").replace("_", "")
    try:
        value = int(cleaned)
    except ValueError:
        raise BadRequest(f"'{name}' must be an integer, got '{raw}'.")
    if value <= 0:
        raise BadRequest(f"'{name}' must be greater than 0.")
    return value


def build_sizes(step, n_max):
    """Input sizes from 0 up to n_max (inclusive) in increments of step."""
    sizes = list(range(0, n_max + 1, step))
    if sizes[-1] != n_max:
        sizes.append(n_max)
    if len(sizes) > MAX_POINTS:
        raise BadRequest(
            f"Too many data points ({len(sizes)}). Increase 'step' or lower "
            f"'n_max' so that n_max / step is at most {MAX_POINTS}."
        )
    return sizes


def make_plot(sizes, results, algos):
    os.makedirs(PLOTS_DIR, exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 5.5))
    for name in algos:
        spec = ALGORITHMS[name]
        ax.plot(sizes[:len(results[name])], results[name], marker="o", markersize=3,
                label=f"{spec['label']} - {spec['big_o']}")
    ax.set_title("Time complexity analysis")
    ax.set_xlabel("Number of elements (n)")
    ax.set_ylabel("Runtime (ms)")
    ax.grid(True, alpha=0.3)
    ax.legend()
    fig.tight_layout()

    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    path = os.path.join(PLOTS_DIR, f"analysis_{stamp}.png")
    fig.savefig(path, dpi=120)
    plt.close(fig)
    return path


@app.errorhandler(BadRequest)
def handle_bad_request(err):
    return jsonify({"error": str(err)}), 400


@app.route("/")
def index():
    return jsonify({
        "message": "time_complexity_visualizer API",
        "usage": "/analyze?algo=linear_search&step=10&n_max=10000",
        "algorithms": {k: v["big_o"] for k, v in ALGORITHMS.items()},
    })


@app.route("/analyze")
def analyze_endpoint():
    algos = parse_algos()
    step = parse_int("step")
    n_max = parse_int("n_max")

    for name in algos:
        limit = ALGORITHMS[name]["max_n"]
        if n_max > limit:
            raise BadRequest(
                f"n_max={n_max} is too large for '{name}' "
                f"(max {limit}, it is {ALGORITHMS[name]['big_o']})."
            )

    sizes = build_sizes(step, n_max)
    results = {}
    truncated = {}
    for name in algos:
        results[name], truncated[name] = analyze(name, sizes)

    image_path = make_plot(sizes, results, algos)
    with open(image_path, "rb") as f:
        image_b64 = base64.b64encode(f.read()).decode("utf-8")

    return jsonify({
        "algorithms": algos,
        "step": step,
        "n_min": 0,
        "n_max": n_max,
        "sizes": sizes,
        "runtimes_ms": results,
        "truncated": truncated,
        "image_saved_to": os.path.relpath(image_path, os.path.dirname(__file__)),
        "image_base64": image_b64,
    })


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000, debug=True)
