"""
IPL Player Performance & Auction Value Analysis
Complete Data Analysis Project — Resume Ready
Author: [Your Name]
"""

import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.gridspec import GridSpec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# ── Style ─────────────────────────────────────────────────────────────────────
DARK  = "#1a1a2e"
MID   = "#16213e"
BLUE  = "#0f3460"
ACC1  = "#e94560"   # red-pink accent
ACC2  = "#f5a623"   # gold
ACC3  = "#00b4d8"   # cyan
ACC4  = "#06d6a0"   # green
WHITE = "#f0f0f0"
GRAY  = "#888888"

plt.rcParams.update({
    "figure.facecolor": DARK,
    "axes.facecolor":   MID,
    "axes.edgecolor":   GRAY,
    "axes.labelcolor":  WHITE,
    "xtick.color":      GRAY,
    "ytick.color":      GRAY,
    "text.color":       WHITE,
    "grid.color":       "#2a2a4a",
    "grid.linewidth":   0.5,
    "font.family":      "DejaVu Sans",
    "axes.spines.top":  False,
    "axes.spines.right":False,
})

df = pd.read_csv("/home/claude/ipl_project/data/ipl_player_stats.csv")
print(f"Loaded {len(df)} records\n")

# ── Helper ────────────────────────────────────────────────────────────────────
def save(fig, name):
    path = f"/home/claude/ipl_project/charts/{name}.png"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=DARK)
    plt.close(fig)
    print(f"  Saved {name}.png")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 1 — Dashboard Overview (2x3 grid)
# ═══════════════════════════════════════════════════════════════════════════════
print("Generating Chart 1: Dashboard overview...")
fig = plt.figure(figsize=(18, 11), facecolor=DARK)
fig.suptitle("IPL Player Performance & Auction Value Analysis  |  2021–2023",
             fontsize=20, fontweight="bold", color=WHITE, y=0.98)
gs = GridSpec(2, 3, figure=fig, hspace=0.42, wspace=0.32)

# 1A — Avg runs by role
ax1 = fig.add_subplot(gs[0, 0])
role_runs = df.groupby("role")["runs"].mean().sort_values(ascending=True)
colors = [ACC3, ACC4, ACC2, ACC1, BLUE][:len(role_runs)]
bars = ax1.barh(role_runs.index, role_runs.values, color=colors, height=0.6)
ax1.set_title("Avg Runs per Season by Role", fontsize=11, color=WHITE, pad=8)
ax1.set_xlabel("Avg Runs")
for bar, val in zip(bars, role_runs.values):
    ax1.text(val + 5, bar.get_y() + bar.get_height()/2,
             f"{val:.0f}", va="center", fontsize=9, color=WHITE)
ax1.grid(axis="x", alpha=0.3)

# 1B — Auction price distribution by role (box)
ax2 = fig.add_subplot(gs[0, 1])
role_order = ["Batter", "Wicket-Keeper", "All-Rounder", "Bowler"]
data_by_role = [df[df["role"] == r]["auction_price_lakh"].values for r in role_order]
bp = ax2.boxplot(data_by_role, labels=role_order, patch_artist=True, notch=False,
                 medianprops=dict(color=ACC1, linewidth=2),
                 whiskerprops=dict(color=GRAY), capprops=dict(color=GRAY),
                 flierprops=dict(marker="o", color=ACC2, markersize=4, alpha=0.6))
box_colors = [ACC3, ACC4, ACC2, ACC1]
for patch, c in zip(bp["boxes"], box_colors):
    patch.set_facecolor(c); patch.set_alpha(0.7)
ax2.set_title("Auction Price Distribution by Role (₹ Lakh)", fontsize=11, color=WHITE, pad=8)
ax2.set_ylabel("Price (₹ Lakh)")
ax2.tick_params(axis="x", labelsize=8)
ax2.grid(axis="y", alpha=0.3)

# 1C — Top 10 run-scorers (3-year total)
ax3 = fig.add_subplot(gs[0, 2])
top_batters = (df.groupby("player_name")["runs"].sum()
                 .sort_values(ascending=False).head(10))
bars = ax3.barh(top_batters.index[::-1], top_batters.values[::-1],
                color=ACC2, height=0.65)
