# Artifact Model and Claim Boundary

## Simulated system

The artifact models authorization requests as exact `(subject, action, resource)` tuples. A stable policy, candidate policies, replay generator, rollout controller, telemetry outputs, and simulated distributed authorization nodes are included.

## Identities, resources, and permissions

The local replay uses four synthetic service identities and eight request templates. Policies are allow-lists of subject/action/resource entitlement tuples. The stable policy contains eight tuples.

## Candidate policies

- `policy_candidate_unsafe.json` removes three permissions exercised by legitimate replay requests. It is designed to test unsafe-candidate detection.
- `policy_candidate_safe.json` removes one stable entitlement generator-labeled redundant and exercised only by low-frequency stale accesses. It is designed to test successful promotion under the same gate.
- `policy_candidate.json` is a documented compatibility alias of the unsafe candidate.

## Authorization oracle

The effective stable policy is not the required-workload oracle. The artifact uses `policy_required.json` as a separate generator-defined required subject/action/resource allow-list. A request is labeled required only when its tuple belongs to that file. The stable policy contains one additional deliberately injected redundant entitlement. This oracle is synthetic, not human-annotated, production-derived, or externally validated.

## Rollout modes

- Immediate enforcement: candidate enforced from request 1.
- Shadow-only validation: candidate evaluated but stable policy always enforced.
- SOR without rollback: first 20% observed, candidate then enforced unconditionally.
- Full SOR: first 20% observed; candidate promoted only if all fixed gates pass.

## Fixed promotion gates

- mismatch rate <= 3%
- required would-deny count <= 0
- candidate expansions <= 0
- at least 20 observations

The exact experiment uses 10,000 observation requests from a 50,000-request replay.

## Repetition and seeds

The primary results are a single deterministic paired replay generated with seed 2026. Requests are deterministic weighted draws from a fixed synthetic vocabulary. Individual requests are not treated as statistically independent enterprise experiments, and the artifact does not report confidence intervals or hypothesis tests for this replay.

## Public configuration structures

The artifact contains an optional static parser for public cloud-native configuration structures. It does not execute third-party projects. These structures do not provide production traffic frequencies or enterprise access semantics.

## What this artifact does not claim

It does not reproduce a production enterprise IAM deployment, prove that unobserved permissions are globally redundant, validate provider-specific policy translation, model all distributed failures, or establish production throughput.

## Effective state versus required-policy oracle

The artifact deliberately separates two concepts that must not be conflated:

- `policy_stable.json` is the effective pre-remediation policy and contains eight entitlements.
- `policy_required.json` is the generator-defined required-workload oracle and contains seven entitlements.
- The set difference contains one explicitly injected redundant entitlement.

The safe candidate removes only that generator-labeled redundant tuple. The replay includes low-frequency stale accesses to it, allowing the artifact to observe stable/candidate mismatches without classifying them as legitimate denials. This is a controlled synthetic oracle, not a claim that unobserved permissions are redundant in production.

## Distributed simulator trigger semantics

The distributed simulator does not use a fixed rollback time. Candidate evaluator propagation is delayed per node, mismatches are computed by directly comparing stable and candidate decisions, and the controller withholds promotion when the measured aggregate mismatch rate crosses the fixed threshold after the minimum event count. The stable policy remains enforced throughout shadow evaluation.


## Sensitivity model

The artifact contains a separate sensitivity generator whose parameters are
predeclared in `config/sensitivity_experiments.json`. It creates medium and large
policy sets deterministically and releases all generated policies and request-level
events. Required, redundant, safe-candidate, and unsafe-candidate sets are
constructed explicitly; the generator never infers semantic redundancy from
non-use. The sensitivity workload is a controlled distribution for gate testing
and is not represented as an enterprise trace.
