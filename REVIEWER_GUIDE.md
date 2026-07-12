# Reviewer Guide

This artifact reproduces the controlled evaluation of the
Shadow–Observe–Restrict rollout-safety framework.

## Main reproduction

From the artifact root, run:

```bash
bash scripts/run_all.sh
```

This command performs an offline, deterministic reproduction of the primary
rollout comparison, scale sensitivity, mismatch-threshold sensitivity, and
propagation-delay experiments. It regenerates the reported tables and validates
their values from released raw outputs.

## What the artifact demonstrates

Under the released generator-defined authorization oracle, the artifact
demonstrates that:

1. Full SOR withholds an unsafe candidate that removes oracle-required
   permissions.
2. Full SOR promotes a candidate that removes only a generator-labeled
   redundant entitlement.
3. This gate behavior persists across generated policy graphs containing
   4, 100, and 1,000 identities and up to 5,000 stable entitlements.
4. The safe-candidate result is not dependent only on the primary mismatch
   threshold of 0.03.
5. Propagation delay increases stale-evaluator exposure and restoration
   convergence time and, under the largest tested delay, decision divergence.

## What the artifact does not demonstrate

The artifact does not claim to reproduce production enterprise authorization
traffic. It does not use customer telemetry, employer data, proprietary IAM
logs, or human-validated business-critical workload labels.

The safe and unsafe candidate labels are valid only relative to the released
generator-defined required-policy oracle.

The generated scale experiments test rollout-control behavior as policy
cardinality increases. They do not establish production traffic realism or
production-scale entitlement-reduction effectiveness.

## Why synthetic workloads are used

Production authorization traces can contain sensitive identity, resource,
workload, and business-process information. The artifact therefore uses
transparent synthetic workloads and configuration-derived authorization
structures so that the evaluation is inspectable and reproducible without
customer, employer, or proprietary telemetry.

## Public-source structural grounding

The artifact includes an optional path that statically extracts authorization
structures from selected public cloud-native repositories. This path provides
external structural grounding through subjects, resources, actions, roles,
bindings, and permission relationships.

It does not provide production request frequencies, temporal workflow
dependencies, identity ownership, or ground-truth business-critical labels.

Public-source fetching is kept separate from the default reproduction because
it requires network access and may be affected by repository availability or
rate limits. See `PUBLIC_CONFIG_CASE_STUDY.md` for the exact workflow and
interpretation boundaries.
