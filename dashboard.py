
"""
dashboard.py
Quick premium dashboard generator for Maze Solver.

Requirements:
pip install pandas plotly
"""

import os
import pandas as pd
import plotly.express as px
import shutil
from pathlib import Path

RESULTS="results"
CSV=os.path.join(RESULTS,"benchmark.csv")

def create_dashboard():
    df=pd.read_csv(CSV)

    summary=df.groupby("algorithm").agg(
        Runtime=("runtime_ms","mean"),
        Nodes=("nodes_expanded","mean"),
        Path=("path_length","mean"),
        Efficiency=("efficiency","mean"),
        Success=("success",lambda s:(s.astype(str).str.lower()=="true").mean()*100)
    ).reset_index()

    fastest=summary.loc[summary.Runtime.idxmin()]
    shortest=summary.loc[summary.Path.idxmin()]
    nodes=summary.loc[summary.Nodes.idxmin()]
    success=summary.loc[summary.Success.idxmax()]

    charts=[]
    for col,title in [
        ("Runtime","Average Runtime (ms)"),
        ("Nodes","Average Nodes Expanded"),
        ("Path","Average Path Length"),
        ("Efficiency","Search Efficiency"),
        ("Success","Success Rate (%)")
    ]:
        fig=px.bar(summary,x="algorithm",y=col,text_auto=".2f",
                   template="plotly_dark",title=title,
                   color="algorithm")
        charts.append(fig.to_html(full_html=False,include_plotlyjs='cdn'))

    table=summary.round(3).to_html(index=False,
        classes="table",border=0)

    html=f"""
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<title>Maze Solver Benchmark Dashboard</title>
<style>
body{{background:#0f172a;color:#fff;font-family:Arial;margin:35px}}
h1{{font-size:38px}}
.cards{{display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
.card{{background:#1e293b;padding:18px;border-radius:12px;
box-shadow:0 6px 20px rgba(0,0,0,.4)}}
.card h2{{margin:5px 0;color:#60a5fa}}
.section{{margin-top:40px}}
.table{{width:100%;border-collapse:collapse}}
.table th{{background:#2563eb;padding:10px}}
.table td{{background:#1e293b;padding:10px;text-align:center}}
button{{background:#2563eb;color:white;border:none;
padding:12px 18px;border-radius:8px;cursor:pointer;margin-right:10px}}
</style>
</head>
<body>

<h1>🚀 Maze Solver Benchmark Dashboard</h1>

<div class="cards">
<div class="card"><h3>⚡ Fastest</h3><h2>{fastest.algorithm}</h2>{fastest.Runtime:.2f} ms</div>
<div class="card"><h3>🎯 Shortest Path</h3><h2>{shortest.algorithm}</h2>{shortest.Path:.1f} steps</div>
<div class="card"><h3>🧭 Fewest Nodes</h3><h2>{nodes.algorithm}</h2>{nodes.Nodes:.1f}</div>
<div class="card"><h3>✅ Success</h3><h2>{success.algorithm}</h2>{success.Success:.1f}%</div>
</div>

<div class="section">
<h2>Benchmark Configuration</h2>
<ul>
<li>Algorithms: BFS, DFS, A*, ACO</li>
<li>Random Mazes: {len(df)//4}</li>
<li>Maze Size: 10 × 10</li>
</ul>
</div>

<div class="section">
<h2>Key Findings</h2>
<ul>
<li>{fastest.algorithm} is the fastest algorithm.</li>
<li>{shortest.algorithm} finds the shortest average path.</li>
<li>{nodes.algorithm} explores the fewest nodes.</li>
<li>{success.algorithm} achieved the highest success rate.</li>
</ul>
</div>

<button onclick="window.print()">🖨 Print Report</button>
<button onclick="location.href='benchmark.csv'">⬇ Download CSV</button>

<div class="section">
<h2>Performance Summary</h2>
{table}
</div>

{''.join(charts)}

</body>
</html>
"""
# -----------------------------
# Create output directories
# -----------------------------
RESULTS_DIR = Path("results")
DOCS_DIR = Path("docs")

RESULTS_DIR.mkdir(exist_ok=True)
DOCS_DIR.mkdir(exist_ok=True)

# -----------------------------
# Save dashboard to results
# -----------------------------
dashboard_path = RESULTS_DIR / "benchmark_dashboard.html"

with open(dashboard_path, "w", encoding="utf-8") as f:
    f.write(html)

print(f"✓ Dashboard saved to {dashboard_path}")

# -----------------------------
# Automatically deploy to GitHub Pages
# -----------------------------
github_dashboard = DOCS_DIR / "index.html"

shutil.copy2(dashboard_path, github_dashboard)

print(f"✓ GitHub Pages dashboard updated -> {github_dashboard}")

# -----------------------------
# Copy benchmark CSV
# -----------------------------
csv_source = RESULTS_DIR / "benchmark.csv"

if csv_source.exists():
    shutil.copy2(csv_source, DOCS_DIR / "benchmark.csv")
    print("✓ benchmark.csv copied to docs/")
else:
    print("⚠ benchmark.csv not found")