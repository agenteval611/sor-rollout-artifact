# Shadow--Observe--Restrict Artifact

Anonymous reproducibility artifact for controlled least-privilege rollout experiments.

## What the artifact contains

- FastAPI authorization and rollout-control prototype
- effective stable, generator-required oracle, unsafe-candidate, and safe-candidate policy snapshots
- deterministic 50,000-request replay generator
- four rollout-mode implementations
- request-level raw outputs and aggregate CSV tables
- three-node propagation-delay simulation
- multi-scale sensitivity at 4/100/1,000 identities and 8/500/5,000 stable entitlements
- mismatch-threshold sensitivity on the primary replay
- optional static extraction of public cloud-native authorization structures
- local runtime microbenchmark

## Main reproduction command

From the artifact root:

```bash
bash scripts/run_all.sh
```

The command always uses the deterministic local simulation, regardless of whether Docker is installed. This prevents reviewer environments from selecting different reproduction paths. The primary FPS results require no network access, cloud credentials, or proprietary data. The Docker service demonstration is optional and separate.

The command regenerates:

```text
artifact_results/baseline_comparison.csv
artifact_results/replay_prefix_sensitivity.csv
artifact_results/fps_experiment_metadata.json
artifact_results/delay_sensitivity.csv
artifact_results/scale_sensitivity.csv
artifact_results/scale_sensitivity_summary.csv
artifact_results/threshold_sensitivity.csv
artifact_results/sensitivity_experiment_metadata.json
results/raw/fps_replay_events.csv
results/raw/scale_sensitivity/*.csv
results/generated_scale_policies/*/*.json
paper/fps_tables.tex
paper/sensitivity_tables.tex
```

It first checks the environment, runs semantic unit tests, regenerates the outputs, validates aggregate results against request-level raw data, and writes SHA-256 checksums for primary generated files.

## Primary FPS candidate experiment

Run only this experiment with:

```bash
python3 scripts/run_fps_experiments.py --requests 50000 --seed 2026
python3 scripts/validate_fps_results.py
```

The same effective stable policy, required-policy oracle, and request replay are used for two candidates:

- **Unsafe candidate:** proposes a 37.5% policy reduction by removing three oracle-required permissions. Full SOR withholds promotion.
- **Safe candidate:** proposes a 12.5% policy reduction by removing one generator-labeled redundant entitlement. The replay includes low-frequency stale accesses to this tuple, so the candidate produces observable mismatches while denying no oracle-required request. Full SOR promotes it.

The safe label is relative to the generator-defined required-policy oracle. The effective stable policy contains one explicitly injected redundant entitlement. This synthetic label is not evidence that non-use alone proves real-world redundancy.

## Fixed promotion thresholds

The experiment fixes all gates before replay execution:

```text
Observation prefix:             20% (10,000 of 50,000 requests)
Minimum observations:           20
Mismatch-rate threshold:        0.03
Legitimate-denial threshold:    0
Candidate-expansion threshold:  0
Seed:                           2026
```

Machine-readable values are stored in `artifact_results/fps_experiment_metadata.json`.

## Rollout modes

- **Immediate enforcement:** candidate decisions are enforced from request 1.
- **Shadow-only validation:** candidate decisions are logged; stable decisions remain enforced.
- **SOR without rollback:** first 20% is observed, then the candidate is enforced unconditionally.
- **Full SOR:** first 20% is observed; the candidate is promoted only when every gate passes.

The output uses precise safety actions: `Shadow only`, `Promotion withheld`, and `Promoted`. Promotion withholding is not mislabeled as rollback.

## Metrics

- **Mismatch:** stable and candidate decisions differ.
- **Legitimate denial:** a request in `policy_required.json` is denied by the enforced decision.
- **LDR:** legitimate denials divided by all replay requests.
- **Candidate LDR:** required requests the candidate would deny divided by requests in a shadow-evaluated replay prefix.
- **Affected IDs:** distinct subjects experiencing enforced legitimate denials.
- **Proposed reduction:** stable-policy tuples absent from the candidate.
- **Enforced reduction:** proposed reduction actually placed into force after the rollout approach completes.

## Raw request-level output

`results/raw/fps_replay_events.csv` includes:

```text
request_id,candidate,candidate_label,approach,phase,subject,action,resource,
expected_rare,stable_decision,candidate_decision,enforced_decision,
oracle_required,mismatch,candidate_would_deny_required,legitimate_denial,
safety_action
```

