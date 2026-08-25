#!/usr/bin/env python3
"""Reproduce agreement statistics and majority aggregation for the expert mapping.

Input: ../expert_validation/expert_ratings_anonymized.csv
Output: agreement summary, item-level agreement and majority matrix.
"""
from pathlib import Path
import csv
import statistics
from collections import Counter, defaultdict

ROOT = Path(__file__).resolve().parents[1]
EXPERT_DIR = ROOT / 'expert_validation'
path = EXPERT_DIR / 'expert_ratings_anonymized.csv'

with path.open(newline='', encoding='utf-8') as f:
    rows = list(csv.DictReader(f))

by_coder = defaultdict(list)
for r in rows:
    by_coder[r['coder_id']].append(r)
coder_ids = sorted(by_coder, key=lambda x: int(x))
if len(coder_ids) != 3:
    raise SystemExit(f'Expected 3 coders, found {len(coder_ids)}')

experts = [by_coder[c] for c in coder_ids]
keys = [(r['risk_domain'], r['objective']) for r in experts[0]]
if any([(r['risk_domain'], r['objective']) for r in ex] != keys for ex in experts[1:]):
    raise SystemExit('Coder rows are not aligned.')

ratings = {k: [int(ex[i]['code_0_or_1']) for ex in experts] for i, k in enumerate(keys)}
confidence = {k: [int(ex[i]['confidence_1_to_5']) for ex in experts] for i, k in enumerate(keys)}
N, n = len(keys), len(experts)
counts = [[ratings[k].count(0), ratings[k].count(1)] for k in keys]
P_i = [(sum(c*c for c in cnt) - n) / (n*(n-1)) for cnt in counts]
observed_pair_agreement = sum(P_i) / N
p = [sum(cnt[j] for cnt in counts) / (N*n) for j in range(2)]
expected_agreement = sum(x*x for x in p)
fleiss_kappa = (observed_pair_agreement - expected_agreement) / (1 - expected_agreement)
unanimous = sum(len(set(ratings[k])) == 1 for k in keys)
majority = {k: int(sum(ratings[k]) >= 2) for k in keys}
unanimity_positive = {k: int(sum(ratings[k]) == 3) for k in keys}

def cohen(a, b):
    po = sum(x == y for x, y in zip(a, b)) / len(a)
    pa, pb = sum(a)/len(a), sum(b)/len(b)
    pe = pa*pb + (1-pa)*(1-pb)
    return po, (po-pe)/(1-pe)

pair_stats = {}
for i, j in [(0,1), (0,2), (1,2)]:
    a = [int(r['code_0_or_1']) for r in experts[i]]
    b = [int(r['code_0_or_1']) for r in experts[j]]
    pair_stats[(i+1,j+1)] = cohen(a,b)

# Nominal Krippendorff alpha for complete binary ratings, reported as a sensitivity statistic.
pair_total = 0
pair_disagree = 0
for k in keys:
    row = ratings[k]
    for i in range(n):
        for j in range(i+1,n):
            pair_total += 1
            pair_disagree += int(row[i] != row[j])
Do = pair_disagree / pair_total
pooled = [v for k in keys for v in ratings[k]]
ct = Counter(pooled)
Nt = len(pooled)
De = 1 - sum(c*(c-1) for c in ct.values()) / (Nt*(Nt-1))
krippendorff_alpha_nominal = 1 - Do/De

initial_path = EXPERT_DIR / 'initial_analytical_matrix.csv'
initial = None
if initial_path.exists():
    with initial_path.open(newline='', encoding='utf-8') as f:
        initial_rows = list(csv.DictReader(f))
    initial = {(r['risk'], o): int(r[o]) for r in initial_rows for o in r if o != 'risk'}

