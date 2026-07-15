
"""
benchmark.py
============
Benchmark runner for the Maze Solver project.

Runs BFS, DFS, A*, and ACO on randomly generated mazes and stores
performance metrics in results/benchmark.csv.

Compatible with:
- maze.py
- algorithms.py
"""

from __future__ import annotations

import csv
import os
import statistics
import time

from maze import generate_random_maze
from algorithms import bfs, dfs, astar, aco

RESULTS_DIR = "results"
CSV_FILE = os.path.join(RESULTS_DIR, "benchmark.csv")


ALGORITHMS = {
    "BFS": bfs,
    "DFS": dfs,
    "A*": astar,
    "ACO": aco,
}


def run_single(maze, name, func, optimal_length=None):
    start = time.perf_counter()
    result = func(maze)
    elapsed_ms = (time.perf_counter() - start) * 1000

    path_length = len(result.path) - 1 if result.success else 0

    if optimal_length is None:
        optimal = result.success
    else:
        optimal = result.success and path_length == optimal_length

    efficiency = (
        path_length / result.nodes_expanded
        if result.success and result.nodes_expanded > 0
        else 0.0
    )

    return {
        "algorithm": name,
        "success": result.success,
        "runtime_ms": elapsed_ms,
        "nodes_expanded": result.nodes_expanded,
        "path_length": path_length,
        "optimal": optimal,
        "efficiency": efficiency,
    }


def benchmark(num_mazes=100, rows=10, cols=10, exits=3):
    os.makedirs(RESULTS_DIR, exist_ok=True)

    rows_out = []

    print("=" * 70)
    print(f"Running benchmark on {num_mazes} random mazes")
    print("=" * 70)

    for maze_id in range(1, num_mazes + 1):
        maze = generate_random_maze(rows=rows, cols=cols, num_exits=exits)

        bfs_result = run_single(maze, "BFS", bfs)
        optimal_length = bfs_result["path_length"] if bfs_result["success"] else None

        bfs_result["maze_id"] = maze_id
        rows_out.append(bfs_result)

        for name, func in ALGORITHMS.items():
            if name == "BFS":
                continue

            r = run_single(maze, name, func, optimal_length)
            r["maze_id"] = maze_id
            rows_out.append(r)

        if maze_id % 10 == 0:
            print(f"Completed {maze_id}/{num_mazes}")

    with open(CSV_FILE, "w", newline="") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=[
                "maze_id",
                "algorithm",
                "success",
                "runtime_ms",
                "nodes_expanded",
                "path_length",
                "optimal",
                "efficiency",
            ],
        )
        writer.writeheader()
        writer.writerows(rows_out)

    print("\nSaved:", CSV_FILE)
    print_summary(rows_out)


def print_summary(data):
    print("\n" + "=" * 85)
    print(
        f"{'Algorithm':<10}"
        f"{'Success %':>12}"
        f"{'Runtime(ms)':>15}"
        f"{'Nodes':>12}"
        f"{'Path':>10}"
        f"{'Optimal %':>12}"
        f"{'Efficiency':>14}"
    )
    print("=" * 85)

    for algo in ALGORITHMS:
        subset = [x for x in data if x["algorithm"] == algo]

        success_rate = (
            sum(x["success"] for x in subset) / len(subset) * 100
        )

        runtime = statistics.mean(x["runtime_ms"] for x in subset)
        nodes = statistics.mean(x["nodes_expanded"] for x in subset)

        paths = [x["path_length"] for x in subset if x["success"]]
        avg_path = statistics.mean(paths) if paths else 0

        optimal = (
            sum(x["optimal"] for x in subset) / len(subset) * 100
        )

        eff = statistics.mean(x["efficiency"] for x in subset)

        print(
            f"{algo:<10}"
            f"{success_rate:>11.1f}%"
            f"{runtime:>15.2f}"
            f"{nodes:>12.1f}"
            f"{avg_path:>10.1f}"
            f"{optimal:>11.1f}%"
            f"{eff:>14.3f}"
        )

    print("=" * 85)


if __name__ == "__main__":
    benchmark(num_mazes=100)
