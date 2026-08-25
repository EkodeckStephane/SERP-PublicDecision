#!/usr/bin/env python3
"""Recalculate SERP reference scores, coupling sensitivity, and objective ablations.

All inputs are local CSV files shipped with the replication package. The reference
implementation-domain/objective matrix is the three-expert majority matrix. Domain loads are derived
from rows explicitly marked reference_selected=1 in indicator_data.csv; no domain
load is hard-coded.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ind = pd.read_csv(ROOT / 'data' / 'indicator_data.csv')
inc = pd.read_csv(ROOT / 'data' / 'domain_objective_matrix.csv').set_index('domain')
consensus = pd.read_csv(ROOT / 'expert_validation' / 'consensus_majority_matrix.csv').set_index('domain')
if not inc.equals(consensus):
    raise SystemExit('Reference matrix does not match the expert-majority matrix.')

codes = list(inc.index)
objectives = list(inc.columns)
reference = ind[ind['reference_selected'].astype(int) == 1].copy()
missing = [c for c in codes if reference.loc[reference.domain == c, 'gap'].empty]
if missing:
    raise SystemExit(f'Reference indicator set leaves domains without evidence: {missing}')

vals = {c: float(reference.loc[reference.domain == c, 'gap'].mean()) for c in codes}
b = np.array([vals[c] for c in codes], dtype=float)
A = inc.to_numpy(dtype=float)


def calculate(matrix, loads, coupling=0.35):
    Q = matrix @ matrix.T
    np.fill_diagonal(Q, 0)
    rho = max(np.linalg.eigvals(Q).real) if np.any(Q) else 1.0
    W = Q / rho if rho > 0 else Q
    z = np.linalg.solve(np.eye(len(codes)) - coupling * W, loads)
    rel = z / z.max()
    ranks = pd.Series(rel, index=codes).rank(method='min', ascending=False).astype(int)
    return rel, ranks

r, ranks = calculate(A, b, 0.35)
out = pd.DataFrame({'domain': codes, 'base_gap': b, 'systemic_relative_score': r})
out['rank'] = [int(ranks[c]) for c in codes]
out.to_csv(ROOT / 'results' / 'implementation_priority_scores.csv', index=False)

rows = []
for coupling in np.round(np.arange(0, 0.8001, 0.01), 2):
    rel, rk = calculate(A, b, float(coupling))
    for i, c in enumerate(codes):
        rows.append({'lambda': float(coupling), 'domain': c, 'relative_score': float(rel[i]), 'rank': int(rk[c])})
sens = pd.DataFrame(rows)
sens.to_csv(ROOT / 'results' / 'sensitivity.csv', index=False)
summary = []
for c in codes:
    d = sens[sens.domain == c]
    summary.append({'domain': c, 'min_rank': int(d['rank'].min()), 'max_rank': int(d['rank'].max()), 'top4_persistence': float((d['rank'] <= 4).mean())})
pd.DataFrame(summary).to_csv(ROOT / 'results' / 'sensitivity_summary.csv', index=False)
for c in codes:
    sens[sens.domain == c][['lambda', 'relative_score', 'rank']].to_csv(ROOT / 'results' / f'sensitivity_{c}.csv', index=False)

rows = []
for j, obj in enumerate(objectives):
    rel, rk = calculate(np.delete(A, j, axis=1), b, 0.35)
    for i, c in enumerate(codes):
        rows.append({'objective_removed': obj, 'domain': c, 'relative_score': float(rel[i]), 'rank': int(rk[c])})
abl = pd.DataFrame(rows)
abl.to_csv(ROOT / 'results' / 'objective_ablation.csv', index=False)
summary = []
for c in codes:
    d = abl[abl.domain == c]
    summary.append({'domain': c, 'min_rank': int(d['rank'].min()), 'max_rank': int(d['rank'].max()), 'top4_all_ablations': int((d['rank'] <= 4).all())})
pd.DataFrame(summary).to_csv(ROOT / 'results' / 'objective_ablation_summary.csv', index=False)

print(out.sort_values('rank').to_string(index=False))