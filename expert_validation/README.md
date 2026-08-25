# External expert validation of the risk-objective matrix

Three external experts returned separate coding sheets covering all 42 risk-domain/objective pairs. Each pair contains a binary 0/1 direct-link judgment, a 1-5 confidence score, a short rationale, and a source-location field in the returned records. The original responses were in French; the English rationale translations were supplied by the authors. The binary codes used in the quantitative analysis are unchanged by translation.

## Protocol audit and independence caveat

The returned sheets document the judgments and the sources used to justify them. Several rationales explicitly refer to PATNuC implementation values and national diagnostics. The available audit trail therefore does **not** support a claim that the coders were blinded to gap magnitudes. The expert exercise is treated as **content validation of the risk-objective mapping**, not as evidence-independent validation of the numerical risk loads. A future blind re-coding round withholding gap values would provide a stronger independence check.

The files retained for this revision do not justify reconstructing undocumented instructions or claiming that specific source materials were withheld from or supplied to the experts beyond what is evidenced by the returned sheets. This limitation is stated explicitly in the manuscript.

## Public/de-identified files
- `expert_ratings_anonymized.csv`: coder ID, risk domain, objective, binary code, and confidence only.
- `expert_validation_summary.csv`: panel-level agreement and confidence statistics.
- `item_agreement.csv`: item-level coder values, majority code, unanimity flag, and mean confidence.
- `consensus_majority_matrix.csv`: deterministic majority-derived matrix used by the reference SERP analysis.
- `consensus_unanimity_matrix.csv`: unanimity-only matrix used for vote-rule sensitivity.
- `initial_analytical_matrix.csv`: initial documentary coding retained only for audit comparison.
- `expert_validation_report.txt`: human-readable validation summary.

The majority rule retains a link when at least two of the three coders select 1. The unanimity rule retains a link only when all three select 1. These are aggregation rules, not deliberative consensus rounds.

## Agreement results
- 31/42 unanimous items (73.8%).
- Expert 1 vs Expert 2: 85.7% observed agreement; Cohen's kappa = 0.720.
- Expert 1 vs Expert 3: 88.1% observed agreement; Cohen's kappa = 0.748.
- Expert 2 vs Expert 3: 73.8% observed agreement; Cohen's kappa = 0.503.
- Mean pairwise observed agreement: 82.5%.
- Fleiss' kappa = 0.645.
- Nominal Krippendorff alpha = 0.648 (reported as a sensitivity statistic).
- Mean confidence = 4.12/5.
- Initial analytical matrix vs expert-majority matrix: 92.9% cell agreement; three cells changed (CONN-O3, SKILL-O4, AFFORD-O5).
- Majority and unanimity rules preserve the same reference-evidence top-four membership, although their internal ordering differs.

## Reproducibility
Run:

```bash
python ../code/analyze_expert_validation.py
```

The translated rationale sheets are retained in `private_not_for_submission/` and are not part of a public release unless the authors confirm that sharing them is permitted.