## Scale and threshold sensitivity

The default reproduction also runs predeclared sensitivity experiments from
`config/sensitivity_experiments.json`. The primary 50K experiment remains
unchanged. The additional experiments evaluate Full SOR at three scales and
three deterministic seeds per scale:

```text
Small:       4 identities,    8 stable entitlements,    7 required
Medium:    100 identities,  500 stable entitlements,  450 required
Large:   1,000 identities, 5,000 stable entitlements, 4,500 required
```

Each seed uses 50,000 requests and a 20% observation prefix. Medium and large
policies are created by a transparent deterministic generator. The generated
policies, per-request raw events, per-seed outputs, summary CSV, metadata, and
LaTeX-ready tables are committed to the artifact.

The generated request mixture is fixed before execution: 93.5% required
requests retained by both candidates, 6.0% required requests removed by the
unsafe candidate, and 0.5% accesses to generator-labeled redundant
entitlements removed by the safe candidate. This construction tests control-loop
behavior across scale; it is not presented as an enterprise traffic model.

Threshold sensitivity recomputes the primary observation gate at mismatch
thresholds 0.005, 0.01, 0.03, 0.05, and 0.10 while holding the required-denial
and expansion gates fixed at zero. It shows that a very strict threshold can
withhold the safe candidate, while the unsafe candidate remains blocked at every
threshold because it would deny oracle-required requests.

Primary files:

```text
artifact_results/scale_sensitivity.csv
artifact_results/scale_sensitivity_summary.csv
artifact_results/threshold_sensitivity.csv
artifact_results/sensitivity_experiment_metadata.json
results/raw/scale_sensitivity/*.csv
results/generated_scale_policies/*/*.json
paper/sensitivity_tables.tex
```

## Distributed propagation-delay experiment

The event-driven local simulation evaluates three authorization nodes under 500, 3,000, and 7,000 ms configured delays. Nodes receive the candidate shadow evaluator after delayed propagation; the stable policy remains enforced. Mismatches are computed from direct stable/candidate decision comparison, and promotion withholding is triggered only when the aggregate threshold is actually crossed. This experiment is separate from the 50K candidate replay.

```bash
python3 scripts/simulate_distributed_run.py
```


Host-specific runtime benchmark outputs are generated only when running:

```bash
bash scripts/run_all.sh --with-benchmark
```

## Optional Docker prototype

Run the service-level demonstration separately:

```bash
bash scripts/run_docker_demo.sh
```

Docker outputs are diagnostic and are not used to generate the paper tables. The endpoints are minimal and not authenticated or production-hardened.

## Reviewer orientation

- `REVIEWER_GUIDE.md` explains what the controlled evaluation demonstrates and what it does not claim.
- `PUBLIC_CONFIG_CASE_STUDY.md` documents the optional public-source extraction path and its interpretation boundaries.

## Optional public-source structure extraction

Recorded sources are listed in `datasets/metadata/public_sources.csv`.

```bash
bash scripts/fetch_public_sources.sh
python3 scripts/extract_public_policy_configs.py
bash scripts/run_all.sh --public
```

The extractor performs static parsing only. Public structures do not provide production request frequencies, temporal dependencies, or enterprise access semantics.

## Environment and troubleshooting

Python 3.10 or newer is required. First verify the interpreter version:

```bash
python3 --version
```

If `python3` reports version 3.10 or newer, create and activate a virtual environment:

```bash
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
bash scripts/run_all.sh
```

If the system `python3` is older than 3.10, create the environment with an installed compatible interpreter, for example:

```bash
python3.11 -m venv .venv
source .venv/bin/activate
python3 --version
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
bash scripts/run_all.sh
```

The macOS-provided Python 3.9 interpreter is not supported.

Use `python3 scripts/check_environment.py` for a fail-fast dependency and input check. Host-specific runtime measurements are excluded from the default reproduction path; run `bash scripts/run_all.sh --with-benchmark` only when such diagnostics are desired.

## Result documentation

See:

- `artifact_results/README_tables.md`
- `ARTIFACT_MODEL.md`
- `ARTIFACT_AUDIT.md`
- `datasets/SOURCES.md`

## Claim boundary

The artifact demonstrates the rollout control loop under controlled synthetic conditions. It does not reproduce a production enterprise IAM deployment, prove that unobserved permissions are globally redundant, or establish production throughput.
