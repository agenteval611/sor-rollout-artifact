# Dataset and Source Notes

This artifact supports two workload modes.

## 1. Offline example mode

The files under `datasets/examples/` are small local examples. They are included only to make the artifact runnable without network access.

Use this wording when reporting example-mode results:

> configuration-structure-derived examples

Do **not** describe example-mode results as a public dataset evaluation.

## 2. Public repository source mode

The artifact records selected public repositories in:

```text
datasets/metadata/public_sources.csv
```

The selected sources are public cloud-native authorization/configuration repositories containing Kubernetes RBAC manifests, GitHub Actions workflow permissions, and/or Rego policy files.

The artifact does not vendor full third-party repositories. Instead, run:

```bash
bash scripts/fetch_public_sources.sh
python3 scripts/extract_public_policy_configs.py
bash scripts/run_all.sh --public
```

The extractor performs static analysis only. It reads YAML/YML/Rego files and copies/extracts only configuration-policy artifacts into `datasets/public_sources/extracted/`. It does not execute repository code, install Helm charts, run CI workflows, run containers, or invoke project-specific scripts.

## Source provenance

The public-source list currently includes:

| Source | Type | License | URL |
|---|---|---|---|
| Argo CD | Kubernetes RBAC + GitHub Actions | Apache-2.0 | https://github.com/argoproj/argo-cd |
| Tekton Pipelines | Kubernetes RBAC + GitHub Actions | Apache-2.0 | https://github.com/tektoncd/pipeline |
| Flux v2 | Kubernetes RBAC + GitHub Actions | Apache-2.0 | https://github.com/fluxcd/flux2 |
| Prometheus Operator | Kubernetes RBAC + GitHub Actions | Apache-2.0 | https://github.com/prometheus-operator/prometheus-operator |
| OPA Gatekeeper Library | Rego + Kubernetes admission policies | Apache-2.0 | https://github.com/open-policy-agent/gatekeeper-library |
| RBAC Police | Kubernetes RBAC + Rego | Apache-2.0 | https://github.com/PaloAltoNetworks/rbac-police |

When using public-source mode, cite the repositories and preserve license/provenance metadata. The extracted traces are not production telemetry. They are policy/configuration-structure-derived replay workloads.
