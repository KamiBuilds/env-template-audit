# Env Template Audit

`env-template-audit` compares the **key names** in a dotenv template and an environment file. It reports missing keys, unexpected keys, and duplicate definitions without printing secret values.

It is useful in CI, deployment preflight checks, and local development when `.env.example` drifts away from `.env`.

## Download and install

Clone the repository on Linux, macOS, or Windows:

```bash
git clone https://github.com/KamiBuilds/env-template-audit.git
cd env-template-audit
```

No package installation is required. On Linux/macOS, use `python3`; on Windows PowerShell, replace `python3` with `py` in the commands below.

## Requirements

- Python 3.11 or newer
- No third-party runtime dependencies

## Run

Audit the included drift example:

```bash
python3 env_template_audit.py examples/.env.example examples/drift.env
```

The command exits with `1` when drift or duplicates are found and `0` when the files agree. File/read and argument errors exit with `2`.

Machine-readable output:

```bash
python3 env_template_audit.py examples/.env.example examples/drift.env --json
```

A clean audit:

```bash
python3 env_template_audit.py examples/.env.example examples/clean.env
```

The parser supports blank lines, comments, ordinary `KEY=value` assignments, and `export KEY=value` assignments. Values are never included in reports.

## Test and verify

Run the complete test suite:

```bash
python3 -m unittest discover -s tests -v
```

Compile-check the project:

```bash
python3 -m compileall -q env_template_audit.py tests
```

## Example JSON

```json
{"env_duplicates": [], "extra": ["DEBUG"], "missing": ["REGION"], "template_duplicates": []}
```

## CI use

Because drift produces a non-zero status, the command can be used directly in a CI step:

```yaml
- name: Check dotenv contract
  run: python3 env_template_audit.py .env.example .env.ci
```

Never commit a real `.env` file. This repository's `.gitignore` excludes it by default.

## License

MIT
