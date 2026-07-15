
"""
benchmark_runner.py
===================

Simple CLI entry point for the Maze Solver benchmarking framework.

Workflow
--------
1. Run benchmark.py
2. Compute summary using metrics.py
3. Generate plots/report using report.py
"""

import argparse
import csv
import time

from benchmark import benchmark
from metrics import summarize, print_summary
from dashboard import create_dashboard


def run(args):
    start = time.perf_counter()

    print("=" * 70)
    print("Maze Solver Research Benchmark")
    print("=" * 70)

    benchmark(
        num_mazes=args.mazes,
        rows=args.rows,
        cols=args.cols,
        exits=args.exits,
    )

    with open("results/benchmark.csv") as f:
        rows = list(csv.DictReader(f))

    summary = summarize(rows)

    print("\nStatistical Summary")
    print("-" * 70)
    print_summary(summary)

    print("\nGenerating graphs and HTML report...")
    create_dashboard()

    elapsed = time.perf_counter() - start

    print("\n" + "=" * 70)
    print("Benchmark Complete")
    print("=" * 70)
    print(f"Mazes Tested : {args.mazes}")
    print(f"Maze Size    : {args.rows} x {args.cols}")
    print(f"Algorithms   : BFS, DFS, A*, ACO")
    print(f"Elapsed Time : {elapsed:.2f} s")
    print("CSV          : results/benchmark.csv")
    print("Report       : results/benchmark_report.html")
    print("=" * 70)


def main():
    parser = argparse.ArgumentParser(
        description="Maze Solver Benchmark Runner"
    )

    parser.add_argument(
        "-n",
        "--mazes",
        type=int,
        default=100,
        help="Number of random mazes to benchmark",
    )

    parser.add_argument(
        "--rows",
        type=int,
        default=10,
        help="Maze rows",
    )

    parser.add_argument(
        "--cols",
        type=int,
        default=10,
        help="Maze columns",
    )

    parser.add_argument(
        "--exits",
        type=int,
        default=3,
        help="Number of exits",
    )

    args = parser.parse_args()
    run(args)


if __name__ == "__main__":
    main()
