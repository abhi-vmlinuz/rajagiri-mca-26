#!/usr/bin/env python3
"""Build slides.tex from slides.template.tex by injecting results.json values."""
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
R = json.loads((ROOT / 'results.json').read_text())

tm, mm = R['descriptive']['target_runs'], R['descriptive']['result_margin']
b = R['binomial']
reg = R['regression']

S = {
    'MEAN_TM': f"{tm['mean']:.0f}", 'MED_TM': f"{tm['median']:.0f}", 'MODE_TM': f"{tm['mode']:.0f}",
    'SD_TM': f"{tm['std']:.1f}", 'CV_TM': f"{tm['cv']:.2f}",
    'MEAN_MM': f"{mm['mean']:.0f}", 'MED_MM': f"{mm['median']:.0f}",
    'SD_MM': f"{mm['std']:.1f}", 'CV_MM': f"{mm['cv']:.2f}",
    'SKEW_MM': f"{mm['skew']:.1f}", 'MAX_MM': f"{mm['max']:.0f}",
    'IQR_TM': f"{tm['iqr']:.0f}", 'IQR_MM': f"{mm['iqr']:.0f}",
    'K_BAT': b['bat_first_win']['k'], 'N_BAT': b['bat_first_win']['n'],
    'PV_BAT': f"{b['bat_first_win']['p_value']:.3f}",
    'K_FIELD': b['field_first_win']['k'], 'N_FIELD': b['field_first_win']['n'],
    'PV_FIELD': f"{b['field_first_win']['p_value']:.3f}",
    'REG_INT': f"{reg['intercept']:.1f}", 'REG_SLP': f"{reg['slope']:.2f}",
    'REG_R2': f"{reg['r2']:.3f}", 'REG_PV': f"{reg['p_value']:.3f}",
}

tpl = (ROOT / 'report' / 'slides.template.tex').read_text()
out = tpl
# Tokens may appear either as PLAIN_UNDERSCORE or as LaTeX-escaped
# BACKSLASH\_UNDERSCORE (both are valid ways to write a placeholder in the
# template). Substitute longest-first so prefix collisions are safe.
def variants(key):
    yield key
    yield key.replace('_', '\\_')      # LaTeX-escaped form, e.g. MEAN\_TM

for key in sorted(S, key=len, reverse=True):
    for v in variants(key):
        out = out.replace(v, str(S[key]))

left = re.findall(r'\b[A-Z]{2,}_[A-Z0-9_]+\b', out)
known = set(S)
left = [t for t in left if t in known]
if left:
    raise SystemExit(f"Unresolved placeholders remain: {left}")

dest = ROOT / 'report' / 'slides.tex'
dest.write_text(out)
print(f"Wrote {dest} ({len(out.splitlines())} lines)")
