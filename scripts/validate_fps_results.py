#!/usr/bin/env python3
"""Recompute primary FPS results from raw files and fail on any mismatch."""
from __future__ import annotations
import csv
import json
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifact_results"
RAW = ROOT / "results/raw"


def b(v: str) -> bool:
    return str(v).lower() in {"true", "1", "yes"}

comparison = list(csv.DictReader((ART / "baseline_comparison.csv").open()))
meta = json.loads((ART / "fps_experiment_metadata.json").read_text())
delay = list(csv.DictReader((ART / "delay_sensitivity.csv").open()))

assert len(comparison) == 8
assert meta["seed"] == 2026 and meta["request_count"] == 50000
assert meta["required_policy_file"] == "datasets/examples/policy_required.json"
assert meta["stable_entitlements"] == 8 and meta["required_entitlements"] == 7
assert meta["generator_labeled_redundant_entitlements"] == 1
assert meta["thresholds"] == {
    "observation_prefix_fraction": 0.2,
    "observation_prefix_requests": 10000,
    "minimum_gate_observations": 20,
    "mismatch_rate_threshold": 0.03,
    "legitimate_denial_threshold": 0,
    "candidate_expansion_threshold": 0,
}

idx = {(r["Candidate"], r["Approach"]): r for r in comparison}
assert idx[("Unsafe candidate", "Full SOR")]["Safety Action"] == "Promotion withheld"
assert idx[("Safe candidate", "Full SOR")]["Safety Action"] == "Promoted"
assert float(idx[("Unsafe candidate", "Full SOR")]["Enforced Reduction %"]) == 0
assert float(idx[("Safe candidate", "Full SOR")]["Enforced Reduction %"]) == 12.5

# Stream the large raw file to avoid requiring hundreds of MB of reviewer memory.
groups = defaultdict(lambda: {"rows": 0, "denials": 0, "affected": set(), "mismatches": 0})
with (RAW / "fps_replay_events.csv").open(newline="", encoding="utf-8") as f:
    for r in csv.DictReader(f):
        g = groups[(r["candidate_label"], r["approach"])]
        g["rows"] += 1
        if b(r["legitimate_denial"]):
            g["denials"] += 1
            g["affected"].add(r["subject"])
        g["mismatches"] += int(b(r["mismatch"]))
assert sum(g["rows"] for g in groups.values()) == 2 * 4 * 50000
for row in comparison:
    g = groups[(row["Candidate"], row["Approach"])]
    assert g["rows"] == 50000
    assert g["denials"] == int(row["Legitimate Denials"])
    assert len(g["affected"]) == int(row["Affected IDs"])
    assert g["mismatches"] == int(row["Mismatches"])
    assert abs(g["denials"] / g["rows"] - float(row["LDR"])) < 1e-12

assert len(delay) == 3

for row in delay:
    d = int(row["delay_ms"])
    raw_path = RAW / f"events.delay_{d}ms.csv"
    metrics_path = ROOT / "results" / "tables" / f"distributed_metrics.delay_{d}ms.json"

    assert raw_path.is_file(), f"missing raw delay events for {d} ms"
    assert metrics_path.is_file(), f"missing distributed metrics for {d} ms"

    raw_rows = list(csv.DictReader(raw_path.open(newline="", encoding="utf-8")))
    metrics = json.loads(metrics_path.read_text(encoding="utf-8"))["metrics"]

    assert int(row["events"]) == len(raw_rows)
    assert int(row["events"]) == int(metrics["events"])

    stale = sum(int(b(r["stale_candidate_evaluator"])) for r in raw_rows)
    assert int(row["stale_exposure"]) == stale
    assert int(row["stale_exposure"]) == int(metrics["stale_candidate_evaluator_events"])

    logical_groups = defaultdict(set)
    for r in raw_rows:
        logical_groups[r["logical_request_id"]].add(r["candidate_decision"])

    divergence = sum(len(v) > 1 for v in logical_groups.values()) / max(len(logical_groups), 1)

    assert abs(float(row["divergence_rate"]) - divergence) < 1e-12
    assert abs(float(row["divergence_rate"]) - float(metrics["enforcement_divergence_rate"])) < 1e-12

    assert int(row["convergence_ms"]) == int(metrics["restoration_convergence_time_ms"])

