# SERP-PublicDecision

**SERP-PublicDecision** is the public reproducibility repository for **Systemic Evidence-based Response Prioritization (SERP)**, an auditable public-sector decision-support framework that combines implementation target gaps with strategic interdependencies to derive systemic implementation priorities.

Repository: **https://github.com/EkodeckStephane/SERP-PublicDecision**

The repository accompanies the study **“Systemic prioritization of digital-transformation gaps: Applying SERP to Cameroon's PATNuC”**. It contains transformed public evidence, de-identified expert coding, model code, sensitivity analyses, and reproducibility metadata. Journal-specific submission files are intentionally kept outside this repository.

## 1. Context

Public-sector digital-transformation programmes are commonly monitored through project components, policy pillars, targets, and performance indicators. These administrative structures are useful for accountability, but implementation bottlenecks do not necessarily respect the same boundaries. Connectivity, digital skills, governance and implementation capacity, affordability, digital trust, and productive adoption can affect several strategic objectives simultaneously.

This creates a practical decision problem. Indicator dashboards can identify which targets are behind schedule, but an isolated target-gap view does not explicitly represent the fact that several implementation domains may be connected through shared strategic objectives. Conversely, a qualitative discussion of interdependence can identify systemic relationships without producing a transparent and reproducible prioritization rule tied to observed implementation evidence.

SERP-PublicDecision addresses this gap by combining two auditable layers:

1. **evidence** — normalized implementation target gaps derived from documented public indicators;
2. **structure** — a binary implementation-domain/objective incidence matrix evaluated through an external expert-coding exercise.

The empirical application uses the World Bank-supported **Acceleration of the Digital Transformation of Cameroon Project (PATNuC)** as a bounded implementation case. Independent national diagnostics are used only for contextual triangulation and are not inserted into the reference target-gap vector.

## 2. Problem

Public-sector prioritization becomes difficult when three conditions occur simultaneously:

- implementation evidence is heterogeneous, sparse, or measured at different levels;
- implementation domains share strategic objectives and therefore cannot be treated as independent silos;
- decision makers need to distinguish priorities that are structurally stable from priorities that depend strongly on a particular evidence-selection rule.

The research problem is therefore to connect four requirements in one transparent workflow:

1. **traceable evidence construction** from public implementation indicators;
2. **explicit representation of strategic interdependence** across implementation domains;
3. **systemic prioritization** that combines direct shortfall and structural exposure;
4. **robustness analysis** that separates model-structure sensitivity from evidence-selection sensitivity.

SERP does **not** estimate a probability of project failure, a causal treatment effect, social welfare, or an optimal budget allocation. Its output is a **systemic implementation-priority signal conditional on the admitted evidence and encoded policy structure**.

## 3. Research question

> **Can traceable target-gap evidence and explicit strategic interdependencies be combined into an auditable public-sector prioritization rule, and which implementation priorities remain stable when the model structure and admissible evidence set are perturbed?**

The repository also examines the conditions that shape the answer: coupling strength, objective removal, single-link perturbation, expert aggregation rule, within-domain aggregation, network normalization, indicator removal, and alternative admissible evidence selections.

## 4. Proposed solution

SERP transforms implementation evidence into systemic priorities through an evidence layer and an interdependency layer.

### 4.1 Evidence layer

For each implementation indicator, the replication package records its inclusion/exclusion decision, transformation rule, domain assignment, and normalized target gap.

The complete audit is stored in:

```text
data/indicator_inventory.csv
```

The transformed analytical dataset is:

```text
data/indicator_data.csv
```

Rows marked `reference_selected=1` define the reference evidence set. Domain loads are calculated from those rows by the analysis code rather than being hard-coded.

The six implementation domains are represented by the codes:

- `GOV` — governance and implementation capacity;
- `CONN` — connectivity;
- `SKILL` — digital skills/capabilities;
- `AFFORD` — affordability;
- `TRUST` — digital trust/security-related implementation conditions;
- `ADOPT` — productive adoption/use.

The repository retains some historical filenames containing the word `risk` (for example `risk_domains.csv` and `risk_scores.csv`). These filenames are part of the frozen replication layout; the scientific interpretation of the current study is **implementation priority**, not probabilistic risk.

### 4.2 Strategic interdependency layer

