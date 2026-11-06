"""Create a dependency-free SVG runtime chart from the benchmark CSV."""
import csv
from pathlib import Path

rows = list(csv.DictReader(open("images/runtime_results.csv", encoding="utf-8")))
values = [float(row["seconds"]) for row in rows]
maximum = max(values) or 1.0
bars = []
for index, (row, value) in enumerate(zip(rows, values)):
	height = 260 * value / maximum
	x = 80 + index * 180
	y = 330 - height
	bars.append(f'<rect x="{x}" y="{y:.2f}" width="90" height="{height:.2f}" fill="#24527a"/>')
	bars.append(f'<text x="{x + 45}" y="355" text-anchor="middle" font-size="12">{row["component"]}</text>')
	bars.append(f'<text x="{x + 45}" y="{y - 8:.2f}" text-anchor="middle" font-size="11">{value:.6f}s</text>')
svg = """<svg xmlns="http://www.w3.org/2000/svg" width="850" height="420" viewBox="0 0 850 420">
<rect width="100%" height="100%" fill="#f7f9fb"/><text x="425" y="35" text-anchor="middle" font-size="22" font-family="sans-serif">Mini-Courier Planner Component Runtime</text>
<line x1="55" y1="330" x2="800" y2="330" stroke="#23395d"/>""" + "".join(bars) + "</svg>"
Path("images/runtime_chart.svg").write_text(svg, encoding="utf-8")
print("Saved images/runtime_chart.svg")
