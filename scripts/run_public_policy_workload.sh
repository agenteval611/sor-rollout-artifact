#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
MODE="${1:-}"
bash scripts/generate_public_policy_workload.sh "${MODE}"
python3 scripts/simulate_distributed_run.py --public-only
python3 scripts/make_tables_and_figures.py
cat results/tables/public_policy_workload_metrics.csv
