
"""
metrics.py
==========

Utility functions for analyzing benchmark.csv produced by benchmark.py.
"""

from __future__ import annotations

import math
import statistics
from collections import defaultdict


def confidence_interval(values, confidence=0.95):
    if not values:
        return (0.0, 0.0)
    if len(values) == 1:
        return (values[0], values[0])

    mean = statistics.mean(values)
    std = statistics.stdev(values)
    z = 1.96 if confidence == 0.95 else 1.96
    margin = z * (std / math.sqrt(len(values)))
    return (mean - margin, mean + margin)


def summarize(records):
    """
    records: iterable of dictionaries from benchmark.csv
    """
    grouped = defaultdict(list)

    for r in records:
        grouped[r["algorithm"]].append(r)

    summary = {}

    for algo, rows in grouped.items():
        runtime = [float(r["runtime_ms"]) for r in rows]
        nodes = [float(r["nodes_expanded"]) for r in rows]
        path = [float(r["path_length"]) for r in rows if float(r["path_length"]) > 0]
        eff = [float(r["efficiency"]) for r in rows]

        success = sum(str(r["success"]).lower() == "true" for r in rows)
        optimal = sum(str(r["optimal"]).lower() == "true" for r in rows)

        summary[algo] = {
            "runs": len(rows),
            "success_rate": success / len(rows) * 100,
            "optimal_rate": optimal / len(rows) * 100,
            "runtime_mean": statistics.mean(runtime),
            "runtime_std": statistics.stdev(runtime) if len(runtime) > 1 else 0,
            "runtime_ci95": confidence_interval(runtime),
            "nodes_mean": statistics.mean(nodes),
            "nodes_std": statistics.stdev(nodes) if len(nodes) > 1 else 0,
            "path_mean": statistics.mean(path) if path else 0,
            "path_std": statistics.stdev(path) if len(path) > 1 else 0,
            "efficiency_mean": statistics.mean(eff),
            "efficiency_std": statistics.stdev(eff) if len(eff) > 1 else 0,
            "runtime_min": min(runtime),
            "runtime_max": max(runtime),
            "nodes_min": min(nodes),
            "nodes_max": max(nodes),
        }

    return summary


def print_summary(summary):
    print("=" * 120)
    print(
        f"{'Algorithm':<10}"
        f"{'Runs':>6}"
        f"{'Success%':>12}"
        f"{'Optimal%':>12}"
        f"{'Runtime(ms)':>15}"
        f"{'Nodes':>12}"
        f"{'Path':>10}"
        f"{'Efficiency':>14}"
    )
    print("=" * 120)

    for algo, s in summary.items():
        print(
            f"{algo:<10}"
            f"{s['runs']:>6}"
            f"{s['success_rate']:>11.1f}%"
            f"{s['optimal_rate']:>11.1f}%"
            f"{s['runtime_mean']:>15.2f}"
            f"{s['nodes_mean']:>12.2f}"
            f"{s['path_mean']:>10.2f}"
            f"{s['efficiency_mean']:>14.3f}"
        )

    print("=" * 120)


if __name__ == "__main__":
    import csv

    with open("results/benchmark.csv") as f:
        rows = list(csv.DictReader(f))

    summary = summarize(rows)
    print_summary(summary)

    print("\n95% Confidence Intervals")
    print("-" * 60)
    for algo, s in summary.items():
        low, high = s["runtime_ci95"]
        print(f"{algo:<8}: {low:.3f} ms  -  {high:.3f} ms")
