# Replication package

This directory contains the transformed public evidence, the de-identified expert coding layer, and the scripts used to reproduce the SERP analyses reported in the manuscript. The reference calculation is conditional on the audited reference evidence rule; evidence-selection sensitivity is reported separately.

## Core data
- `data/indicator_inventory.csv`: complete audit of the 24 quantitative PDO, intermediate, CRI, and nested subgroup rows in the revised PATNuC results framework, including include/exclude decisions and explicit criteria.
- `data/indicator_data.csv`: normalized implementation indicators and target gaps used by the scripts; `reference_selected=1` identifies the reference evidence set.
- `data/risk_objective_matrix.csv`: expert-majority binary risk-objective incidence matrix used in the reference analysis.
- `data/strategic_objectives.csv`: definitions of the seven policy objectives.
- `data/risk_domains.csv`: definitions of the six risk domains.
- `data/external_triangulation.csv`: independent national diagnostics used for interpretation only and never inserted into the target-gap vector.

## Expert validation
See `expert_validation/README.md`. The public replication layer contains de-identified coder values, majority and unanimity matrices, and agreement outputs. The elicitation was not blind to implementation values, so it is treated as content validation of the policy mapping rather than as evidence-independent validation of numerical risk loads. Author-retained translated rationale sheets remain outside the submission payload.

## Results
- `results/risk_scores.csv`: reference results at interdependence coupling $\lambda=0.35$.
- `results/sensitivity.csv`: 81-point coupling-sensitivity grid for $\lambda\in[0,0.8]$.
- `results/objective_ablation.csv`: leave-one-objective-out results.
- `results/mapping_single_link_perturbation.csv`: exhaustive 42 single-link perturbations.
- `results/expert_vote_rule_robustness.csv`: majority-versus-unanimity expert vote-rule sensitivity.
- `results/aggregation_robustness.csv`: limited within-domain aggregation diagnostic.
- `results/network_normalization_robustness.csv`: spectral-versus-row network normalization.
- `results/indicator_leave_one_out.csv`: leave-one-indicator-out evidence sensitivity where every domain remains represented.
- `results/evidence_selection_scenarios.csv`: add-back scenarios for excluded normalizable indicators.
- `results/evidence_selection_summary.txt`: concise evidence-selection audit.

## Code
- `code/analyze_expert_validation.py`: agreement statistics and majority/unanimity matrix reconstruction.
- `code/compute_risk_model.py`: reference SERP recalculation, coupling sensitivity, and objective ablation.
- `code/extended_robustness.py`: single-link, limited aggregation, and normalization checks.
- `code/evidence_selection_robustness.py`: leave-one-indicator-out, excluded-indicator add-back, and vote-rule tests.

## Reproducibility metadata
- `requirements.txt`: pinned Python dependencies used for the audited rerun.
- `RUNTIME.txt`: tested interpreter/toolchain versions.
- `VERSION`: package version.
- `LICENSE.md`: licensing scope and exclusions.
- `CITATION.cff`: citation metadata for the replication package.
- `RELEASE_CHECKLIST.md`: fields to be completed when the authors deposit the package in a persistent repository and obtain a DOI or other permanent identifier.

The underlying policy and project documents are not redistributed. Their public sources are cited in the article bibliography.
