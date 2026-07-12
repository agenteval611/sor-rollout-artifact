#!/usr/bin/env bash
set -euo pipefail
export PYTHONDONTWRITEBYTECODE=1
cd "$(dirname "$0")/.."

MODE="--example-fallback"
WITH_BENCHMARK=0
for arg in "$@"; do
  case "$arg" in
    --public) MODE="--public" ;;
    --with-benchmark) WITH_BENCHMARK=1 ;;
    -h|--help)
      cat <<'EOF'
Usage: bash scripts/run_all.sh [--public] [--with-benchmark]

Default: deterministic, offline, Docker-independent reproduction of paper tables.
--public: use previously fetched public-source inputs (network fetch remains separate).
--with-benchmark: additionally run the host-specific microbenchmark.
The optional Docker demonstration is run separately with bash scripts/run_docker_demo.sh.
EOF
      exit 0 ;;
    *) echo "Unknown argument: $arg" >&2; exit 2 ;;
  esac
done

if [[ "$MODE" == "--public" ]]; then
  if [[ ! -d datasets/public_sources/extracted ]] || [[ -z "$(find datasets/public_sources/extracted -type f \( -name '*.yaml' -o -name '*.yml' -o -name '*.rego' \) 2>/dev/null | head -1)" ]]; then
    cat >&2 <<'EOF'
No extracted public sources found. Run:
  bash scripts/fetch_public_sources.sh
  python3 scripts/extract_public_policy_configs.py
Then rerun:
  bash scripts/run_all.sh --public
EOF
    exit 1
  fi
fi

mkdir -p results/raw results/tables results/figures artifact_results paper
rm -f \
  results/raw/events.csv results/raw/events.delay_*.csv results/raw/public_policy_events.csv \
  results/raw/fps_replay_events.csv results/raw/scale_sensitivity/*.csv results/tables/*.csv results/tables/*.json \
  results/figures/*.png artifact_results/baseline_comparison.csv \
  artifact_results/replay_prefix_sensitivity.csv artifact_results/observation_window_sensitivity.csv \
  artifact_results/scale_sensitivity.csv artifact_results/scale_sensitivity_summary.csv \
  artifact_results/threshold_sensitivity.csv artifact_results/sensitivity_experiment_metadata.json \
  artifact_results/fps_experiment_metadata.json artifact_results/delay_sensitivity.csv \
  artifact_results/delay_sensitivity.json artifact_results/distributed_metrics.csv \
  artifact_results/distributed_metrics.json artifact_results/node_summary.csv \
  artifact_results/low_frequency_workflows.csv artifact_results/public_policy_workload_metrics.csv \
  artifact_results/public_source_extraction_metrics.json artifact_results/*.png \
  artifact_results/SHA256SUMS.txt paper/tables.tex paper/fps_tables.tex paper/sensitivity_tables.tex
if [[ "$WITH_BENCHMARK" -eq 1 ]]; then
  rm -f artifact_results/runtime_benchmark.csv artifact_results/runtime_benchmark.json
fi

printf '[1/10] Checking environment and required inputs\n'
python3 scripts/check_environment.py
printf '[2/10] Running semantic unit tests\n'
python3 -m unittest discover -s tests -v
printf '[3/10] Generating configuration-structure-derived workload (%s)\n' "$MODE"
bash ./scripts/generate_public_policy_workload.sh "$MODE"
printf '[4/10] Running deterministic local distributed simulation\n'
python3 scripts/simulate_distributed_run.py
printf '[5/10] Generating distributed tables and figures\n'
python3 scripts/make_tables_and_figures.py
printf '[6/10] Generating safe/unsafe FPS candidate results\n'
python3 scripts/run_fps_experiments.py --requests 50000 --seed 2026
if [[ "$WITH_BENCHMARK" -eq 1 ]]; then
  printf '[7/10] Running optional host-specific microbenchmark\n'
  python3 scripts/benchmark_runtime.py
else
  printf '[7/10] Skipping host-specific benchmark (use --with-benchmark to enable)\n'
fi
printf '[8/10] Generating multi-scale and threshold sensitivity results\n'
python3 scripts/run_sensitivity_experiments.py
printf '[9/10] Validating generated results from raw outputs\n'
python3 scripts/validate_fps_results.py
printf '[10/10] Writing checksums for primary generated outputs\n'
python3 scripts/generate_checksums.py

printf '\nPrimary results written to artifact_results/, results/raw/, results/tables/, and paper/.\n'
printf 'Artifact reproduction complete: deterministic paper tables regenerated and validation passed.\n'