ax3.set_title("Top 10 Run Scorers (2021–2023 Total)", fontsize=11, color=WHITE, pad=8)
ax3.set_xlabel("Total Runs")
for bar, val in zip(bars, top_batters.values[::-1]):
    ax3.text(val + 10, bar.get_y() + bar.get_height()/2,
             str(int(val)), va="center", fontsize=8, color=WHITE)
ax3.grid(axis="x", alpha=0.3)

# 1D — Economy rate vs wickets (Bowlers & AR)
ax4 = fig.add_subplot(gs[1, 0])
bowl_df = df[df["role"].isin(["Bowler", "All-Rounder"]) & (df["wickets"] > 0)]
colors_map = {"Bowler": ACC1, "All-Rounder": ACC3}
for role, grp in bowl_df.groupby("role"):
    ax4.scatter(grp["economy_rate"], grp["wickets"],
                color=colors_map[role], alpha=0.7, s=40, label=role)
ax4.set_title("Economy Rate vs Wickets (Bowlers & AR)", fontsize=11, color=WHITE, pad=8)
ax4.set_xlabel("Economy Rate"); ax4.set_ylabel("Wickets")
ax4.legend(fontsize=8, facecolor=DARK, edgecolor=GRAY)
ax4.grid(alpha=0.3)

# 1E — Strike rate vs auction price
ax5 = fig.add_subplot(gs[1, 1])
bat_df = df[df["role"].isin(["Batter", "Wicket-Keeper"]) & (df["runs"] > 50)]
sc = ax5.scatter(bat_df["strike_rate"], bat_df["auction_price_lakh"],
                 c=bat_df["runs"], cmap="plasma", alpha=0.75, s=45, edgecolors="none")
cbar = fig.colorbar(sc, ax=ax5, pad=0.02)
cbar.set_label("Runs", color=WHITE, fontsize=8)
cbar.ax.yaxis.set_tick_params(color=WHITE); plt.setp(cbar.ax.yaxis.get_ticklabels(), color=WHITE)
ax5.set_title("Strike Rate vs Auction Price (Batters)", fontsize=11, color=WHITE, pad=8)
ax5.set_xlabel("Strike Rate"); ax5.set_ylabel("Auction Price (₹ Lakh)")
ax5.grid(alpha=0.3)

# 1F — Avg auction price by team
ax6 = fig.add_subplot(gs[1, 2])
team_avg = df.groupby("team")["auction_price_lakh"].mean().sort_values(ascending=True)
bars = ax6.barh(team_avg.index, team_avg.values, color=ACC4, height=0.65)
ax6.set_title("Avg Player Auction Price by Team (₹ Lakh)", fontsize=11, color=WHITE, pad=8)
ax6.set_xlabel("Avg Price (₹ Lakh)")
for bar, val in zip(bars, team_avg.values):
    ax6.text(val + 3, bar.get_y() + bar.get_height()/2,
             f"{val:.0f}", va="center", fontsize=8, color=WHITE)
ax6.grid(axis="x", alpha=0.3)

save(fig, "01_dashboard_overview")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 2 — Season-wise performance trends
# ═══════════════════════════════════════════════════════════════════════════════
print("Generating Chart 2: Season trends...")
fig, axes = plt.subplots(1, 3, figsize=(16, 5), facecolor=DARK)
fig.suptitle("Season-wise Performance Trends  |  2021 → 2023",
             fontsize=16, fontweight="bold", color=WHITE, y=1.02)

seasons = [2021, 2022, 2023]

# Avg runs per season by role
ax = axes[0]
for role, color in zip(["Batter", "All-Rounder", "Bowler", "Wicket-Keeper"],
                        [ACC2, ACC3, ACC1, ACC4]):
    vals = [df[(df["season"]==s) & (df["role"]==role)]["runs"].mean() for s in seasons]
    ax.plot(seasons, vals, marker="o", color=color, linewidth=2, label=role, markersize=7)
    ax.fill_between(seasons, vals, alpha=0.08, color=color)
ax.set_title("Avg Runs per Season by Role", fontsize=11, color=WHITE)
ax.set_xlabel("Season"); ax.set_ylabel("Avg Runs")
ax.legend(fontsize=8, facecolor=DARK, edgecolor=GRAY)
ax.set_xticks(seasons); ax.grid(alpha=0.3)

