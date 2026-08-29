"""Prepare the analysis dataset: filter to 2008-2018, keep the 10 chosen variables.

Output: data/ipl_2008_2018.csv used by all downstream analysis (R visuals + Python stats).
"""
import pandas as pd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'data'
OUT.mkdir(exist_ok=True)

KEEP = ['team1', 'team2', 'season', 'toss_winner', 'toss_decision', 'winner',
        'venue', 'result', 'result_margin', 'target_runs']

df = pd.read_csv(ROOT / 'ipl.csv')
df['match_date'] = pd.to_datetime(df['match_date'])

# Window: seasons 1-11 == calendar 2008-2018 (season N runs in year 2007+N)
sub = df[df['match_date'] <= '2018-12-31'].copy()
sub['year'] = sub['match_date'].dt.year

# Sanity: season code vs calendar year must be consistent
assert (sub['season'] == sub['year'] - 2007).all(), "season/year mismatch"

# Drop abandoned / no-result matches: no winner, no margin -> not usable for win modeling
abandoned = sub['winner'].isna().sum()
clean = sub.dropna(subset=['winner']).copy()

# target_runs missing only for abandoned matches; verify nothing left missing there
clean = clean.dropna(subset=['target_runs'])

# NOTE: exactly 1 tie remains (Pune Warriors v KXIP, season 6) with result_margin NaN.
# Kept by design: ties have no margin. Margin-based statistics exclude it via dropna.
final = clean[KEEP].reset_index(drop=True)

n_ties = int((final['result'] == 'tie').sum())
print(f"Ties kept (no margin) : {n_ties}")

print(f"Source rows 2008-2018 : {len(sub)}")
print(f"Dropped (no result)   : {abandoned}")
print(f"Final analysis rows   : {len(final)}")
print(f"Variables kept        : {len(KEEP)} -> {KEEP}")
print(f"Nulls remaining       : {int(final.isnull().sum().sum())}")
print(f"Seasons               : {sorted(final.season.unique())}")

final.to_csv(OUT / 'ipl_2008_2018.csv', index=False)
print(f"\nWritten: {OUT/'ipl_2008_2018.csv'}")
