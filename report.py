
"""
report.py
=========

Generates publication-style graphs from results/benchmark.csv.

Outputs (results/):
- runtime.png
- nodes.png
- path_length.png
- efficiency.png
- success_rate.png
- benchmark_report.html
"""

import csv
import os
from collections import defaultdict

import matplotlib.pyplot as plt

RESULTS_DIR = "results"
CSV_FILE = os.path.join(RESULTS_DIR, "benchmark.csv")


def load_data():
    with open(CSV_FILE) as f:
        return list(csv.DictReader(f))


def group(records):
    g = defaultdict(list)
    for r in records:
        g[r["algorithm"]].append(r)
    return g


def mean(vals):
    return sum(vals) / len(vals) if vals else 0.0


def bar_chart(labels, values, title, ylabel, filename):
    plt.figure(figsize=(7,5))
    plt.bar(labels, values)
    plt.title(title)
    plt.ylabel(ylabel)
    plt.grid(axis="y", alpha=0.3)
    plt.tight_layout()
    plt.savefig(os.path.join(RESULTS_DIR, filename), dpi=200)
    plt.close()


def create_report():
    os.makedirs(RESULTS_DIR, exist_ok=True)

    data = load_data()
    grouped = group(data)

    algos = list(grouped.keys())

    runtime = []
    nodes = []
    path = []
    efficiency = []
    success = []

    for algo in algos:
        rows = grouped[algo]

        runtime.append(mean([float(r["runtime_ms"]) for r in rows]))
        nodes.append(mean([float(r["nodes_expanded"]) for r in rows]))

        p = [float(r["path_length"]) for r in rows if float(r["path_length"]) > 0]
        path.append(mean(p))

        efficiency.append(mean([float(r["efficiency"]) for r in rows]))

        s = sum(str(r["success"]).lower() == "true" for r in rows)
        success.append(100 * s / len(rows))

    bar_chart(algos, runtime,
              "Average Runtime",
              "Milliseconds",
              "runtime.png")

    bar_chart(algos, nodes,
              "Average Nodes Expanded",
              "Nodes",
              "nodes.png")

    bar_chart(algos, path,
              "Average Path Length",
              "Steps",
              "path_length.png")

    bar_chart(algos, efficiency,
              "Search Efficiency",
              "Efficiency",
              "efficiency.png")

    bar_chart(algos, success,
              "Success Rate",
              "Percentage",
              "success_rate.png")

    html = f"""
<!DOCTYPE html>
<html>
<head>
<title>Maze Solver Benchmark Report</title>
<style>
body {{
font-family: Arial;
margin:40px;
}}
img {{
width:650px;
margin-bottom:30px;
border:1px solid #ddd;
}}
table {{
border-collapse:collapse;
}}
td,th {{
border:1px solid #999;
padding:8px;
}}
</style>
</head>
<body>

<h1>Maze Solver Benchmark Report</h1>

<p>This report summarizes the performance of BFS, DFS, A*, and ACO across randomly generated mazes.</p>

<table>
<tr>
<th>Algorithm</th>
<th>Runtime (ms)</th>
<th>Nodes</th>
<th>Path</th>
<th>Efficiency</th>
<th>Success %</th>
</tr>
"""

    for i, algo in enumerate(algos):
        html += f"""
<tr>
<td>{algo}</td>
<td>{runtime[i]:.3f}</td>
<td>{nodes[i]:.1f}</td>
<td>{path[i]:.1f}</td>
<td>{efficiency[i]:.3f}</td>
<td>{success[i]:.1f}</td>
</tr>
"""

    html += """
</table>

<h2>Average Runtime</h2>
<img src="runtime.png">

<h2>Average Nodes Expanded</h2>
<img src="nodes.png">

<h2>Average Path Length</h2>
<img src="path_length.png">

<h2>Search Efficiency</h2>
<img src="efficiency.png">

<h2>Success Rate</h2>
<img src="success_rate.png">

</body>
</html>
"""

    with open(os.path.join(RESULTS_DIR, "benchmark_report.html"), "w") as f:
        f.write(html)

    print("Generated report in results/")


if __name__ == "__main__":
    create_report()
