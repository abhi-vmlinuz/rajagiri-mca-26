"""Statistical engine: computes every number used in the report/slides.

Course-constrained toolkit: central tendency, dispersion, PMF/PDF, range
probabilities, Binomial model. OLS regression (allowed). No Poisson/Normal fits.

Writes results.json consumed by the LaTeX report and slide deck.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd
from scipy import stats

ROOT = Path(__file__).resolve().parents[1]
R = {}

df = pd.read_csv(ROOT / 'data' / 'ipl_2008_2018.csv')
n_matches = len(df)

# ---------------------------------------------------------------- descriptive
margin = df['result_margin'].dropna()          # excludes the 1 tie
target = df['target_runs']

def describe(s):
    return {
        'n': int(s.count()), 'mean': float(s.mean()), 'median': float(s.median()),
        'mode': float(s.mode().iloc[0]), 'std': float(s.std(ddof=1)),
        'var': float(s.var(ddof=1)), 'min': float(s.min()), 'max': float(s.max()),
        'q1': float(s.quantile(.25)), 'q3': float(s.quantile(.75)),
        'iqr': float(s.quantile(.75) - s.quantile(.25)),
        'range': float(s.max() - s.min()),
        'cv': float(s.std(ddof=1) / s.mean()),
        'skew': float(s.skew()), 'kurt': float(s.kurtosis()),
    }

R['meta'] = {
    'source_rows': 1169, 'window_rows': n_matches + 10, 'dropped_noresult': 10,
    'ties_kept': int((df.result == 'tie').sum()), 'n': n_matches,
    'variables': 10, 'seasons': '2008-2018 (seasons 1-11)',
}
R['descriptive'] = {'result_margin': describe(margin), 'target_runs': describe(target)}

# ------------------------------------------------------- PMF / range probs
# Empirical PMF of result_margin for chased matches (wickets: integer margins)
wicket_margins = df.loc[df.result == 'wickets', 'result_margin'].dropna().astype(int)
pmf = wicket_margins.value_counts(normalize=True).sort_index()
R['pmf_wickets'] = {
    'n': int(len(wicket_margins)),
    'support_min': int(pmf.index.min()), 'support_max': int(pmf.index.max()),
    'pmf': {int(k): float(v) for k, v in pmf.items()},
    'mode': int(pmf.idxmax()), 'max_pmf': float(pmf.max()),
}

def rng(a, b):
    m = target[(target >= a) & (target <= b)]
    return float(len(m)) / len(target)

R['range_prob'] = {
    'P(140<=T<=160)': rng(140, 160),
    'P(161<=T<=190)': rng(161, 190),
    'P(T>200)': float((target > 200).sum()) / len(target),
    'P(T<120)': float((target < 120).sum()) / len(target),
    'P(margin>50)': float((margin > 50).sum()) / len(margin),
    'P(margin>=100)': float((margin >= 100).sum()) / len(margin),
}

# ---------------------------------------------------------------- binomial
def binom_test(k, n, p0=0.5):
    """Two-sided exact binomial test via scipy."""
    res = stats.binomtest(k, n, p0)
    return {'k': int(k), 'n': int(n), 'p_hat': k / n, 'p_value': float(res.pvalue),
            'ci95': [float(res.proportion_ci(0.95).low), float(res.proportion_ci(0.95).high)]}

bat_first = df[df.toss_decision == 'bat']
toss_bat = bat_first[bat_first.toss_winner == bat_first.winner]
chased = df[df.toss_decision == 'field']
toss_field_win = chased[chased.toss_winner == chased.winner]

R['binomial'] = {
    'bat_first_win': binom_test(len(toss_bat), len(bat_first)),
    'field_first_win': binom_test(len(toss_field_win), len(chased)),
    'overall_toss_luck': binom_test(int((df.toss_winner == df.winner).sum()), n_matches),
}

# Team dominance: MI win rate across all their matches in window
mi_games = int(((df.team1 == 'Mumbai Indians') | (df.team2 == 'Mumbai Indians')).sum())
mi_wins = int((df.winner == 'Mumbai Indians').sum())
csk_games = int(((df.team1 == 'Chennai Super Kings') | (df.team2 == 'Chennai Super Kings')).sum())
csk_wins = int((df.winner == 'Chennai Super Kings').sum())
R['team_dominance'] = {
    'MI': {'games': mi_games, 'wins': mi_wins, **binom_test(mi_wins, mi_games)},
    'CSK': {'games': csk_games, 'wins': csk_wins, **binom_test(csk_wins, csk_games)},
}

# ------------------------------------------------------------ OLS regression
x = df.groupby('season')['target_runs'].mean().reset_index()
slope, intercept, r_val, p_val, stderr = stats.linregress(x.season, x.target_runs)
R['regression'] = {
    'slope': float(slope), 'intercept': float(intercept), 'r': float(r_val),
    'r2': float(r_val**2), 'p_value': float(p_val), 'stderr': float(stderr),
    'points': x.to_dict('records'),
}

# Per-match scatter data for R plot (season vs target)
R['scatter_n'] = n_matches

out = ROOT / 'results.json'
out.write_text(json.dumps(R, indent=2))
print(json.dumps(R, indent=2)[:1500])
print("...\nFull results ->", out)