# Avg strike rate trend
ax = axes[1]
for role, color in zip(["Batter", "All-Rounder", "Wicket-Keeper"],
                        [ACC2, ACC3, ACC4]):
    vals = [df[(df["season"]==s) & (df["role"]==role)]["strike_rate"].mean() for s in seasons]
    ax.plot(seasons, vals, marker="s", color=color, linewidth=2, label=role, markersize=7)
ax.set_title("Avg Strike Rate Trend by Role", fontsize=11, color=WHITE)
ax.set_xlabel("Season"); ax.set_ylabel("Strike Rate")
ax.legend(fontsize=8, facecolor=DARK, edgecolor=GRAY)
ax.set_xticks(seasons); ax.grid(alpha=0.3)

# Avg auction price by season
ax = axes[2]
for role, color in zip(["Batter", "Bowler", "All-Rounder"],
                        [ACC2, ACC1, ACC3]):
    vals = [df[(df["season"]==s) & (df["role"]==role)]["auction_price_lakh"].mean() for s in seasons]
    ax.plot(seasons, vals, marker="D", color=color, linewidth=2.5, label=role, markersize=8)
ax.set_title("Avg Auction Price Trend by Role (₹ Lakh)", fontsize=11, color=WHITE)
ax.set_xlabel("Season"); ax.set_ylabel("Avg Price (₹ Lakh)")
ax.legend(fontsize=8, facecolor=DARK, edgecolor=GRAY)
ax.set_xticks(seasons); ax.grid(alpha=0.3)

plt.tight_layout()
save(fig, "02_season_trends")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 3 — Undervalued Players (the money slide)
# ═══════════════════════════════════════════════════════════════════════════════
print("Generating Chart 3: Undervalued players...")

# Composite performance score
df["perf_score"] = (
    df["runs"] * 0.25 +
    df["strike_rate"] * 0.20 +
    df["wickets"] * 15 +
    (1 / df["economy_rate"].replace(0, np.nan)).fillna(0) * 50 +
    df["fifties"] * 10 +
    df["hundreds"] * 30
)
# Normalize 0-100
mn, mx = df["perf_score"].min(), df["perf_score"].max()
df["perf_score_norm"] = ((df["perf_score"] - mn) / (mx - mn)) * 100

# Normalize price
mn2, mx2 = df["auction_price_lakh"].min(), df["auction_price_lakh"].max()
df["price_norm"] = ((df["auction_price_lakh"] - mn2) / (mx2 - mn2)) * 100

# Value ratio — high = undervalued
df["value_ratio"] = df["perf_score_norm"] / (df["price_norm"] + 1)

# Use 2023 season for recency
df23 = df[df["season"] == 2023].copy()
top_undervalued = df23.sort_values("value_ratio", ascending=False).head(10)
top_overvalued  = df23.sort_values("value_ratio", ascending=True).head(5)

fig, axes = plt.subplots(1, 2, figsize=(16, 7), facecolor=DARK)
fig.suptitle("Player Value Analysis  |  Performance vs Price (2023 Season)",
             fontsize=15, fontweight="bold", color=WHITE, y=1.01)

# Scatter: all players
ax = axes[0]
colors_role = {"Batter": ACC2, "Wicket-Keeper": ACC4, "All-Rounder": ACC3, "Bowler": ACC1}
for role, grp in df23.groupby("role"):
    ax.scatter(grp["perf_score_norm"], grp["price_norm"],
               color=colors_role[role], alpha=0.65, s=60, label=role)

# Annotate top undervalued
for _, row in top_undervalued.head(5).iterrows():
    ax.annotate(row["player_name"].split()[-1],
                (row["perf_score_norm"], row["price_norm"]),
                textcoords="offset points", xytext=(6, 6),
                fontsize=7.5, color=ACC4,
                arrowprops=dict(arrowstyle="-", color=ACC4, lw=0.6))

# Quadrant lines
ax.axvline(df23["perf_score_norm"].median(), color=GRAY, lw=0.8, linestyle="--", alpha=0.5)
ax.axhline(df23["price_norm"].median(),      color=GRAY, lw=0.8, linestyle="--", alpha=0.5)
ax.text(2, df23["price_norm"].median() + 2, "Overpriced", color=GRAY, fontsize=8, alpha=0.7)
ax.text(2, df23["price_norm"].median() - 8, "Undervalued", color=ACC4, fontsize=8, alpha=0.9)

