from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Iterator, List, Optional
import json
import time

from .utils import is_subpath


@dataclass(frozen=True)
class Move:
    src: str
    dst: str


def journals_dir(root: Path) -> Path:
    return root / ".organizador" / "journals"


def write_journal(root: Path, moves: List[Move]) -> Path:
    d = journals_dir(root)
    d.mkdir(parents=True, exist_ok=True)
    stamp = time.strftime("%Y%m%d-%H%M%S")
    fp = d / f"journal-{stamp}.jsonl"
    with fp.open("w", encoding="utf-8") as f:
        for m in moves:
            f.write(json.dumps({"src": m.src, "dst": m.dst}, ensure_ascii=False) + "\n")
    return fp


def list_journals(root: Path) -> List[Path]:
    d = journals_dir(root)
    if not d.exists():
        return []
    return sorted(d.glob("journal-*.jsonl"))


def read_journal(path: Path) -> List[Move]:
    moves: List[Move] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        obj = json.loads(line)
        moves.append(Move(src=obj["src"], dst=obj["dst"]))
    return moves


def latest_journal(root: Path) -> Optional[Path]:
    js = list_journals(root)
    return js[-1] if js else None
