# Reviewer-Risk Checklist

This checklist maps recurring empirical-review risks to concrete artifact evidence.

- **System model underspecified:** `ARTIFACT_MODEL.md` defines policies, requests, oracle, candidates, modes, and claim boundaries.
- **Oracle unclear or leaked:** effective stable state and required-policy oracle are separate files; raw rows include `oracle_required`.
- **Hardcoded table values:** aggregate tables are regenerated from request-level output and recomputed by `validate_fps_results.py`.
- **Identical conditions without explanation:** each rollout mode has explicit enforcement semantics; shared mismatch counts are expected because the same paired replay and candidate are evaluated.
- **Missing raw counts:** `results/raw/fps_replay_events.csv` contains one row per candidate, mode, and request.
- **Missing ablation/condition output:** only experiments with generated numeric outputs are documented as results.
- **Synthetic evaluation overstated:** README and model document explicitly bound claims and distinguish configuration structures from traffic traces.
- **Repeated runs treated as independent:** the artifact explicitly identifies the primary result as one deterministic paired replay.
- **Environment-dependent reproduction:** `run_all.sh` is Docker-independent and excludes runtime benchmarking by default.
- **Reviewer cannot run artifact:** fail-fast environment checker, pinned dependencies, unit tests, validator, and checksum manifest are included.
- **Anonymity leakage:** final packaging removes caches and scans for names, emails, local paths, and prior-conference references.
- **Only one tiny synthetic configuration:** `config/sensitivity_experiments.json` predeclares small, medium, and large scales; generated policies and request-level events are released for three seeds per scale.
- **Magic threshold concern:** `artifact_results/threshold_sensitivity.csv` recomputes the primary gate at five mismatch thresholds while holding the required-denial and expansion gates fixed.
- **Scale results cannot be inspected:** `results/generated_scale_policies/` and `results/raw/scale_sensitivity/` expose every generated policy and request-level event used by the scale table.
