#!/usr/bin/env python3
"""Exact three-coder bootstrap sensitivity for the expert mapping."""
from pathlib import Path
from itertools import product
from collections import Counter
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
RATINGS = pd.read_csv(ROOT / "expert_validation" / "expert_ratings_anonymized.csv")
INC = pd.read_csv(ROOT / "data" / "domain_objective_matrix.csv").set_index("domain")
IND = pd.read_csv(ROOT / "data" / "indicator_data.csv")
CODES = list(INC.index)
OBJECTIVES = list(INC.columns)
CODERS = sorted(RATINGS["coder_id"].unique().tolist())
REFERENCE = IND[IND["reference_selected"].astype(int) == 1].copy()
B = np.array([float(REFERENCE.loc[REFERENCE.domain == c, "gap"].mean()) for c in CODES])
LAMBDA = 0.35

def coder_matrix(coder):
    d = RATINGS[RATINGS.coder_id == coder].pivot(index="domain", columns="objective", values="code_0_or_1")
    return d.reindex(index=CODES, columns=OBJECTIVES).to_numpy(dtype=int)

def calculate(matrix):
    q = matrix @ matrix.T
    np.fill_diagonal(q, 0)
    if np.any(q):
        rho = float(np.max(np.linalg.eigvals(q).real)); w = q / rho if rho > 0 else q.astype(float)
    else: w = q.astype(float)
    z = np.linalg.solve(np.eye(len(CODES)) - LAMBDA * w, B)
    rel = z / z.max()
    rk = pd.Series(rel, index=CODES).rank(method="min", ascending=False).astype(int)
    return rel, rk

MATS = {coder: coder_matrix(coder) for coder in CODERS}
rows=[]; top_sets=Counter(); unique_matrices=Counter()
for sample in product(CODERS, repeat=3):
    stack=np.stack([MATS[c] for c in sample], axis=0)
    matrix=(stack.sum(axis=0) >= 2).astype(int)
    unique_matrices[tuple(matrix.ravel().tolist())] += 1
    rel,rk=calculate(matrix)
    top4=tuple(sorted([c for c in CODES if int(rk.loc[c]) <= 4])); top_sets[top4] += 1
    sample_id="-".join(map(str,sample))
    for i,c in enumerate(CODES):
        rows.append({"bootstrap_sample":sample_id,"domain":c,"relative_score":float(rel[i]),"rank":int(rk.loc[c]),"top4":int(rk.loc[c] <= 4)})
samples=pd.DataFrame(rows); samples.to_csv(ROOT / "results" / "panel_bootstrap_samples.csv", index=False)
summary=(samples.groupby("domain",sort=False).agg(top4_frequency=("top4","mean"),mean_rank=("rank","mean"),min_rank=("rank","min"),max_rank=("rank","max"),mean_relative_score=("relative_score","mean"),sd_relative_score=("relative_score",lambda x: float(np.std(x,ddof=0)))).reset_index())
summary.to_csv(ROOT / "results" / "panel_bootstrap_summary.csv", index=False)
sets=pd.DataFrame([{"top4_set":", ".join(k),"count":v,"frequency":v/(len(CODERS)**3)} for k,v in sorted(top_sets.items(), key=lambda kv:(-kv[1],kv[0]))])
sets.to_csv(ROOT / "results" / "panel_bootstrap_top4_sets.csv", index=False)
with open(ROOT / "results" / "panel_bootstrap_summary.txt", "w", encoding="utf-8") as f:
    f.write("Exact bootstrap sensitivity to observed three-coder panel composition\n")
    f.write("=================================================================\n")
    f.write(f"Ordered resamples enumerated: {len(CODERS)**3}\n")
    f.write(f"Unique majority matrices generated: {len(unique_matrices)}\n")
    f.write(f"Reference coupling lambda={LAMBDA:.2f}\n\n")
    f.write(summary.to_string(index=False)); f.write("\n\nTop-four set frequencies\n"); f.write(sets.to_string(index=False))
    f.write("\n\nCaveat: this bootstrap only measures sensitivity to reweighting the three\nobserved coders. It does not establish external validity and does not replace\na larger, independent, preferably blinded expert validation.\n")
print(summary.to_string(index=False)); print("\nTop-four sets:\n", sets.to_string(index=False))