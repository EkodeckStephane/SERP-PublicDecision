#!/usr/bin/env python3
"""Reproduce SERP structural/model robustness checks."""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT=Path(__file__).resolve().parents[1]
ind=pd.read_csv(ROOT/'data'/'indicator_data.csv')
ind=ind[ind['reference_selected'].astype(int)==1].copy()
inc=pd.read_csv(ROOT/'data'/'domain_objective_matrix.csv').set_index('domain')
codes=list(inc.index); objectives=list(inc.columns); A=inc.to_numpy(dtype=float)
base_values={c:float(ind.loc[ind.domain==c,'gap'].mean()) for c in codes}
if any(np.isnan(v) for v in base_values.values()): raise SystemExit('A reference domain has no selected indicator.')
b=np.array([base_values[c] for c in codes],dtype=float)

def calculate(matrix,loads,coupling=0.35,normalization='spectral'):
    q=matrix@matrix.T; np.fill_diagonal(q,0.0)
    if normalization=='spectral':
        rho=max(np.linalg.eigvals(q).real) if np.any(q) else 1.0; w=q/rho if rho>0 else q
    elif normalization=='row':
        rowsums=q.sum(axis=1,keepdims=True); w=np.divide(q,rowsums,out=np.zeros_like(q),where=rowsums!=0)
    else: raise ValueError(normalization)
    z=np.linalg.solve(np.eye(len(loads))-coupling*w,loads); relative=z/z.max(); ranks=pd.Series(relative,index=codes).rank(method='min',ascending=False).astype(int)
    return relative,ranks

_,reference_ranks=calculate(A,b); reference_top4={c for c in codes if reference_ranks[c]<=4}
rows=[]
for i,domain in enumerate(codes):
    for j,objective in enumerate(objectives):
        perturbed=A.copy(); perturbed[i,j]=1-perturbed[i,j]; _,ranks=calculate(perturbed,b); top4={c for c in codes if ranks[c]<=4}
        row={'domain_flipped':domain,'objective_flipped':objective,'new_value':int(perturbed[i,j]),'top4_same':int(top4==reference_top4)}; row.update({f'rank_{c}':int(ranks[c]) for c in codes}); rows.append(row)
pd.DataFrame(rows).to_csv(ROOT/'results'/'mapping_single_link_perturbation.csv',index=False)

groups={c:ind.loc[ind.domain==c,'gap'].to_numpy(dtype=float) for c in codes}; rows=[]
for aggregation in ['mean','median','max','min']:
    values={c:float(getattr(np,aggregation)(arr)) for c,arr in groups.items()}; loads=np.array([values[c] for c in codes],dtype=float); _,ranks=calculate(A,loads); top4={c for c in codes if ranks[c]<=4}
    row={'aggregation':aggregation,'top4_same':int(top4==reference_top4)}; row.update({f'n_indicators_{c}':int(len(groups[c])) for c in codes}); row.update({f'base_{c}':values[c] for c in codes}); row.update({f'rank_{c}':int(ranks[c]) for c in codes}); rows.append(row)
pd.DataFrame(rows).to_csv(ROOT/'results'/'aggregation_robustness.csv',index=False)

rows=[]
for normalization in ['spectral','row']:
    scores,ranks=calculate(A,b,normalization=normalization); top4={c for c in codes if ranks[c]<=4}
    row={'normalization':normalization,'top4_same':int(top4==reference_top4)}; row.update({f'score_{c}':float(scores[i]) for i,c in enumerate(codes)}); row.update({f'rank_{c}':int(ranks[c]) for c in codes}); rows.append(row)
pd.DataFrame(rows).to_csv(ROOT/'results'/'network_normalization_robustness.csv',index=False)
print('reference_top4',sorted(reference_top4)); print('single_link_same',int(pd.read_csv(ROOT/'results'/'mapping_single_link_perturbation.csv')['top4_same'].sum()),'/ 42'); print('reference_domain_counts',{c:len(groups[c]) for c in codes})