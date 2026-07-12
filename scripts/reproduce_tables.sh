#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m telemetry.metrics
python3 scripts/make_tables_and_figures.py
cat results/tables/distributed_metrics.csv
