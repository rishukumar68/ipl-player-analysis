import pandas as pd
import numpy as np
import random

np.random.seed(42)
random.seed(42)

# ── Players ──────────────────────────────────────────────────────────────────
players = [
    # Name, Role, Country, Base Price (Lakh)
    ("Virat Kohli",       "Batter",      "India",       200),
    ("Rohit Sharma",      "Batter",      "India",       200),
    ("KL Rahul",          "Batter",      "India",       150),
    ("Shubman Gill",      "Batter",      "India",       100),
    ("Ruturaj Gaikwad",   "Batter",      "India",        75),
    ("Yashasvi Jaiswal",  "Batter",      "India",        20),
    ("Ishan Kishan",      "Batter",      "India",        60),
    ("Devdutt Padikkal",  "Batter",      "India",        20),
    ("Tilak Varma",       "Batter",      "India",        20),
    ("Rinku Singh",       "Batter",      "India",        20),
    ("MS Dhoni",          "Wicket-Keeper","India",       200),
    ("Sanju Samson",      "Wicket-Keeper","India",        80),
    ("Rishabh Pant",      "Wicket-Keeper","India",       200),
    ("Jasprit Bumrah",    "Bowler",      "India",       200),
    ("Mohammed Shami",    "Bowler",      "India",       200),
    ("Yuzvendra Chahal",  "Bowler",      "India",       100),
    ("Ravindra Jadeja",   "All-Rounder", "India",       200),
    ("Hardik Pandya",     "All-Rounder", "India",       150),
    ("Axar Patel",        "All-Rounder", "India",        75),
    ("Washington Sundar", "All-Rounder", "India",        50),
    ("Shivam Dube",       "All-Rounder", "India",        20),
    ("Jos Buttler",       "Batter",      "England",      150),
    ("Jonny Bairstow",    "Batter",      "England",      100),
    ("Sam Curran",        "All-Rounder", "England",      100),
    ("Liam Livingstone",  "All-Rounder", "England",       75),
    ("David Warner",      "Batter",      "Australia",    150),
    ("Steve Smith",       "Batter",      "Australia",    125),
    ("Glenn Maxwell",     "All-Rounder", "Australia",    125),
    ("Mitchell Starc",    "Bowler",      "Australia",    200),
    ("Pat Cummins",       "Bowler",      "Australia",    200),
    ("Faf du Plessis",    "Batter",      "South Africa", 100),
    ("Quinton de Kock",   "Wicket-Keeper","South Africa", 100),
    ("Kagiso Rabada",     "Bowler",      "South Africa", 150),
    ("Anrich Nortje",     "Bowler",      "South Africa", 100),
    ("Heinrich Klaasen",  "Wicket-Keeper","South Africa",  75),
    ("Suryakumar Yadav",  "Batter",      "India",        150),
    ("Deepak Chahar",     "Bowler",      "India",         75),
    ("Trent Boult",       "Bowler",      "New Zealand",   125),
    ("Sunil Narine",      "All-Rounder", "West Indies",   100),
    ("Andre Russell",     "All-Rounder", "West Indies",   125),
    ("Nicholas Pooran",   "Wicket-Keeper","West Indies",   75),
    ("Kieron Pollard",    "All-Rounder", "West Indies",    75),
    ("Mohammed Siraj",    "Bowler",      "India",          75),
    ("Arshdeep Singh",    "Bowler",      "India",          50),
    ("Kuldeep Yadav",     "Bowler",      "India",          75),
    ("R Ashwin",          "All-Rounder", "India",         125),
    ("Dinesh Karthik",    "Wicket-Keeper","India",          75),
    ("Mayank Agarwal",    "Batter",      "India",          75),
    ("Manish Pandey",     "Batter",      "India",          50),
    ("Ambati Rayudu",     "Batter",      "India",          50),
]

