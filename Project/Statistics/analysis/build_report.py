#!/usr/bin/env python3
"""Substitute computed values from results.json into report.template.tex
to produce the final report.tex. All layout lives in the template; this
script only injects real numeric results."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / 'results.json').read_text())

d = R['descriptive']
tm, mm = d['target_runs'], d['result_margin']
b = R['binomial']
rb = R['range_prob']
pm = R['pmf_wickets']
reg = R['regression']
csk = R['team_dominance']['CSK']
mi = R['team_dominance']['MI']

S = {
    # central tendency / dispersion
    'MEAN_TM': f"{tm['mean']:.2f}", 'MED_TM': f"{tm['median']:.0f}", 'MODE_TM': f"{tm['mode']:.0f}",
    'MEAN_MM': f"{mm['mean']:.2f}", 'MED_MM': f"{mm['median']:.0f}",
    'SD_TM': f"{tm['std']:.2f}", 'SD_MM': f"{mm['std']:.2f}",
    'CV_MM': f"{mm['cv']:.3f}", 'CV_TM': f"{tm['cv']:.3f}",
    'Q1_TM': f"{tm['q1']:.0f}", 'Q3_TM': f"{tm['q3']:.0f}", 'IQR_TM': f"{tm['iqr']:.0f}",
    'Q1_MM': f"{mm['q1']:.0f}", 'Q3_MM': f"{mm['q3']:.0f}", 'IQR_MM': f"{mm['iqr']:.0f}",
    'MAX_MM': f"{mm['max']:.0f}",
    'SKEW_MM': f"{mm['skew']:.2f}", 'SKEW_TM': f"{tm['skew']:.2f}",
    # binomial
    'N_BAT': b['bat_first_win']['n'], 'K_BAT': b['bat_first_win']['k'],
    'PHAT_BAT': f"{b['bat_first_win']['p_hat']:.3f}",
    'PV_BAT': f"{b['bat_first_win']['p_value']:.3f}",
    'N_FIELD': b['field_first_win']['n'], 'K_FIELD': b['field_first_win']['k'],
    'PHAT_FIELD': f"{b['field_first_win']['p_hat']:.3f}",
    'PV_FIELD': f"{b['field_first_win']['p_value']:.3f}",
    'CIB_LO': f"{b['bat_first_win']['ci95'][0]:.3f}",
    'CIB_HI': f"{b['bat_first_win']['ci95'][1]:.3f}",
    'CIF_LO': f"{b['field_first_win']['ci95'][0]:.3f}",
    'CIF_HI': f"{b['field_first_win']['ci95'][1]:.3f}",
    # pmf
    'N_PM': pm['n'], 'MODE_PM': pm['mode'], 'MAXP_PM': f"{pm['max_pmf']:.3f}",
    # range probs
    'P_140_160': f"{rb['P(140<=T<=160)']:.3f}",
    'P_161_190': f"{rb['P(161<=T<=190)']:.3f}",
    'P_GT200': f"{rb['P(T>200)']:.3f}",
    'P_LT120': f"{rb['P(T<120)']:.3f}",
    'P_M50': f"{rb['P(margin>50)']:.3f}",
    'P_M100': f"{rb['P(margin>=100)']:.3f}",
    # regression
    'REG_INT': f"{reg['intercept']:.2f}", 'REG_SLP': f"{reg['slope']:.2f}",
    'REG_SLP_R1': f"{reg['slope']:.1f}", 'REG_R2': f"{reg['r2']:.3f}",
    'REG_PV': f"{reg['p_value']:.3f}",
    # team dominance
    'CSK_W': csk['wins'], 'CSK_G': csk['games'], 'CSK_P': f"{csk['p_hat']:.3f}",
    'CSK_PV': f"{csk['p_value']:.3f}",
    'MI_P': f"{mi['p_hat']:.3f}",
}

tpl = (ROOT / 'report' / 'report.template.tex').read_text()
out = tpl
# Replace longer/more-specific tokens FIRST so prefix collisions (e.g. CSK_PV
# vs CSK_P, REG_SLP_R1 vs REG_SLP) resolve correctly.
for key in sorted(S, key=len, reverse=True):
    out = out.replace(key, str(S[key]))

# Any placeholder left untouched means a bug -- fail loudly rather than silently
leftover = [k for k in S if k in out]
if leftover:
    raise SystemExit(f"Unresolved placeholders remain: {leftover}")

# The *100% inline percentage substitutions
out = out.replace('P_140_160*100', f"{rb['P(140<=T<=160)']*100:.1f}")
out = out.replace('P_161_190*100', f"{rb['P(161<=T<=190)']*100:.1f}")
out = out.replace('P_GT200*100', f"{rb['P(T>200)']*100:.0f}")
out = out.replace('P_M50*100', f"{rb['P(margin>50)']*100:.0f}")
out = out.replace('REG_R2*100', f"{reg['r2']*100:.1f}")

# sanity: no leftover placeholder tokens at all (any known key pattern)
import re
left = re.findall(r'\b[A-Z]{2,}_[A-Z0-9_]+\b', out)
left = [t for t in left if t.split('_')[0] in {'MEAN','MED','MODE','SD','CV','Q1','Q3','IQR','MAX','SKEW','N','K','P','CI','REG','CSK','MI','PHAT','PV'}]
if left:
    print("WARN unresolved-like tokens:", left)

dest = ROOT / 'report' / 'report.tex'
dest.write_text(out)
print(f"Wrote {dest} ({len(out.splitlines())} lines)")
