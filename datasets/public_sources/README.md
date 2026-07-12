# Public authorization configuration sources

This artifact does not vendor full third-party repositories by default. Instead, it records the public repositories used for policy-derived workload generation and provides reproducible fetch/extraction scripts.

Rationale:

- avoid redistributing large third-party repositories;
- preserve upstream license attribution through `datasets/metadata/public_sources.csv`;
- avoid executing untrusted repository code;
- keep the artifact lightweight and reviewer friendly.

Use:

```bash
bash scripts/fetch_public_sources.sh
python3 scripts/extract_public_policy_configs.py
bash scripts/run_all.sh --public
```

The extraction step performs static parsing only. It reads YAML/YML/Rego files and GitHub Actions workflow permission declarations. It does not run Makefiles, Dockerfiles, CI jobs, shell scripts, Helm installs, or project-specific binaries.

The default command uses the included local cloud-native configuration examples and is fully offline:

```bash
bash scripts/run_all.sh
```

The explicit public-source mode does not silently fall back. It requires previously fetched and extracted public inputs and exits before modifying generated outputs when those inputs are absent:

```bash
bash scripts/run_all.sh --public
```

See `../../PUBLIC_CONFIG_CASE_STUDY.md` for interpretation boundaries and the complete optional workflow.