teams = ["MI", "CSK", "RCB", "KKR", "DC", "SRH", "PBKS", "RR", "GT", "LSG"]
seasons = [2021, 2022, 2023]
venues = {
    "MI":   "Wankhede Stadium, Mumbai",
    "CSK":  "MA Chidambaram Stadium, Chennai",
    "RCB":  "M Chinnaswamy Stadium, Bangalore",
    "KKR":  "Eden Gardens, Kolkata",
    "DC":   "Arun Jaitley Stadium, Delhi",
    "SRH":  "Rajiv Gandhi Intl Stadium, Hyderabad",
    "PBKS": "PCA Stadium, Mohali",
    "RR":   "Sawai Mansingh Stadium, Jaipur",
    "GT":   "Narendra Modi Stadium, Ahmedabad",
    "LSG":  "Ekana Cricket Stadium, Lucknow",
}

def batting_stats(role, season_idx):
    """Generate per-season batting stats based on role."""
    base = {"Batter": 380, "Wicket-Keeper": 340, "All-Rounder": 280, "Bowler": 60}[role]
    runs = max(0, int(np.random.normal(base, base * 0.25)))
    matches = random.randint(10, 16)
    innings = matches - random.randint(0, 2)
    sr_base = {"Batter": 138, "Wicket-Keeper": 132, "All-Rounder": 148, "Bowler": 115}[role]
    sr = round(np.random.normal(sr_base, 12), 1)
    avg_base = runs / max(innings - random.randint(0, 3), 1)
    avg = round(max(0, np.random.normal(avg_base, 5)), 1)
    fours = int(runs * random.uniform(0.08, 0.14))
    sixes = int(runs * random.uniform(0.05, 0.13))
    fifties = int(runs // 120 + random.randint(0, 2))
    hundreds = 1 if runs > 500 and random.random() > 0.5 else 0
    return runs, matches, innings, round(avg, 1), sr, fours, sixes, fifties, hundreds

def bowling_stats(role, season_idx):
    """Generate per-season bowling stats based on role."""
    base_wkts = {"Bowler": 18, "All-Rounder": 10, "Batter": 1, "Wicket-Keeper": 0}[role]
    wickets = max(0, int(np.random.normal(base_wkts, base_wkts * 0.35 + 1)))
    overs = max(0, round(np.random.normal({"Bowler": 52, "All-Rounder": 28, "Batter": 4, "Wicket-Keeper": 0}[role], 10), 1))
    eco_base = {"Bowler": 7.8, "All-Rounder": 8.4, "Batter": 9.5, "Wicket-Keeper": 10.0}[role]
    economy = round(max(5.0, np.random.normal(eco_base, 0.8)), 2)
    avg = round((economy * overs) / max(wickets, 1), 1)
    sr = round((overs * 6) / max(wickets, 1), 1)
    return wickets, round(overs, 1), economy, avg, sr

rows = []
for idx, (name, role, country, base_price) in enumerate(players):
    team = teams[idx % len(teams)]
    for s_idx, season in enumerate(seasons):
        runs, matches, innings, avg, sr, fours, sixes, fifties, hundreds = batting_stats(role, s_idx)
        wickets, overs, economy, bowl_avg, bowl_sr = bowling_stats(role, s_idx)

        # Auction price = base * multiplier driven by performance
        perf_score = (runs * 0.3 + wickets * 20 + sr * 0.5) / 100
        multiplier = max(1.0, perf_score + np.random.normal(0, 0.5))
        auction_price = round(base_price * multiplier, 1)
        if auction_price > 2000: auction_price = 2000.0  # cap at 20 Cr

        rows.append({
            "player_name": name,
            "role": role,
            "country": country,
            "team": team,
            "home_venue": venues[team],
            "season": season,
            "matches": matches,
            "innings": innings,
            "runs": runs,
            "batting_avg": avg,
            "strike_rate": sr,
            "fours": fours,
            "sixes": sixes,
            "fifties": fifties,
            "hundreds": hundreds,
            "wickets": wickets,
            "overs_bowled": overs,
            "economy_rate": economy,
            "bowling_avg": bowl_avg,
            "bowling_sr": bowl_sr,
            "base_price_lakh": base_price,
            "auction_price_lakh": auction_price,
        })

df = pd.DataFrame(rows)
df.to_csv("/home/claude/ipl_project/data/ipl_player_stats.csv", index=False)
print(f"Dataset created: {len(df)} rows, {df['player_name'].nunique()} players, {df['season'].nunique()} seasons")
print(df.head(3).to_string())
