# Reproducibility Protocol

## Supported path

The paper tables are reproduced with one offline, deterministic command:

```bash
bash scripts/run_all.sh
```

This path never auto-selects Docker and never runs the host-dependent runtime benchmark. Docker and benchmarking are explicit optional diagnostics.

## Clean setup

```bash
python3 --version  # must report 3.10 or newer
python3 -m venv .venv
source .venv/bin/activate
python3 -m pip install --upgrade pip
python3 -m pip install -r requirements.txt
bash scripts/run_all.sh
```

If the system `python3` is older than 3.10, create the environment with an installed compatible interpreter such as `python3.11 -m venv .venv`. Python 3.10+ is required. Dependencies are pinned in `requirements.txt`. No network access is required after installation.

## Validation

The command runs:

1. environment and JSON input checks;
2. semantic unit tests for stable, required, safe, and unsafe policy relationships;
3. deterministic distributed simulation;
4. deterministic 50K paired replay;
5. multi-scale and threshold sensitivity generation;
6. aggregate-versus-raw validation for primary and sensitivity outputs; and
7. SHA-256 generation for primary outputs.

`artifact_results/SHA256SUMS.txt` identifies the generated files used by the paper.

## Independence and statistics

The primary replay is one deterministic paired workload with seed 2026. Requests are weighted synthetic draws and are not represented as independent enterprise samples. The artifact does not use per-request confidence intervals or significance tests.

## Optional paths

- `bash scripts/run_docker_demo.sh`: service-level demonstration; not the paper reproduction path.
- `bash scripts/run_all.sh --with-benchmark`: host-specific microbenchmark; not a primary paper result.
- public-source fetching is separate because it requires network access.


## Sensitivity protocol

Scale and threshold settings are declared in
`config/sensitivity_experiments.json`. Scale sensitivity uses 50,000 requests
for each of seeds 2026, 2027, and 2028 at three policy sizes. Every generated
policy is stored under `results/generated_scale_policies/`, and every
request-level trace is stored under `results/raw/scale_sensitivity/`.

The scale experiment is intended to test whether gate behavior remains stable
as identity and policy cardinality increase. It does not claim that the generated
request mixture reproduces production enterprise traffic. Threshold sensitivity
uses the fixed primary replay and changes only the mismatch-rate threshold; the
required-denial and expansion gates remain fixed.
