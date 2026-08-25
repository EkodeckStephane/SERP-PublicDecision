# SERP-PublicDecision

**SERP-PublicDecision** is the public reproducibility repository for **Systemic Evidence-based Response Prioritization (SERP)**, an auditable public-sector decision-support framework that combines implementation target gaps with strategic interdependencies to derive systemic implementation priorities.

Repository: **https://github.com/EkodeckStephane/SERP-PublicDecision**

The repository accompanies the study **“Systemic prioritization of digital-transformation gaps: Applying SERP to Cameroon's PATNuC”**. It contains transformed public evidence, de-identified expert coding, six deterministic analysis scripts, generated robustness outputs, and reproducibility metadata. Journal-specific submission files are intentionally kept outside this repository.

## 1. Context

Public-sector digital-transformation programmes are usually monitored through project components, policy pillars, targets, and performance indicators. Those administrative structures are useful for accountability, but implementation bottlenecks can cut across them. Connectivity, digital skills, governance and implementation capacity, affordability, digital trust, and productive adoption may affect several strategic objectives simultaneously.

SERP-PublicDecision addresses the resulting decision problem by combining two auditable layers:

1. **evidence** — normalized implementation target gaps derived from documented public indicators;
2. **structure** — an implementation-domain/objective incidence matrix evaluated through external expert coding.

The empirical application uses the World Bank-supported **Acceleration of the Digital Transformation of Cameroon Project (PATNuC)** as a bounded implementation case. Independent national diagnostics are used only for contextual triangulation and are not inserted into the reference target-gap vector.

## 2. Problem

Public-sector prioritization becomes difficult when implementation evidence is heterogeneous, implementation domains share strategic objectives, and decision makers need to distinguish stable priorities from conclusions that depend strongly on a particular evidence-selection rule.

The research problem is therefore to connect four requirements in one transparent workflow:

1. traceable evidence construction from public implementation indicators;
2. explicit representation of strategic interdependence;
3. systemic prioritization combining direct shortfall and structural exposure;
4. robustness analysis separating structural/model sensitivity from evidence-selection sensitivity.

SERP does **not** estimate a probability of project failure, a causal treatment effect, social welfare, or an optimal budget allocation. Its output is a **systemic implementation-priority signal conditional on the admitted evidence and encoded policy structure**.

## 3. Research question

> **Can traceable target-gap evidence and explicit strategic interdependencies be combined into an auditable public-sector prioritization rule, and which implementation priorities remain stable when the model structure and admissible evidence set are perturbed?**

The repository evaluates coupling strength, objective removal, all single-link perturbations, expert aggregation rule, within-domain aggregation, network normalization, indicator removal, alternative admissible evidence selections, transparent ranking baselines, and exact resampling of the observed three-coder panel.

## 4. Proposed solution

### 4.1 Evidence layer

`data/indicator_inventory.csv` records the PATNuC quantitative indicator inventory and the stated inclusion/exclusion criteria. `data/indicator_data.csv` contains the normalized analytical indicators; `reference_selected=1` marks the reference evidence set.

The six implementation domains are:

- `GOV` — governance and implementation capacity;
- `CONN` — connectivity and infrastructure deployment;
- `SKILL` — digital skills and capacity to use services;
- `AFFORD` — affordability;
- `TRUST` — digital trust, security, and regulatory readiness;
- `ADOPT` — productive adoption and sectoral innovation.

Definitions are stored in `data/implementation_domains.csv`.

### 4.2 Strategic interdependency layer

Let `A` denote the binary implementation-domain/objective incidence matrix in `data/domain_objective_matrix.csv`. A cell equals 1 when a domain is judged to directly affect a strategic objective.

The reference matrix is the majority-derived matrix from three external coders. The public expert-validation layer contains de-identified binary ratings, confidence scores, majority and unanimity matrices, and agreement statistics. Identifiable original records are not released.

### 4.3 Co-dependence network

SERP derives a symmetric co-dependence matrix from shared objectives:

```text
Q = A A^T
```

with the diagonal removed. The reference implementation normalizes this matrix by its spectral radius. This represents **shared strategic exposure**, not signed, directional, lagged, or causal influence.

