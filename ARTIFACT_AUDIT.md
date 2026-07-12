# Artifact Audit Status

## Current status

The artifact has been revised so that all FPS comparison rows are generated from request-level events. The original hardcoded FPS table generator has been removed.

## Corrections incorporated

- added distinct unsafe and safe candidate policies
- implemented successful safe-candidate promotion
- replaced ambiguous rollback flags with explicit safety actions
- separated proposed from enforced policy reduction
- renamed FPR to legitimate-denial rate (LDR)
- made all gate thresholds machine-readable
- added candidate and approach fields to raw event outputs
- renamed observation-window output to replay-prefix sensitivity
- documented that prefix values are shadow outcomes, not enforced denials
- added automated result invariants
- preserved documentation when `run_all.sh` cleans generated outputs
- removed Python cache files and obsolete hardcoded generator

## Primary expected outcomes

- Unsafe candidate + Full SOR: promotion withheld, 0% enforced reduction, zero enforced legitimate denials.
- Safe candidate + Full SOR: promoted, 12.5% enforced reduction, zero enforced legitimate denials.

## Remaining limitations

The policy graph and request vocabulary are intentionally small and synthetic. The required-policy file is the generator-defined oracle; the stable policy is the effective pre-remediation state. Results are one deterministic paired replay with seed 2026. The safe candidate is safe relative to the explicit generator-defined required-policy oracle; this remains a synthetic claim, not production validation.