with (EXPERT_DIR/'expert_validation_summary.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['metric','value'])
    w.writerow(['items',N]); w.writerow(['raters',n])
    w.writerow(['unanimous_items',unanimous]); w.writerow(['unanimous_item_fraction',f'{unanimous/N:.9f}'])
    w.writerow(['observed_pair_agreement',f'{observed_pair_agreement:.9f}'])
    w.writerow(['fleiss_kappa',f'{fleiss_kappa:.9f}'])
    w.writerow(['krippendorff_alpha_nominal',f'{krippendorff_alpha_nominal:.9f}'])
    w.writerow(['mean_confidence_all',f'{statistics.mean([c for k in keys for c in confidence[k]]):.9f}'])
    w.writerow(['mean_confidence_unanimous',f'{statistics.mean([c for k in keys if len(set(ratings[k]))==1 for c in confidence[k]]):.9f}'])
    w.writerow(['mean_confidence_disagreement',f'{statistics.mean([c for k in keys if len(set(ratings[k]))>1 for c in confidence[k]]):.9f}'])
    for (i,j),(po,kappa) in pair_stats.items():
        w.writerow([f'pair_{i}_{j}_agreement',f'{po:.9f}'])
        w.writerow([f'pair_{i}_{j}_cohen_kappa',f'{kappa:.9f}'])
    if initial is not None:
        init_vec=[initial[k] for k in keys]; maj_vec=[majority[k] for k in keys]
        po,kappa=cohen(init_vec,maj_vec)
        w.writerow(['initial_vs_majority_agreement',f'{po:.9f}'])
        w.writerow(['initial_vs_majority_cohen_kappa',f'{kappa:.9f}'])
        w.writerow(['initial_vs_majority_cells_changed',sum(initial[k]!=majority[k] for k in keys)])

with (EXPERT_DIR/'item_agreement.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.writer(f)
    w.writerow(['risk_domain','objective','expert_1','expert_2','expert_3','majority_code','unanimous','mean_confidence'])
    for k in keys:
        vals=ratings[k]
        w.writerow([k[0],k[1],*vals,majority[k],int(len(set(vals))==1),f'{statistics.mean(confidence[k]):.3f}'])

domains=[]; objectives=[]
for k in keys:
    if k[0] not in domains: domains.append(k[0])
    if k[1] not in objectives: objectives.append(k[1])
with (EXPERT_DIR/'consensus_majority_matrix.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['risk']+objectives)
    for d in domains: w.writerow([d]+[majority[(d,o)] for o in objectives])
with (EXPERT_DIR/'consensus_unanimity_matrix.csv').open('w', newline='', encoding='utf-8') as f:
    w=csv.writer(f); w.writerow(['risk']+objectives)
    for d in domains: w.writerow([d]+[unanimity_positive[(d,o)] for o in objectives])

report=[
    f'Items: {N}; raters: {n}',
    f'All-three unanimity: {unanimous}/{N} ({100*unanimous/N:.1f}%)',
    f'Observed pairwise agreement: {100*observed_pair_agreement:.1f}%',
    f"Fleiss' kappa: {fleiss_kappa:.3f}",
    f'Nominal Krippendorff alpha: {krippendorff_alpha_nominal:.3f}',
    f'Mean confidence: {statistics.mean([c for k in keys for c in confidence[k]]):.2f}/5',
    f'Mean confidence, unanimous items: {statistics.mean([c for k in keys if len(set(ratings[k]))==1 for c in confidence[k]]):.2f}/5',
    f'Mean confidence, disagreement items: {statistics.mean([c for k in keys if len(set(ratings[k]))>1 for c in confidence[k]]):.2f}/5',
    'Pairwise agreement/Cohen kappa: ' + '; '.join(
        f'Expert {i}-{j}: {100*po:.1f}%, kappa={kap:.3f}'
        for (i,j),(po,kap) in pair_stats.items()
    ),
]
if initial is not None:
    init_vec=[initial[k] for k in keys]; maj_vec=[majority[k] for k in keys]
    po,kappa=cohen(init_vec,maj_vec)
    changed=[f'{k[0]}-{k[1]}' for k in keys if initial[k]!=majority[k]]
    report += [
        f'Initial analytical matrix vs expert-majority matrix: {100*po:.1f}% agreement; Cohen kappa={kappa:.3f}',
        f'Changed cells ({len(changed)}): ' + ', '.join(changed)
    ]
(EXPERT_DIR/'expert_validation_report.txt').write_text('\n'.join(report)+'\n',encoding='utf-8')
print('\n'.join(report))