# Validate multi-scale sensitivity from request-level files.
scale_rows = list(csv.DictReader((ART / "scale_sensitivity.csv").open()))
scale_summary = list(csv.DictReader((ART / "scale_sensitivity_summary.csv").open()))
threshold_rows = list(csv.DictReader((ART / "threshold_sensitivity.csv").open()))
sensitivity_meta = json.loads((ART / "sensitivity_experiment_metadata.json").read_text())
assert len(scale_rows) == 9
assert len(scale_summary) == 3
assert len(threshold_rows) == 10
assert sensitivity_meta["seeds"] == [2026, 2027, 2028]
assert sensitivity_meta["requests_per_seed"] == 50000
expected_scale_counts = {
    "Small": (4, 8, 7),
    "Medium": (100, 500, 450),
    "Large": (1000, 5000, 4500),
}
for row in scale_rows:
    scale = row["Scale"]
    assert scale in expected_scale_counts
    identities, stable_n, required_n = expected_scale_counts[scale]
    assert int(row["Identities"]) == identities
    assert int(row["Stable Entitlements"]) == stable_n
    assert int(row["Required Entitlements"]) == required_n
    assert int(row["Requests"]) == 50000
    assert int(row["Observation Requests"]) == 10000
    raw_path = ROOT / row["Raw Event File"]
    assert raw_path.is_file()
    counts = {
        "rows": 0, "obs": 0, "unsafe_m": 0, "safe_m": 0,
        "unsafe_wd": 0, "safe_wd": 0,
    }
    with raw_path.open(newline="", encoding="utf-8") as f:
        for event in csv.DictReader(f):
            counts["rows"] += 1
            if event["phase"] == "observation":
                counts["obs"] += 1
                counts["unsafe_m"] += int(b(event["unsafe_mismatch"]))
                counts["safe_m"] += int(b(event["safe_mismatch"]))
                counts["unsafe_wd"] += int(b(event["unsafe_required_would_deny"]))
                counts["safe_wd"] += int(b(event["safe_required_would_deny"]))
    assert counts["rows"] == 50000 and counts["obs"] == 10000
    assert counts["unsafe_m"] == int(row["Unsafe Observation Mismatches"])
    assert counts["safe_m"] == int(row["Safe Observation Mismatches"])
    assert counts["unsafe_wd"] == int(row["Unsafe Required Would-Deny"])
    assert counts["safe_wd"] == int(row["Safe Required Would-Deny"])
    assert abs(counts["unsafe_m"] / 10000 - float(row["Unsafe Observation Mismatch Rate"])) < 1e-12
    assert abs(counts["safe_m"] / 10000 - float(row["Safe Observation Mismatch Rate"])) < 1e-12
    assert row["Unsafe Full SOR Action"] == "Promotion withheld"
    assert row["Safe Full SOR Action"] == "Promoted"
    assert int(row["Unsafe Legitimate Denials"]) == 0
    assert int(row["Safe Legitimate Denials"]) == 0

# Verify generated policy sizes and set relationships for every scale.
def policy_rules(path):
    data = json.loads(path.read_text())
    return {(r["subject"], r["action"], r["resource"]) for r in data["allow"]}
for key, (_, stable_n, required_n) in {
    "small": expected_scale_counts["Small"],
    "medium": expected_scale_counts["Medium"],
    "large": expected_scale_counts["Large"],
}.items():
    d = ROOT / "results/generated_scale_policies" / key
    stable = policy_rules(d / "policy_stable.json")
    required = policy_rules(d / "policy_required.json")
    unsafe = policy_rules(d / "policy_candidate_unsafe.json")
    safe = policy_rules(d / "policy_candidate_safe.json")
    assert len(stable) == stable_n and len(required) == required_n
    assert required < stable
    assert safe == required
    assert required - unsafe
    assert unsafe <= stable

# Threshold sensitivity must be a pure recomputation of the fixed primary gate.
threshold_index = {(r["Mismatch Threshold"], r["Candidate"]): r for r in threshold_rows}
for threshold in ["0.005", "0.010", "0.030", "0.050", "0.100"]:
    u = threshold_index[(threshold, "Unsafe candidate")]
    srow = threshold_index[(threshold, "Safe candidate")]
    assert int(u["Observation Mismatches"]) == 599
    assert int(u["Required Would-Deny"]) == 599
    assert u["Full SOR Action"] == "Promotion withheld"
    assert int(srow["Observation Mismatches"]) == 93
    assert int(srow["Required Would-Deny"]) == 0
    expected_safe = "Promotion withheld" if threshold == "0.005" else "Promoted"
    assert srow["Full SOR Action"] == expected_safe

print("FPS result validation: PASS")