ax.set_title("Performance Score vs Auction Price", fontsize=12, color=WHITE)
ax.set_xlabel("Performance Score (0–100)"); ax.set_ylabel("Price (normalised)")
ax.legend(fontsize=8, facecolor=DARK, edgecolor=GRAY)
ax.grid(alpha=0.3)

# Bar: Top 10 undervalued
ax = axes[1]
top_undervalued_sorted = top_undervalued.sort_values("value_ratio")
bar_colors = [ACC4 if v > top_undervalued_sorted["value_ratio"].median() else ACC3
              for v in top_undervalued_sorted["value_ratio"]]
bars = ax.barh(top_undervalued_sorted["player_name"],
               top_undervalued_sorted["value_ratio"],
               color=bar_colors, height=0.65)
ax.set_title("Top 10 Undervalued Players (2023)", fontsize=12, color=WHITE)
ax.set_xlabel("Value Ratio  (Higher = More Undervalued)")
for bar, (_, row) in zip(bars, top_undervalued_sorted.iterrows()):
    ax.text(bar.get_width() + 0.01,
            bar.get_y() + bar.get_height()/2,
            f"₹{row['auction_price_lakh']:.0f}L  |  Score:{row['perf_score_norm']:.1f}",
            va="center", fontsize=7.5, color=WHITE)
ax.grid(axis="x", alpha=0.3)
# Highlight the #1 pick
ax.get_yticklabels()[-1].set_color(ACC2)
ax.get_yticklabels()[-1].set_fontweight("bold")

plt.tight_layout()
save(fig, "03_undervalued_players")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 4 — Bowling deep dive
# ═══════════════════════════════════════════════════════════════════════════════
print("Generating Chart 4: Bowling analysis...")
bowl = df[df["role"].isin(["Bowler", "All-Rounder"]) & (df["wickets"] > 3)].copy()

fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor=DARK)
fig.suptitle("Bowling Performance Deep Dive  |  2021–2023",
             fontsize=15, fontweight="bold", color=WHITE, y=1.01)

# Top wicket-takers
ax = axes[0]
top_bowl = df.groupby("player_name")["wickets"].sum().sort_values(ascending=False).head(10)
bars = ax.barh(top_bowl.index[::-1], top_bowl.values[::-1], color=ACC1, height=0.65)
ax.set_title("Top 10 Wicket Takers (3-Year Total)", fontsize=12, color=WHITE)
ax.set_xlabel("Total Wickets")
for bar, val in zip(bars, top_bowl.values[::-1]):
    ax.text(val + 0.3, bar.get_y() + bar.get_height()/2,
            str(int(val)), va="center", fontsize=9, color=WHITE)
ax.grid(axis="x", alpha=0.3)

# Economy heatmap by team & season
ax = axes[1]
pivot = df[df["role"] == "Bowler"].pivot_table(
    values="economy_rate", index="team", columns="season", aggfunc="mean")
sns.heatmap(pivot, ax=ax, cmap="RdYlGn_r", annot=True, fmt=".1f",
            linewidths=0.4, linecolor=DARK,
            cbar_kws={"label": "Economy Rate"},
            annot_kws={"size": 9, "color": "white"})
ax.set_title("Avg Economy Rate — Bowlers by Team & Season", fontsize=12, color=WHITE)
ax.set_xlabel("Season"); ax.set_ylabel("Team")
ax.tick_params(colors=WHITE)
cbar = ax.collections[0].colorbar
cbar.ax.yaxis.set_tick_params(color=WHITE)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=WHITE)
cbar.set_label("Economy Rate", color=WHITE)

plt.tight_layout()
save(fig, "04_bowling_analysis")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 5 — Country & Team breakdown
# ═══════════════════════════════════════════════════════════════════════════════
print("Generating Chart 5: Country & team breakdown...")
fig, axes = plt.subplots(1, 2, figsize=(14, 6), facecolor=DARK)
fig.suptitle("Country & Team Composition Analysis",
             fontsize=15, fontweight="bold", color=WHITE, y=1.01)

