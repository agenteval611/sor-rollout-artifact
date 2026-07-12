# Updated Files and Outputs

## Code

- `scripts/run_fps_experiments.py`: implements safe and unsafe candidates, four rollout modes, explicit gate semantics, raw event output, aggregate CSVs, metadata, and LaTeX tables.
- `scripts/validate_fps_results.py`: validates the expected unsafe-candidate withholding and safe-candidate promotion outcomes.
- `scripts/run_all.sh`: regenerates all outputs while preserving documentation and runs validation.

## Policies

- `datasets/examples/policy_candidate_unsafe.json`
- `datasets/examples/policy_candidate_safe.json`
- `datasets/examples/policy_candidate.json` (compatibility alias for the unsafe candidate)

## Documentation

- `README.md`
- `ARTIFACT_MODEL.md`
- `ARTIFACT_AUDIT.md`
- `artifact_results/README_tables.md`

## Primary regenerated results

- `artifact_results/baseline_comparison.csv`
- `artifact_results/replay_prefix_sensitivity.csv`
- `artifact_results/fps_experiment_metadata.json`
- `artifact_results/delay_sensitivity.csv`
- `results/raw/fps_replay_events.csv`
- `paper/fps_tables.tex`

## Removed or superseded

- hardcoded FPS table generator
- old observation-window CSV naming and semantics
- ambiguous `Rollback Triggered` comparison field
- Python bytecode caches

## Added sensitivity experiment code and configuration

- `config/sensitivity_experiments.json`: predeclared scale, seed, request-mix, and threshold settings.
- `scripts/run_sensitivity_experiments.py`: generates scale and threshold sensitivity outputs from released policies and raw events.
- `tests/test_artifact.py`: validates sensitivity configuration in addition to primary policy semantics.
- `scripts/validate_fps_results.py`: independently recomputes scale and threshold statistics from raw outputs.
- `scripts/generate_checksums.py`: includes sensitivity outputs in the checksum manifest.

## Added sensitivity outputs

- `artifact_results/scale_sensitivity.csv`
- `artifact_results/scale_sensitivity_summary.csv`
- `artifact_results/threshold_sensitivity.csv`
- `artifact_results/sensitivity_experiment_metadata.json`
- `results/raw/scale_sensitivity/*.csv`
- `results/generated_scale_policies/*/*.json`
- `paper/sensitivity_tables.tex`
