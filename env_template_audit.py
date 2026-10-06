"""Audit dotenv files against a committed template."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from dataclasses import asdict
import json
from pathlib import Path


@dataclass(frozen=True)
class AuditReport:
    """Differences found between a template and an environment file."""

    missing: tuple[str, ...]
    extra: tuple[str, ...]
    template_duplicates: tuple[str, ...]
    env_duplicates: tuple[str, ...]


def _scan(text: str) -> tuple[set[str], tuple[str, ...]]:
    keys: set[str] = set()
    duplicates: set[str] = set()
    for raw_line in text.splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        if line.startswith("export "):
            line = line[7:].lstrip()
        key = line.split("=", 1)[0].strip()
        if key:
            if key in keys:
                duplicates.add(key)
            keys.add(key)
    return keys, tuple(sorted(duplicates))


def audit_text(template_text: str, env_text: str) -> AuditReport:
    """Compare dotenv content and return a deterministic report."""

    template_keys, template_duplicates = _scan(template_text)
    env_keys, env_duplicates = _scan(env_text)
    return AuditReport(
        missing=tuple(sorted(template_keys - env_keys)),
        extra=tuple(sorted(env_keys - template_keys)),
        template_duplicates=template_duplicates,
        env_duplicates=env_duplicates,
    )


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        description="Compare dotenv key names without exposing their values."
    )
    parser.add_argument("template", type=Path, help="template file, such as .env.example")
    parser.add_argument("environment", type=Path, help="environment file to audit")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = parser.parse_args(argv)

    try:
        report = audit_text(
            args.template.read_text(encoding="utf-8"),
            args.environment.read_text(encoding="utf-8"),
        )
    except OSError as error:
        parser.error(str(error))

    result = asdict(report)
    if args.json:
        print(json.dumps(result, sort_keys=True))
    else:
        for label, keys in result.items():
            print(f"{label}: {', '.join(keys) if keys else '-'}")

    return 1 if any(result.values()) else 0


if __name__ == "__main__":
    raise SystemExit(main())
