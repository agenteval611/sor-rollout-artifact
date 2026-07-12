# Sensitivity Experiment Design

## Purpose

The sensitivity experiments test whether the SOR promotion gate preserves its
functional behavior as identity and policy cardinality increase and as the
mismatch-rate threshold changes. They do not estimate enterprise prevalence or
claim production realism.

## Predeclared configuration

All parameters are machine-readable in `config/sensitivity_experiments.json`.
The experiment uses three deterministic seeds (2026, 2027, and 2028), 50,000
requests per seed, and a 20% observation prefix.

| Scale | Identities | Stable entitlements | Required entitlements |
|---|---:|---:|---:|
| Small | 4 | 8 | 7 |
| Medium | 100 | 500 | 450 |
| Large | 1,000 | 5,000 | 4,500 |

The small scale reuses the bundled primary policy structure. Medium and large
policies are generated deterministically and written to
`results/generated_scale_policies/`.

## Generated request mixture

For the medium and large scales, each request is sampled from one of three
explicit categories:

- 93.5%: oracle-required permission retained by both candidates;
- 6.0%: oracle-required permission removed by the unsafe candidate;
- 0.5%: generator-labeled redundant permission removed by the safe candidate.

The mixture is chosen to exercise both gate outcomes. It is not represented as
an empirical model of enterprise authorization traffic.

## Candidate construction

The unsafe candidate removes 10% of stable-policy tuples, all selected from the
required-policy oracle. The safe candidate removes all generator-labeled
redundant tuples and no required tuples. Redundancy is assigned by the generator;
it is never inferred from absence in the replay.

## Released evidence

For every scale and seed, the artifact releases:

- stable, required, unsafe-candidate, and safe-candidate policy snapshots;
- 50,000 request-level events with both candidate decisions and oracle labels;
- observation-prefix mismatch and required-would-deny counts;
- Full SOR gate actions;
- aggregate and summary CSVs.

`validate_fps_results.py` recomputes the reported values from these raw files.

## Threshold sensitivity

The primary replay is reevaluated at mismatch thresholds 0.005, 0.01, 0.03,
0.05, and 0.10. The required-denial and candidate-expansion thresholds remain
fixed at zero. This isolates the mismatch threshold rather than changing several
gates simultaneously.