Let `A` denote the binary domain-objective incidence matrix. A cell equals 1 when an implementation domain is judged to directly affect a strategic objective and 0 otherwise.

The reference matrix is the majority-derived matrix from three external coders. The public expert-validation layer contains anonymized binary ratings, confidence scores, majority and unanimity matrices, and agreement statistics. Original records capable of identifying individual participants are not released.

The majority rule retains a relationship when at least two of the three coders select 1. The unanimity rule is used as a sensitivity condition.

### 4.3 Co-dependence network

SERP derives a symmetric domain co-dependence matrix from shared strategic objectives:

```text
Q = A A^T
```

with the diagonal removed. The reference implementation normalizes this matrix by its spectral radius to obtain `W`.

This construction represents **shared strategic exposure**, not causal direction. It cannot identify signed, directional, lagged, or causal influence between domains.

### 4.4 Evidence-seeded systemic propagation

For direct domain loads `b`, coupling parameter `lambda`, and normalized co-dependence matrix `W`, the reference prioritization is computed as:

```text
z = (I - lambda W)^(-1) b
```

and normalized relative to the largest value.

The resolvent is established mathematics related to Katz/Bonacich-type propagation. The contribution of SERP is not the matrix inverse in isolation; it is the auditable decision architecture that links documented target gaps, explicit policy structure, expert-evaluated mapping, transparent baselines, and separate structural/evidentiary robustness analyses.

The reference analysis uses:

```text
lambda = 0.35
```

and additionally evaluates the full grid from `0.00` to `0.80` in increments of `0.01`.

## 5. Research assets and means used

The study combines public policy/project documents, quantitative decision modelling, expert content validation, and deterministic computational sensitivity analysis.

### 5.1 Public evidence

The repository contains transformed analytical data rather than redistributing the underlying policy and project documents. The underlying sources remain available from the organizations cited in the article.

Key public-data files include:

- `data/indicator_inventory.csv` — complete indicator inclusion/exclusion audit;
- `data/indicator_data.csv` — transformed indicators and normalized target gaps;
- `data/policy_corpus.csv` — policy/document corpus metadata;
- `data/strategic_objectives.csv` — seven strategic objectives;
- `data/external_triangulation.csv` — national diagnostics used only for interpretation;
- `data/patnuc_component_status.csv` — PATNuC component-status context;
- `data/policy_coverage.csv` — policy-coverage metadata.

### 5.2 Expert validation

Three external experts coded all 42 domain-objective pairs. The public replication layer contains only de-identified coder information.

The retained agreement results are:

- 31/42 items unanimous (73.8%);
- mean pairwise observed agreement: 82.5%;
- Fleiss' kappa: 0.645;
- nominal Krippendorff alpha: 0.648;
- mean confidence: 4.12/5;
- pairwise Cohen kappa values: 0.720, 0.748, and 0.503.

The coders were not demonstrably blinded to all implementation values. The exercise is therefore treated as **content validation of the domain-objective mapping**, not as evidence-independent validation of the numerical priority loads. See `expert_validation/README.md`.

### 5.3 Software environment

The audited environment recorded in `RUNTIME.txt` is:

- Python 3.13.5;
- NumPy 2.3.5;
- pandas 2.2.3;
- Matplotlib 3.10.8.

The four analysis scripts are deterministic for the supplied CSV inputs and do not require network access.

## 6. Main analytical results

The repository preserves favorable findings and boundary conditions because both are necessary to interpret the method correctly.

### 6.1 Reference prioritization

At the reference coupling `lambda = 0.35`, the computed relative systemic scores are:

| Rank | Domain | Direct gap | Relative systemic score |
|---:|---|---:|---:|
| 1 | SKILL | 0.9976 | 1.0000 |
| 2 | CONN | 1.0000 | 0.9633 |
| 3 | GOV | 0.8000 | 0.8991 |
| 4 | ADOPT | 0.9473 | 0.8295 |
| 5 | TRUST | 0.6667 | 0.7195 |
| 6 | AFFORD | 0.0882 | 0.2486 |

These values are regenerated by `code/compute_risk_model.py` and stored in `results/risk_scores.csv`.

### 6.2 Coupling sensitivity

Across the 81-point grid `lambda in [0, 0.8]`:

