from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, List, Literal, Optional, Tuple
import os
import time

from .errors import InvalidPathError
from .journal import Move
from .rules import Rules
from .utils import sanitize_folder_name, unique_path, is_subpath


Mode = Literal["type", "date"]
GroupBy = Literal["year", "month"]


@dataclass(frozen=True)
class PlanItem:
    src: Path
    dst: Path


def iter_files(root: Path, recursive: bool) -> Iterable[Path]:
    if recursive:
        for p in root.rglob("*"):
            if p.is_file():
                yield p
    else:
        for p in root.iterdir():
            if p.is_file():
                yield p


def should_skip(path: Path, root: Path) -> bool:
    # Skip our own bookkeeping folder
    return is_subpath(path, root / ".organizador")


def plan_type(root: Path, rules: Rules, recursive: bool) -> List[PlanItem]:
    items: List[PlanItem] = []
    for f in iter_files(root, recursive=recursive):
        if should_skip(f, root):
            continue
        folder = sanitize_folder_name(rules.folder_for_extension(f.suffix.lower() or ""))
        dst_dir = root / folder
        dst = unique_path(dst_dir / f.name)
        items.append(PlanItem(src=f, dst=dst))
    return items


def plan_date(root: Path, group_by: GroupBy, recursive: bool) -> List[PlanItem]:
    items: List[PlanItem] = []
    for f in iter_files(root, recursive=recursive):
        if should_skip(f, root):
            continue
        st = f.stat()
        t = time.localtime(st.st_mtime)
        year = f"{t.tm_year:04d}"
        if group_by == "year":
            dst_dir = root / year
        else:
            month = f"{t.tm_mon:02d}"
            dst_dir = root / year / month
        dst = unique_path(dst_dir / f.name)
        items.append(PlanItem(src=f, dst=dst))
    return items


def build_plan(
    root: Path,
    mode: Mode,
    rules: Rules,
    group_by: GroupBy = "month",
    recursive: bool = False,
) -> List[PlanItem]:
    if not root.exists() or not root.is_dir():
        raise InvalidPathError(f"Ruta inválida: {root}")
    if mode == "type":
        return plan_type(root, rules, recursive=recursive)
    if mode == "date":
        return plan_date(root, group_by=group_by, recursive=recursive)
    raise ValueError(f"Modo inválido: {mode}")


def apply_plan(plan: List[PlanItem], dry_run: bool) -> List[Move]:
    moves: List[Move] = []
    for item in plan:
        if item.src == item.dst:
            continue
        if dry_run:
            moves.append(Move(src=str(item.src), dst=str(item.dst)))
            continue
        item.dst.parent.mkdir(parents=True, exist_ok=True)
        item.src.replace(item.dst)  # atomic move on same filesystem
        moves.append(Move(src=str(item.src), dst=str(item.dst)))
    return moves