# Country donut
ax = axes[0]
country_counts = df.drop_duplicates("player_name")["country"].value_counts()
explode = [0.05] * len(country_counts)
wedges, texts, autotexts = ax.pie(
    country_counts.values, labels=country_counts.index,
    autopct="%1.0f%%", startangle=140, explode=explode,
    colors=[ACC2, ACC3, ACC1, ACC4, BLUE, "#a855f7", "#f97316"],
    textprops={"color": WHITE, "fontsize": 9},
    wedgeprops={"linewidth": 1.5, "edgecolor": DARK})
for at in autotexts:
    at.set_color(DARK); at.set_fontweight("bold"); at.set_fontsize(8)
centre = plt.Circle((0, 0), 0.55, color=DARK)
ax.add_artist(centre)
ax.text(0, 0, f"{len(df['player_name'].unique())}\nPlayers", ha="center", va="center",
        fontsize=11, fontweight="bold", color=WHITE)
ax.set_title("Players by Country", fontsize=12, color=WHITE)

# Grouped bar: role split by team
ax = axes[1]
role_team = df.drop_duplicates(["player_name", "team"]).groupby(["team", "role"]).size().unstack(fill_value=0)
role_colors = [ACC2, ACC4, ACC3, ACC1]
role_team.plot(kind="bar", ax=ax, color=role_colors, edgecolor=DARK, linewidth=0.5)
ax.set_title("Role Distribution by Team", fontsize=12, color=WHITE)
ax.set_xlabel("Team"); ax.set_ylabel("Player Count")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right", fontsize=8)
ax.legend(fontsize=8, facecolor=DARK, edgecolor=GRAY)
ax.grid(axis="y", alpha=0.3)

plt.tight_layout()
save(fig, "05_country_team")

# ═══════════════════════════════════════════════════════════════════════════════
# CHART 6 — Correlation heatmap
# ═══════════════════════════════════════════════════════════════════════════════
print("Generating Chart 6: Correlation heatmap...")
cols = ["runs", "batting_avg", "strike_rate", "fours", "sixes",
        "wickets", "economy_rate", "auction_price_lakh"]
corr = df[cols].corr()

fig, ax = plt.subplots(figsize=(10, 8), facecolor=DARK)
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, ax=ax, mask=mask, cmap="coolwarm", center=0,
            annot=True, fmt=".2f", linewidths=0.4, linecolor=DARK,
            cbar_kws={"label": "Correlation"},
            annot_kws={"size": 9, "color": "white"})
ax.set_title("Correlation Matrix — Key Performance Metrics",
             fontsize=14, fontweight="bold", color=WHITE, pad=12)
ax.tick_params(colors=WHITE, labelsize=9)
cbar = ax.collections[0].colorbar
cbar.ax.yaxis.set_tick_params(color=WHITE)
plt.setp(cbar.ax.yaxis.get_ticklabels(), color=WHITE)
cbar.set_label("Correlation", color=WHITE)
plt.tight_layout()
save(fig, "06_correlation_heatmap")

# ── KEY INSIGHTS ──────────────────────────────────────────────────────────────
print("\n" + "="*55)
print("KEY INSIGHTS")
print("="*55)

top3_uv = top_undervalued.head(3)[["player_name","auction_price_lakh","perf_score_norm"]]
print("\nTop 3 Undervalued Players (2023):")
print(top3_uv.to_string(index=False))

print(f"\nCorrelation: Strike Rate vs Auction Price = {corr.loc['strike_rate','auction_price_lakh']:.2f}")
print(f"Correlation: Runs vs Auction Price        = {corr.loc['runs','auction_price_lakh']:.2f}")
print(f"Correlation: Wickets vs Auction Price     = {corr.loc['wickets','auction_price_lakh']:.2f}")

best_team_price = df.groupby("team")["auction_price_lakh"].mean().idxmax()
best_team_eco   = df[df["role"]=="Bowler"].groupby("team")["economy_rate"].mean().idxmin()
print(f"\nHighest avg player price team : {best_team_price}")
print(f"Best bowling economy team     : {best_team_eco}")

print("\nAll 6 charts saved to /home/claude/ipl_project/charts/")
print("Dataset saved to /home/claude/ipl_project/data/ipl_player_stats.csv")
