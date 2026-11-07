#!/usr/bin/env python3
"""Assemble the public static site without repository-only files."""
from pathlib import Path
import shutil

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"

EXCLUDED_ROOT_DIRS = {"content", "docs", "reports", "scripts", ".vscode"}
EXCLUDED_ROOT_FILES = {
    ".gitignore",
    "netlify.toml",
    "PERFORMANCE_AUDIT_LTS_2026-11-03.md",
    "SEO_AUDIT_LASER_TECH_SERVICE.md",
}


def ignored_names(directory: str, names: list[str]) -> set[str]:
    relative = Path(directory).relative_to(ROOT)
    ignored = {
        name
        for name in names
        if name in {".git", ".DS_Store", "__pycache__"}
        or name.endswith((".pyc", ".pyo"))
    }

    if not relative.parts:
        ignored.update(EXCLUDED_ROOT_DIRS.intersection(names))
        ignored.update(EXCLUDED_ROOT_FILES.intersection(names))

    return ignored


def main() -> None:
    if DIST.is_symlink():
        raise RuntimeError(f"Refusing to replace symlink: {DIST}")
    if DIST.exists():
        shutil.rmtree(DIST)

    shutil.copytree(ROOT, DIST, ignore=ignored_names)
    print(f"Packaged public site in {DIST}")


if __name__ == "__main__":
    main()