### 4.4 Evidence-seeded propagation

For direct domain loads `b`, coupling parameter `lambda`, and normalized co-dependence matrix `W`:

```text
z = (I - lambda W)^(-1) b
```

The reference analysis uses `lambda = 0.35`; the sensitivity analysis evaluates `0.00` through `0.80` in increments of `0.01`.

The resolvent is established Katz/Bonacich-type mathematics. SERP's contribution lies in the auditable decision architecture joining documented target gaps, explicit policy structure, expert-evaluated mapping, transparent baselines, and separate structural/evidentiary robustness analyses.

## 5. Research assets and means used

The study combines public policy/project documents, quantitative decision modelling, external expert content validation, and deterministic computational sensitivity analysis.

### Public analytical data

- `data/indicator_inventory.csv` — indicator-selection audit;
- `data/indicator_data.csv` — transformed indicators and target gaps;
- `data/domain_objective_matrix.csv` — reference majority incidence matrix;
- `data/implementation_domains.csv` — six domain definitions;
- `data/strategic_objectives.csv` — seven objectives;
- `data/policy_corpus.csv` — source-corpus metadata;
- `data/external_triangulation.csv` — national diagnostics used only for interpretation.

Underlying policy/project documents are not redistributed; they remain available from the organizations cited by the associated study.

### Expert content validation

Three external experts coded all 42 domain-objective pairs. Retained agreement results include:

- 31/42 items unanimous (73.8%);
- mean pairwise agreement: 82.5%;
- Fleiss' kappa: 0.645;
- nominal Krippendorff alpha: 0.648;
- mean confidence: 4.12/5.

The available record does not establish complete blinding to implementation evidence. The exercise is therefore treated as **content validation of the mapping**, not evidence-independent validation of the numerical priority loads. See `expert_validation/README.md`.

### Software environment

The audited runtime is documented in `RUNTIME.txt`. The numerical dependencies are pinned in `requirements.txt`. The six analytical scripts are deterministic for the supplied CSV inputs and do not require network access.

## 6. Main analytical results

### 6.1 Reference prioritization

At `lambda = 0.35`:

| Rank | Domain | Direct gap | Relative systemic score |
|---:|---|---:|---:|
| 1 | SKILL | 0.9976 | 1.0000 |
| 2 | CONN | 1.0000 | 0.9633 |
| 3 | GOV | 0.8000 | 0.8991 |
| 4 | ADOPT | 0.9473 | 0.8295 |
| 5 | TRUST | 0.6667 | 0.7195 |
| 6 | AFFORD | 0.0882 | 0.2486 |

The retained output is `results/implementation_priority_scores.csv`.

### 6.2 Transparent baselines

`code/benchmark_prioritization.py` compares four ranking logics:

- evidence-only direct gaps;
- structure-only weighted degree;
- structure-only network resolvent;
- evidence-seeded SERP.

The comparison is diagnostic. It establishes that the SERP ranking is not a relabeling of direct gaps or network position; it does **not** establish predictive or welfare superiority.

### 6.3 Structural sensitivity

Under the reference evidence set and `lambda = 0.35`:

- all seven leave-one-objective-out calculations preserve `{SKILL, CONN, GOV, ADOPT}`;
- all 42 single domain-objective link flips preserve the same top-four set;
- majority and unanimity vote rules preserve the same top-four membership, although internal ordering can change;
- spectral and row-normalized co-dependence matrices preserve the same top-four membership.

### 6.4 Panel-composition sensitivity

`code/panel_bootstrap.py` enumerates all `3^3 = 27` ordered bootstrap resamples of the three observed coders. All 27 preserve the top-four set `{SKILL, CONN, GOV, ADOPT}`. This quantifies sensitivity to reweighting the observed panel only; it does not replace a larger independent or blinded validation panel.

### 6.5 Evidence-selection sensitivity

Evidence construction is materially consequential. Only five of nine leave-one-reference-indicator-out cases remain estimable because removing a singleton indicator would leave a domain without evidence. All estimable removals preserve the reference top-four set.

Several add-back scenarios change the top-four composition. The decisive case is the attained 30-day feedback-response indicator: adding it to GOV lowers the governance gap and moves GOV outside the top four. Across the tested evidence constructions, the stable intersection is therefore:

