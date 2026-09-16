import sqlite3
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

connection = sqlite3.connect("token_tracker.db")
cursor = connection.cursor()

cursor.execute("""
    SELECT guardrail_blocked, guardrail_reason
    FROM usage_log
    WHERE guardrail_checked = 1 AND provider = 'Claude'
""")
rows = cursor.fetchall()
connection.close()

total = len(rows)
blocked = sum(1 for r in rows if r[0])
allowed = total - blocked

reason_counts = {}
for is_blocked, reason in rows:
    if is_blocked and reason:
        reason_counts[reason] = reason_counts.get(reason, 0) + 1

navy = "#1B2340"
slate = "#5B6B8C"
amber = "#C97B2E"
bg = "#F7F8FA"
panel = "#FFFFFF"
grid = "#E4E7EC"

plt.rcParams["font.family"] = "sans-serif"
fig = plt.figure(figsize=(11, 5.5), facecolor=bg)

fig.text(0.05, 0.94, "Guardrail Enforcement Summary", fontsize=18,
          fontweight="bold", color=navy, family="sans-serif")
fig.text(0.05, 0.885, "Model Armor \u00b7 token-simulator-guardrails \u00b7 cumulative across all test runs",
          fontsize=10.5, color=slate)

tile_y, tile_h = 0.60, 0.22
tile_w = 0.28
tile_specs = [
    (0.05, str(total), "Requests checked", navy),
    (0.05 + tile_w + 0.02, str(allowed), "Allowed", slate),
    (0.05 + 2 * (tile_w + 0.02), str(blocked), "Blocked", amber),
]

for x, number, label, color in tile_specs:
    ax_tile = fig.add_axes([x, tile_y, tile_w, tile_h])
    ax_tile.set_xlim(0, 1)
    ax_tile.set_ylim(0, 1)
    ax_tile.axis("off")
    box = FancyBboxPatch((0, 0), 1, 1, boxstyle="round,pad=0,rounding_size=0.04",
                          linewidth=1, edgecolor=grid, facecolor=panel,
                          transform=ax_tile.transData)
    ax_tile.add_patch(box)
    ax_tile.text(0.08, 0.62, number, fontsize=30, fontweight="bold",
                  color=color, ha="left", va="center")
    ax_tile.text(0.08, 0.22, label, fontsize=11, color=slate, ha="left", va="center")

bar_ax = fig.add_axes([0.05, 0.34, 0.90, 0.10])
bar_ax.set_xlim(0, total)
bar_ax.set_ylim(0, 1)
bar_ax.axis("off")

bar_ax.barh(0.5, allowed, height=0.9, color=slate, left=0, edgecolor=bg, linewidth=2)
bar_ax.barh(0.5, blocked, height=0.9, color=amber, left=allowed, edgecolor=bg, linewidth=2)

bar_ax.text(allowed / 2, 0.5, f"{allowed} allowed", ha="center", va="center",
             fontsize=10.5, color="white", fontweight="bold")
bar_ax.text(allowed + blocked / 2, 0.5, f"{blocked} blocked", ha="center", va="center",
             fontsize=10.5, color="white", fontweight="bold")

reason_ax = fig.add_axes([0.05, 0.06, 0.90, 0.20])
reason_ax.axis("off")
reason_ax.text(0, 0.85, "Blocked by", fontsize=10.5, color=slate, fontweight="bold")

y_pos = 0.45
for reason, count in sorted(reason_counts.items(), key=lambda x: -x[1]):
    reason_ax.add_patch(plt.Rectangle((0, y_pos - 0.06), 0.012, 0.14,
                                        color=amber, transform=reason_ax.transAxes))
    reason_ax.text(0.02, y_pos, f"{reason.replace('_', ' ')}", fontsize=11,
                    color=navy, va="center")
    reason_ax.text(0.32, y_pos, f"{count}", fontsize=11, color=slate,
                    va="center", fontweight="bold")
    y_pos -= 0.35

plt.savefig("guardrail_chart.png", dpi=200, facecolor=bg)
print("Chart saved as guardrail_chart.png")