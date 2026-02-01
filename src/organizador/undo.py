from __future__ import annotations

from pathlib import Path
from typing import List

from .errors import NothingToUndoError
from .journal import Move, latest_journal, read_journal
from .utils import unique_path


def undo_last(root: Path, dry_run: bool = False) -> List[Move]:
    j = latest_journal(root)
    if j is None:
        raise NothingToUndoError("No hay journals para deshacer en esa carpeta.")
    moves = read_journal(j)
    # Reverse: dst -> src
    reverted: List[Move] = []
    for m in reversed(moves):
        dst = Path(m.dst)
        src = Path(m.src)
        if not dst.exists():
            # If file was deleted/moved after the run, skip.
            continue
        final_src = unique_path(src)
        if dry_run:
            reverted.append(Move(src=str(dst), dst=str(final_src)))
            continue
        final_src.parent.mkdir(parents=True, exist_ok=True)
        dst.replace(final_src)
        reverted.append(Move(src=str(dst), dst=str(final_src)))
    return reverted
