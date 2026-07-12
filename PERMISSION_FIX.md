# Shell-script invocation compatibility

The primary reproduction command is:

```bash
bash scripts/run_all.sh
```

The main script invokes nested shell scripts through `bash`, so reproduction does not depend on executable permission bits being preserved by a ZIP extractor. The repository also retains executable bits on `scripts/*.sh` for normal Git checkouts.
