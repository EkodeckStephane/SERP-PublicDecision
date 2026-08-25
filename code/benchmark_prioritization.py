#!/usr/bin/env python3
"""Benchmark SERP against transparent evidence-only and structure-only rankings."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
IND = pd.read_csv(ROOT / "data" / "indicator_data.csv")
INC = pd.read_csv(ROOT / "data" / "domain_objective_matrix.csv").set_index("domain")
CODES = list(INC.index)
REFERENCE = IND[IND["reference_selected"].astype(int) == 1].copy()
B = np.array([float(REFERENCE.loc[REFERENCE.domain == c, "gap"].mean()) for c in CODES])
A = INC.to_numpy(dtype=float)
LAMBDA = 0.35

def spectral_network(matrix):
    q = matrix @ matrix.T
    np.fill_diagonal(q, 0)
    if not np.any(q): return q
    rho = float(np.max(np.linalg.eigvals(q).real))
    return q / rho if rho > 0 else q

def normalize(x):
    m = float(np.max(x)); return x / m if m > 0 else x

def ranks(x):
    return pd.Series(x).rank(method="min", ascending=False).astype(int).to_numpy()

W = spectral_network(A)
direct = normalize(B)
weighted_degree = normalize(W.sum(axis=1))
network_only = normalize(np.linalg.solve(np.eye(len(CODES)) - LAMBDA * W, np.ones(len(CODES))))
serp = normalize(np.linalg.solve(np.eye(len(CODES)) - LAMBDA * W, B))

out = pd.DataFrame({
    "domain": CODES,
    "direct_gap_score": direct, "direct_gap_rank": ranks(direct),
    "weighted_degree_score": weighted_degree, "weighted_degree_rank": ranks(weighted_degree),
    "network_only_resolvent_score": network_only, "network_only_resolvent_rank": ranks(network_only),
    "serp_score": serp, "serp_rank": ranks(serp),
})
out.to_csv(ROOT / "results" / "method_benchmark.csv", index=False)
rank_cols = ["direct_gap_rank", "weighted_degree_rank", "network_only_resolvent_rank", "serp_rank"]
corr = out[rank_cols].corr(method="spearman")
corr.to_csv(ROOT / "results" / "method_benchmark_rank_correlations.csv")
with open(ROOT / "results" / "method_benchmark_summary.txt", "w", encoding="utf-8") as f:
    f.write("Transparent benchmark of prioritization logics\n")
    f.write("=============================================\n")
    f.write(f"Reference coupling lambda={LAMBDA:.2f}\n\n")
    f.write(out.sort_values("serp_rank").to_string(index=False))
    f.write("\n\nSpearman correlations among rank vectors\n")
    f.write(corr.to_string())
    f.write("\n\nInterpretation: direct-gap ranking is evidence-only; weighted degree and the\n")
    f.write("network-only resolvent are structure-only diagnostics; SERP is evidence-seeded\n")
    f.write("resolvent propagation. The comparison is descriptive and does not establish\n")
    f.write("predictive or welfare superiority of SERP.\n")
print(out.sort_values("serp_rank").to_string(index=False))