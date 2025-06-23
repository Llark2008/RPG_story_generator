#!/usr/bin/env python
"""Validate that generated JSON schemas are committed."""
import subprocess
from pathlib import Path


def main() -> int:
    # Importing rpggen.models will regenerate schema files in-place
    import rpggen.models  # noqa: F401

    repo = Path(__file__).resolve().parents[1]
    schema_dir = repo / "core" / "rpggen" / "models"
    schema_files = sorted(schema_dir.glob("*.schema.json"))

    if not schema_files:
        print("No schema files found", flush=True)
        return 0

    result = subprocess.run(["git", "diff", "--name-only", "--exit-code", "--"] + [str(f) for f in schema_files])
    if result.returncode != 0:
        print("Schema files are out of date. Run tests to regenerate and commit them.", flush=True)
        return result.returncode
    print("Schemas up to date.")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
