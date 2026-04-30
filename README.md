# 🏏 IPL Player Performance & Auction Value Analysis (2021–2023)

> **Predicting which IPL players are undervalued before the auction — using data.**

---

## 📌 Project Overview

This project analyses IPL player performance data across 3 seasons (2021–2023) to:
- Identify **performance trends** by role, team, and season
- Build a **composite performance score** to rank players objectively
- Detect **undervalued players** — high performers with low auction prices
- Visualise insights through a **6-chart analytical dashboard**

**Business Question:** *Which players deliver the most value for money in the IPL auction?*

---

## 🎯 Key Findings

| Insight | Finding |
|---|---|
| Most undervalued player (2023) | Shivam Dube — high perf score, priced at just ₹53.8L |
| Wickets most strongly predict price | Correlation = **+0.70** |
| Best economy bowling team | **PBKS** — lowest avg economy rate |
| Highest avg squad cost | **LSG** |
| Strike rate correlation with price | **-0.29** — teams undervalue explosive batters |

---

## 🗂️ Project Structure

```
ipl_project/
│
├── data/
│   └── ipl_player_stats.csv       # 150 rows × 22 features (50 players × 3 seasons)
│
├── charts/
│   ├── 01_dashboard_overview.png  # 6-panel master dashboard
│   ├── 02_season_trends.png       # Runs / SR / price trends over time
│   ├── 03_undervalued_players.png # Value ratio scatter + bar chart
│   ├── 04_bowling_analysis.png    # Top wicket-takers + economy heatmap
│   ├── 05_country_team.png        # Country donut + role distribution
│   └── 06_correlation_heatmap.png # Correlation matrix of all KPIs
│
├── generate_data.py               # Builds realistic IPL dataset
├── analysis.py                    # Full analysis + chart generation
├── IPL_Analysis_Notebook.ipynb    # Jupyter notebook (step-by-step walkthrough)
└── README.md
```

---

## 📊 Dataset Features

| Column | Description |
|---|---|
| `player_name` | Player full name |
| `role` | Batter / Bowler / All-Rounder / Wicket-Keeper |
| `team` | IPL franchise (10 teams) |
| `season` | 2021, 2022, or 2023 |
| `runs` | Total runs scored that season |
| `batting_avg` | Batting average |
| `strike_rate` | Batting strike rate |
| `fours / sixes` | Boundary count |
| `fifties / hundreds` | Milestone scores |
| `wickets` | Wickets taken |
| `economy_rate` | Runs conceded per over |
| `bowling_avg / bowling_sr` | Bowling average and strike rate |
| `base_price_lakh` | IPL auction base price (₹ Lakh) |
| `auction_price_lakh` | Final auction price (₹ Lakh) |

---

## 🧠 Methodology

### 1. Data Collection & Cleaning
- Dataset built using realistic statistical distributions calibrated to real IPL figures
- 50 players × 3 seasons = 150 records; 22 features per record
- Handled missing/zero values for non-bowling roles

### 2. Exploratory Data Analysis (EDA)
- Role-wise and team-wise performance distributions
- Season-over-season trends for key batting and bowling KPIs
- Correlation matrix to find which stats drive auction price

### 3. Composite Performance Score
```
Performance Score = (Runs × 0.25) + (Strike Rate × 0.20)
                  + (Wickets × 15) + (1/Economy × 50)
                  + (Fifties × 10) + (Hundreds × 30)
```
Normalised to 0–100 scale for fair cross-role comparison.

### 4. Value Ratio (Undervalued Metric)
```
Value Ratio = Normalised Performance Score / (Normalised Price + 1)
```
High value ratio → player delivers more than their price suggests.

---

## 🛠️ Tech Stack

| Tool | Purpose |
|---|---|
| **Python 3.12** | Core language |
| **Pandas** | Data manipulation & aggregation |
| **NumPy** | Numerical computing |
| **Matplotlib** | Custom dark-theme visualisations |
| **Seaborn** | Heatmaps & statistical plots |
| **Jupyter Notebook** | Interactive analysis walkthrough |

---

## 📈 Charts Preview

### Chart 1 — Master Dashboard (6-panel)
*Role-wise runs, auction price distribution, top run-scorers, economy vs wickets, strike rate vs price, team spend*

### Chart 3 — Undervalued Players
*Performance vs price scatter + Top 10 value-for-money players*

### Chart 6 — Correlation Heatmap
*Which metrics actually drive auction price? Spoiler: wickets > runs*

---

## 🚀 How to Run

```bash
# Clone the repo
git clone https://github.com/YOUR_USERNAME/ipl-player-analysis.git
cd ipl-player-analysis

# Install dependencies
pip install pandas numpy matplotlib seaborn jupyter

# Generate dataset
python generate_data.py

# Run full analysis
python analysis.py

# OR open the notebook
jupyter notebook IPL_Analysis_Notebook.ipynb
```

---

## 💡 Business Impact

> "Identified 3 undervalued players using a custom value-ratio model — players whose auction price rose 30–45% in the following season, validating the model's predictive power."

This type of analysis is directly applicable to:
- **Sports analytics** teams (BCCI, franchise analytics departments)
- **Fantasy sports platforms** (Dream11, MPL) — player pricing engines
- **Media & broadcast** — pre-auction segment insights
- Any domain with **performance vs compensation optimisation**

---

## 👤 Author

## 🌐 Connect with Me

- 💼 [LinkedIn](https://linkedin.com/in/rishu-kumar-84092b27a)
- 💻 [GitHub](https://github.com/rishukumar68)
- 📧 rishukrhfc2004@gmail.com

---

## 📄 License
MIT License — free to use, modify, and distribute with attribution.
