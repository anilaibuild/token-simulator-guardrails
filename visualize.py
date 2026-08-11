import sqlite3
import matplotlib.pyplot as plt

connection = sqlite3.connect("token_tracker.db")
cursor = connection.cursor()

cursor.execute("SELECT employee_name, cost FROM usage_log")
rows = cursor.fetchall()

connection.close()

rows.sort(key=lambda row: row[1])

names = []
costs = []

for row in rows:
    names.append(row[0])
    costs.append(row[1])

total_cost = sum(costs)
max_cost = max(costs)

# Highlight only the top spender, everyone else stays neutral gray
colors = []
for cost in costs:
    if cost == max_cost:
        colors.append("#D62839")
    else:
        colors.append("#D9D9D9")

plt.style.use("default")
plt.rcParams["font.family"] = "sans-serif"

fig, ax = plt.subplots(figsize=(11, 7.5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

bars = ax.barh(names, costs, color=colors, height=0.55)

for bar, cost in zip(bars, costs):
    width = bar.get_width()
    percentage = (cost / total_cost) * 100
    label = "$" + str(round(cost, 4)) + "   " + str(round(percentage, 1)) + "%"
    text_color = "#D62839" if cost == max_cost else "#666666"
    weight = "bold" if cost == max_cost else "normal"
    ax.text(
        width + (max_cost * 0.02),
        bar.get_y() + bar.get_height() / 2,
        label,
        va="center",
        fontsize=11,
        color=text_color,
        fontweight=weight
    )

fig.text(0.06, 0.96, "Who's Spending the Most?", fontsize=24, fontweight="bold", color="#1a1a1a")
fig.text(0.06, 0.925, "Token API cost by employee, this batch", fontsize=12, color="#888888")

ax.set_xlabel("")
ax.set_ylabel("")

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_visible(False)
ax.spines["bottom"].set_visible(False)

ax.tick_params(axis="y", labelsize=13, colors="#333333", length=0)
ax.tick_params(axis="x", labelsize=0, length=0)

ax.set_xlim(0, max_cost * 1.4)
ax.grid(False)

plt.subplots_adjust(top=0.87, left=0.12, right=0.95, bottom=0.05)
plt.savefig("cost_chart.png", dpi=200, facecolor="white")
print("Chart saved as cost_chart.png")