- SKILL remains in the top four in 100% of grid points;
- CONN remains in the top four in 100%;
- GOV remains in the top four in 100%;
- ADOPT is in the top four in approximately 71.6%;
- TRUST enters the top four in approximately 28.4%;
- AFFORD remains outside the top four throughout.

The coupling analysis therefore supports a stable three-domain intersection `SKILL–CONN–GOV` over this structural parameter sweep, while the fourth position is coupling-sensitive.

### 6.3 Objective and mapping perturbations

At the reference evidence set and `lambda = 0.35`:

- removing any one of the seven strategic objectives preserves the reference top-four membership `{SKILL, CONN, GOV, ADOPT}`;
- all 42 single domain-objective link flips preserve that same top-four set.

These checks evaluate structural sensitivity conditional on the reference evidence construction.

### 6.4 Expert aggregation and network normalization

Majority and unanimity coding rules preserve the same reference-evidence top-four membership, although the internal ordering can change. Spectral and row-normalized network constructions also preserve the same top-four membership, with an ordering change between GOV and ADOPT under row normalization.

### 6.5 Evidence-selection sensitivity

Evidence construction is materially consequential.

Only 5 of the 9 leave-one-indicator-out cases remain estimable because removing a singleton indicator would leave its domain without evidence; the admissible leave-one-out cases preserve the reference top-four set.

Several add-back scenarios change the top-four composition. The decisive case is the attained 30-day feedback-response indicator: adding it to GOV lowers the governance domain gap because that indicator has zero target gap and moves GOV outside the top four.

Across the tested evidence-selection constructions, the stable intersection is therefore:

```text
SKILL – CONN – ADOPT
```

This result is central to the interpretation: **structural robustness conditional on one evidence set is not the same as robustness to alternative evidence construction**.

## 7. Scientific positioning

SERP-PublicDecision sits at the intersection of:

- public-sector decision support;
- operations research and quantitative policy analysis;
- network-informed prioritization;
- multi-criteria and portfolio-oriented public decision methods;
- digital-transformation implementation analysis.

SERP is not proposed as a replacement for DEMATEL, ANP, VIKOR, Choquet-integral methods, or optimization-based portfolio selection. Those methods can be more expressive when rich preference judgments, causal assumptions, or optimization objectives are available.

SERP targets a narrower evidence-constrained setting in which the desired properties are:

- direct use of documented target-gap evidence;
- an explicit and inspectable policy-structure layer;
- deterministic recalculation;
- clear separation between evidence and expert mapping inputs;
- sensitivity to both structural assumptions and evidence selection;
- reproducibility with a compact public data/code package.

The article provides the full scientific literature positioning. This repository focuses on the computational evidence and reproducibility materials rather than redistributing the manuscript.

## 8. Repository structure

```text
SERP-PublicDecision/
├── code/
│   ├── analyze_expert_validation.py
│   ├── compute_risk_model.py
│   ├── evidence_selection_robustness.py
│   └── extended_robustness.py
├── data/
│   ├── external_triangulation.csv
│   ├── indicator_data.csv
│   ├── indicator_inventory.csv
│   ├── patnuc_component_status.csv
│   ├── policy_corpus.csv
│   ├── policy_coverage.csv
│   ├── risk_domains.csv
│   ├── risk_objective_matrix.csv
│   └── strategic_objectives.csv
├── expert_validation/
│   ├── README.md
│   ├── expert_ratings_anonymized.csv
│   ├── expert_validation_summary.csv
│   ├── item_agreement.csv
│   ├── consensus_majority_matrix.csv
│   ├── consensus_unanimity_matrix.csv
│   └── initial_analytical_matrix.csv
├── results/                    # Regenerated model and robustness outputs
├── BIBLIOGRAPHIC_VERIFICATION.md
├── CITATION.cff
├── LICENSE.md
├── RELEASE_CHECKLIST.md
├── requirements.txt
├── RUNTIME.txt
└── VERSION
```

The article PDF/LaTeX source, cover letter, internal editorial audits, author photographs, and identifiable expert records are intentionally absent from this repository.

## 9. Reproducibility procedure

### 9.1 Prerequisites

Recommended environment:

- Python 3.13.x for the exact audited runtime;
- Python virtual environment support;
- no network connection required once the repository is cloned.

The numerical Python dependencies are pinned in `requirements.txt`.

