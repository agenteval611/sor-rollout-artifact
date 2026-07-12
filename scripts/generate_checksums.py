#!/usr/bin/env python3
from __future__ import annotations
import hashlib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "artifact_results" / "SHA256SUMS.txt"
FILES = [
    ROOT / "artifact_results/baseline_comparison.csv",
    ROOT / "artifact_results/replay_prefix_sensitivity.csv",
    ROOT / "artifact_results/fps_experiment_metadata.json",
    ROOT / "artifact_results/delay_sensitivity.csv",
    ROOT / "results/raw/fps_replay_events.csv",
    ROOT / "paper/fps_tables.tex",
    ROOT / "artifact_results/scale_sensitivity.csv",
    ROOT / "artifact_results/scale_sensitivity_summary.csv",
    ROOT / "artifact_results/threshold_sensitivity.csv",
    ROOT / "artifact_results/sensitivity_experiment_metadata.json",
    ROOT / "paper/sensitivity_tables.tex",
]
lines=[]
for p in FILES:
    digest=hashlib.sha256(p.read_bytes()).hexdigest()
    lines.append(f"{digest}  {p.relative_to(ROOT).as_posix()}")
OUT.write_text("\n".join(lines)+"\n", encoding="utf-8")
print(f"Wrote {OUT.relative_to(ROOT)}")
