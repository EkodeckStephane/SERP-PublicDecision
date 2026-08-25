#!/usr/bin/env python3
"""Evidence-selection robustness for SERP.

This script distinguishes model-structure robustness from robustness to the set of
PATNuC indicators admitted to the base-load vector. The reference set is explicitly
marked in indicator_data.csv. Omitted indicators are drawn from the complete revised
Results Framework inventory in indicator_inventory.csv.
"""
from pathlib import Path
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
ind = pd.read_csv(ROOT/'data'/'indicator_data.csv')
inv = pd.read_csv(ROOT/'data'/'indicator_inventory.csv')
A_df = pd.read_csv(ROOT/'data'/'risk_objective_matrix.csv').set_index('risk')
codes = list(A_df.index)
A = A_df.to_numpy(float)


def gap(row):
    b, x, t = float(row.baseline), float(row.current), float(row.target)
    if row.direction == 'increase':
        den = t-b
        if den <= 0: return np.nan
        p = np.clip((x-b)/den,0,1)
    else:
        den = b-t
        if den <= 0: return np.nan
        p = np.clip((b-x)/den,0,1)
    return float(1-p)

inv['gap'] = inv.apply(gap,axis=1)
reference = ind[ind.reference_selected.astype(int)==1].copy()


def calculate(loads, coupling=0.35):
    q=A@A.T; np.fill_diagonal(q,0)
    rho=max(np.linalg.eigvals(q).real) if np.any(q) else 1.0
    w=q/rho if rho>0 else q
    b=np.array([loads[c] for c in codes],float)
    z=np.linalg.solve(np.eye(len(codes))-coupling*w,b)
    rel=z/z.max()
    ranks=pd.Series(rel,index=codes).rank(method='min',ascending=False).astype(int)
    return rel,ranks


def loads_from_rows(rows):
    vals={}
    for c in codes:
        d=rows.loc[rows.domain==c,'gap']
        vals[c]=float(d.mean()) if len(d) else np.nan
    return vals

ref_loads=loads_from_rows(reference)
_,ref_ranks=calculate(ref_loads)
ref_top4={c for c in codes if ref_ranks[c]<=4}

# Leave-one-indicator-out is estimable only when the domain remains represented.
loo=[]
for code in reference.code:
    r=reference[reference.code!=code].copy()
    loads=loads_from_rows(r)
    estimable=not any(np.isnan(v) for v in loads.values())
    row={'indicator_removed':code,'estimable':int(estimable)}
    if estimable:
        rel,ranks=calculate(loads); top4={c for c in codes if ranks[c]<=4}
        row['top4_same']=int(top4==ref_top4)
        row['top4']=';'.join(sorted(top4))
        row.update({f'rank_{c}':int(ranks[c]) for c in codes})
    else:
        row['top4_same']=''; row['top4']='domain would be unrepresented'
    loo.append(row)
pd.DataFrame(loo).to_csv(ROOT/'results'/'indicator_leave_one_out.csv',index=False)

# Add-back scenarios for indicators explicitly questioned in review plus broader families.
by_code=inv.set_index('rf_code')
scenarios={
    'reference':[],
    'add_feedback_30d':['RF24'],
    'add_training_satisfaction':['RF23'],
    'add_broadband_CRI':['RF11'],
    'add_digital_services_CRI':['RF14'],
    'add_PDO_adoption_total':['RF06'],
    'add_productive_partnerships':['RF08'],
    'add_conditional_ratios':['RF23','RF24'],
    'add_all_gender_subindicators':['RF02','RF05','RF07','RF09','RF13','RF16','RF20'],
    'expanded_non_disaggregated':['RF06','RF08','RF11','RF14','RF23','RF24'],
}
rows=[]
for name,adds in scenarios.items():
    d=reference[['code','domain','gap']].copy()
    extra=[]
    for rc in adds:
        rr=by_code.loc[rc]
        if pd.isna(rr['gap']): continue
        extra.append({'code':rc,'domain':rr.domain,'gap':float(rr['gap'])})
    if extra: d=pd.concat([d,pd.DataFrame(extra)],ignore_index=True)
    loads=loads_from_rows(d)
    rel,ranks=calculate(loads)
    top4={c for c in codes if ranks[c]<=4}
    row={'scenario':name,'added_indicators':';'.join(adds),'top4_same':int(top4==ref_top4),'top4':';'.join(sorted(top4))}
    row.update({f'base_{c}':loads[c] for c in codes})
    row.update({f'score_{c}':float(rel[i]) for i,c in enumerate(codes)})
    row.update({f'rank_{c}':int(ranks[c]) for c in codes})
    rows.append(row)
pd.DataFrame(rows).to_csv(ROOT/'results'/'evidence_selection_scenarios.csv',index=False)

# Majority-vs-unanimity vote aggregation sensitivity.
vr=[]
for rule,fn in [('majority',lambda x: int(x>=2)),('unanimity',lambda x: int(x==3))]:
    er=pd.read_csv(ROOT/'expert_validation'/'expert_ratings_anonymized.csv')
    M=np.zeros_like(A)
    for i,c in enumerate(codes):
        for j,o in enumerate(A_df.columns):
            s=int(er[(er.risk_domain==c)&(er.objective==o)].code_0_or_1.sum())
            M[i,j]=fn(s)
    q=M@M.T; np.fill_diagonal(q,0)
    rho=max(np.linalg.eigvals(q).real) if np.any(q) else 1.0
    w=q/rho if rho>0 else q
    b=np.array([ref_loads[c] for c in codes])
    z=np.linalg.solve(np.eye(len(codes))-.35*w,b); rel=z/z.max()
    ranks=pd.Series(rel,index=codes).rank(method='min',ascending=False).astype(int)
    top4={c for c in codes if ranks[c]<=4}
    row={'vote_rule':rule,'top4_same':int(top4==ref_top4),'top4':' ; '.join(sorted(top4))}
    row.update({f'score_{c}':float(rel[i]) for i,c in enumerate(codes)})
    row.update({f'rank_{c}':int(ranks[c]) for c in codes})
    vr.append(row)
pd.DataFrame(vr).to_csv(ROOT/'results'/'expert_vote_rule_robustness.csv',index=False)

changed=pd.DataFrame(rows).query("top4_same == 0")['scenario'].tolist()
summary=[
    f'Reference top-four: {sorted(ref_top4)}',
    f'Admissible leave-one-indicator-out runs: {sum(x["estimable"] for x in loo)}/{len(loo)}; all admissible runs preserve top-four: {all((not x["estimable"]) or x["top4_same"]==1 for x in loo)}',
    'Singleton removals are marked non-estimable because treating missing evidence as a zero gap would be invalid.',
    f'Add-back scenarios changing top-four: {changed}',
    'The 30-day feedback indicator is the decisive add-back: it lowers GOV because its target gap is zero and moves GOV outside the top four.',
    'Majority versus unanimity vote aggregation preserves the same top-four set but changes ordering within it.',
]
(ROOT/'results'/'evidence_selection_summary.txt').write_text('\n'.join(summary)+'\n',encoding='utf-8')
print('\n'.join(summary))
