# External expert content validation of the implementation-domain/objective matrix

Three external experts coded all 42 implementation-domain/objective pairs. The quantitative records contain a binary direct-link judgment and a 1-5 confidence score for every pair. The source analysis uses only the de-identified binary codes and confidence values supplied in this directory.

## Independence boundary

The experts were not blinded to the implementation evidence. The exercise is therefore interpreted as **content validation of the implementation-domain/objective mapping**, not as evidence-independent validation of the numerical target-gap loads. The associated manuscript reports this limitation explicitly and treats a larger, independent, preferably blinded panel as a future validation step.

## Public/de-identified files

- `expert_ratings_anonymized.csv`: coder ID, implementation domain, objective, binary code, and confidence.
- `expert_validation_summary.csv`: panel-level agreement and confidence statistics.
- `item_agreement.csv`: item-level coder values, majority code, unanimity flag, and mean confidence.
- `consensus_majority_matrix.csv`: deterministic majority-derived matrix used by the reference SERP analysis.
- `consensus_unanimity_matrix.csv`: unanimity-only matrix used for vote-rule sensitivity.
- `initial_analytical_matrix.csv`: initial documentary coding retained for audit comparison.
- `expert_validation_report.txt`: human-readable validation summary.
- `expert_coding_sheet.csv`: coding-template structure retained with the package.

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

From the repository root, run:

```bash
python code/analyze_expert_validation.py
```

The public repository excludes original records that may identify individual experts. The released de-identified coding layer is sufficient to reproduce the quantitative agreement and consensus calculations used by SERP.
