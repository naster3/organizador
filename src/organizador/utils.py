from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re


def is_subpath(path: Path, base: Path) -> bool:
    """Return True if `path` is inside `base` (safe cross-platform check)."""
    try:
        path.resolve().relative_to(base.resolve())
        return True
    except Exception:
        return False


def sanitize_folder_name(name: str) -> str:
    # Remove characters invalid on Windows and keep it readable.
    name = name.strip()
    name = re.sub(r'[<>:"/\\|?*]+', "_", name)
    name = re.sub(r"\s+", " ", name)
    return name or "Other"


def unique_path(dest: Path) -> Path:
    """If dest exists, append ' (1)', ' (2)' ... before suffix."""
    if not dest.exists():
        return dest
    stem, suffix = dest.stem, dest.suffix
    parent = dest.parent
    i = 1
    while True:
        candidate = parent / f"{stem} ({i}){suffix}"
        if not candidate.exists():
            return candidate
        i += 1