### 9.2 Clone

```bash
git clone https://github.com/EkodeckStephane/SERP-PublicDecision.git
cd SERP-PublicDecision
```

### 9.3 Create the Python environment

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

If the PowerShell execution policy blocks activation, either use the environment's Python executable directly or apply an appropriate user-level execution-policy setting according to your local security policy.

### 9.4 Reproduce expert-validation statistics

From the repository root:

```bash
python code/analyze_expert_validation.py
```

This reconstructs the panel agreement statistics and majority/unanimity matrices from the de-identified coding layer.

### 9.5 Reproduce the reference SERP calculation

```bash
python code/compute_risk_model.py
```

This regenerates:

- the reference scores at `lambda = 0.35`;
- the 81-point coupling-sensitivity grid;
- coupling persistence summaries;
- leave-one-objective-out results.

The script verifies that `data/risk_objective_matrix.csv` matches the expert-majority consensus matrix before calculating the reference model.

### 9.6 Reproduce structural robustness checks

```bash
python code/extended_robustness.py
```

This regenerates the single-link perturbation, within-domain aggregation, and network-normalization robustness outputs.

### 9.7 Reproduce evidence-selection robustness

```bash
python code/evidence_selection_robustness.py
```

This regenerates the admissible leave-one-indicator-out analyses, excluded-indicator add-back scenarios, and expert vote-rule sensitivity outputs.

### 9.8 Run the full analytical sequence

Linux/macOS:

```bash
python code/analyze_expert_validation.py
python code/compute_risk_model.py
python code/extended_robustness.py
python code/evidence_selection_robustness.py
```

PowerShell uses the same four `python` commands after activating the virtual environment.

After execution, inspect `results/` and confirm that the regenerated outputs reproduce the retained reference files.

## 10. Integrity, provenance, and privacy

The repository is designed to make each analytical layer inspectable.

Important integrity properties include:

- domain loads are recalculated from rows marked `reference_selected=1` rather than hard-coded;
- the reference domain-objective matrix must equal the majority consensus matrix or the calculation aborts;
- national triangulation data are kept separate from the numerical target-gap vector;
- evidence-selection scenarios are reported separately from structural-model perturbations;
- singleton-domain removals are marked non-estimable rather than silently converted to zero evidence;
- de-identified expert codes are public, while records that may identify individual experts are excluded.

The repository does not claim that the expert coding is causally identified or fully independent of implementation evidence. The documented elicitation record does not establish complete blinding to target-gap magnitudes.

## 11. Scope and limitations

The current replication should be interpreted within the following boundaries:

1. **Case scope** — the numerical priority pattern is specific to the analysed PATNuC implementation evidence and should not be presented as a nationally representative ranking of Cameroon.
2. **Evidence sparsity** — several domains rely on very small indicator sets, including singleton domains.
3. **Expert panel size** — the public mapping-validation exercise uses three external coders.
4. **Mapping semantics** — the binary incidence matrix represents judged direct relationships, not an empirically estimated causal graph.
5. **Network semantics** — the co-dependence construction is symmetric and unsigned.
6. **Cross-sectional design** — the model does not estimate trajectories, intervention effects, or realized public value.
7. **Decision scope** — SERP prioritizes implementation pressure; it does not solve budget allocation or policy optimization.

These are substantive boundary conditions, not hidden implementation caveats. They are retained because they define what can and cannot be inferred from the reported scores.

## 12. Citation

Citation metadata are provided in:

```text
CITATION.cff
```

Until a persistent DOI is minted for the repository or associated article, cite the repository by its GitHub URL and version/commit used for the analysis.

When an archival release is created, update `RELEASE_CHECKLIST.md` and `CITATION.cff` with the permanent identifier rather than inventing one in advance.

## 13. License and redistribution

See:

```text
LICENSE.md
```

The repository redistributes transformed analytical material and code under the scope described in that file. Underlying policy/project documents are not redistributed; consult the original public sources cited by the associated study.

## 14. Maintainer

**Stephane Gael R. EKODECK**  
Department of Computer Science, Faculty of Science, University of Yaounde I, Cameroon  
ORCID: **0000-0002-8094-8832**

For reproducibility issues, use the repository's GitHub issue tracker so that corrections and clarifications remain visible and versioned.
