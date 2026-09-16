import sqlite3
import matplotlib.pyplot as plt
import numpy as np

connection = sqlite3.connect("token_tracker.db")
cursor = connection.cursor()

cursor.execute("SELECT employee_name, provider, cost FROM usage_log WHERE id BETWEEN 99 AND 118 ORDER BY id")
rows = cursor.fetchall()
connection.close()

claude_costs = {}
gemini_costs = {}

for name, provider, cost in rows:
    if provider == "Claude":
        claude_costs[name] = cost
    elif provider == "Gemini":
        gemini_costs[name] = cost

names = sorted(set(list(claude_costs.keys()) + list(gemini_costs.keys())),
               key=lambda n: claude_costs.get(n, 0), reverse=True)

claude_values = [claude_costs.get(n, 0) for n in names]
gemini_values = [gemini_costs.get(n, 0) for n in names]

y = np.arange(len(names))
height = 0.35

plt.style.use("default")
plt.rcParams["font.family"] = "sans-serif"

fig, ax = plt.subplots(figsize=(11, 8))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

bars1 = ax.barh(y + height/2, claude_values, height, color="#2B2D42", label="Claude")
bars2 = ax.barh(y - height/2, gemini_values, height, color="#3CA6A6", label="Gemini")

max_val = max(claude_values + gemini_values)

for bar, val in zip(bars1, claude_values):
    if val > 0:
        ax.text(bar.get_width() + max_val*0.02, bar.get_y() + bar.get_height()/2,
                "${:.4f}".format(val), va="center", fontsize=9, color="#2B2D42", fontweight="bold")

for bar, val in zip(bars2, gemini_values):
    if val > 0:
        ax.text(bar.get_width() + max_val*0.02, bar.get_y() + bar.get_height()/2,
                "${:.6f}".format(val), va="center", fontsize=9, color="#3CA6A6", fontweight="bold")

ax.set_yticks(y)
ax.set_yticklabels(names, fontsize=12, color="#1a1a1a")
ax.invert_yaxis()

fig.text(0.06, 0.97, "Claude vs Gemini: Cost per Employee", fontsize=20, fontweight="bold", color="#1a1a1a")
fig.text(0.06, 0.945, "Same 10 employees, same questions, two providers, both on paid tier", fontsize=11, color="#888888")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)
ax.tick_params(axis="x", labelsize=0, length=0)
ax.set_xlim(0, max_val * 1.4)

ax.legend(loc="lower right", frameon=False, fontsize=11)

plt.subplots_adjust(top=0.90, left=0.15, right=0.95, bottom=0.03)
plt.savefig("cost_chart.png", dpi=200, facecolor="white")
print("Chart saved as cost_chart.png")