```text
SKILL - CONN - ADOPT
```

This distinguishes **structural robustness conditional on an evidence set** from **robustness to evidence construction itself**.

## 7. Scientific positioning

SERP-PublicDecision sits at the intersection of public-sector decision support, operations research and quantitative policy analysis, network-informed prioritization, multi-criteria/portfolio-oriented public decisions, and digital-transformation implementation analysis.

SERP is not proposed as a replacement for DEMATEL, ANP, VIKOR, Choquet-integral methods, or optimization-based portfolio selection. It targets evidence-constrained settings where the main requirements are direct use of documented target gaps, an inspectable structural layer, deterministic recalculation, separation of evidence and expert inputs, and explicit sensitivity to both model structure and evidence selection.

The associated article provides the full literature positioning. This repository focuses on software, transformed data, and reproducibility material rather than redistributing the manuscript.

## 8. Repository structure

```text
SERP-PublicDecision/
├── code/
│   ├── analyze_expert_validation.py
│   ├── compute_priority_model.py
│   ├── extended_robustness.py
│   ├── evidence_selection_robustness.py
│   ├── benchmark_prioritization.py
│   └── panel_bootstrap.py
├── data/
│   ├── domain_objective_matrix.csv
│   ├── implementation_domains.csv
│   ├── indicator_data.csv
│   ├── indicator_inventory.csv
│   ├── strategic_objectives.csv
│   ├── policy_corpus.csv
│   └── external_triangulation.csv
├── expert_validation/
├── results/
├── BIBLIOGRAPHIC_VERIFICATION.md
├── CITATION.cff
├── LICENSE.md
├── RELEASE_CHECKLIST.md
├── requirements.txt
├── RUNTIME.txt
└── VERSION
```

The article PDF/LaTeX source, cover letter, internal editorial audits, author photographs, and identifiable expert records are intentionally absent.

## 9. Reproducibility procedure

### 9.1 Clone

```bash
git clone https://github.com/EkodeckStephane/SERP-PublicDecision.git
cd SERP-PublicDecision
```

### 9.2 Environment

Linux/macOS:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

PowerShell:

```powershell
py -3.13 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
```

### 9.3 Run the full analytical sequence

```bash
python code/analyze_expert_validation.py
python code/compute_priority_model.py
python code/extended_robustness.py
python code/evidence_selection_robustness.py
python code/benchmark_prioritization.py
python code/panel_bootstrap.py
```

Inspect `results/` after execution. The reference model script also verifies that the analytical incidence matrix matches the expert-majority consensus matrix before calculating priorities.

## 10. Integrity, provenance, and privacy

Important integrity properties include:

- domain loads are recalculated from rows marked `reference_selected=1` rather than hard-coded;
- the reference incidence matrix must equal the expert-majority consensus matrix;
- national triangulation data are separated from the numerical target-gap vector;
- structural and evidence-selection sensitivity are reported separately;
- singleton-domain removals are marked non-estimable rather than converted to zero evidence;
- de-identified expert codes are public while identifiable original records remain excluded.

## 11. Scope and limitations

The numerical priority pattern is specific to the analysed PATNuC evidence. Several domains rely on sparse indicator sets. The mapping is a three-expert judgment construct rather than an empirically estimated causal graph. The co-dependence network is symmetric and unsigned. The design is cross-sectional. SERP prioritizes implementation pressure; it does not estimate intervention effects, welfare, or optimal resource allocation.

## 12. Citation

Citation metadata are provided in `CITATION.cff`. Until an archival DOI is minted, cite the repository URL together with the version or commit used. When a persistent release is created, update `CITATION.cff` and `RELEASE_CHECKLIST.md` with the actual identifier rather than inventing one.

## 13. License

See `LICENSE.md` for the code/data licensing scope and redistribution exclusions.

## 14. Maintainer

**Stephane Gael R. EKODECK**  
Department of Computer Science, Faculty of Science, University of Yaounde I, Cameroon  
ORCID: **0000-0002-8094-8832**

For reproducibility issues, use the repository issue tracker so corrections and clarifications remain visible and versioned.
