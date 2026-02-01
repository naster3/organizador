from pathlib import Path
import json

from organizador.organize import build_plan, apply_plan
from organizador.rules import Rules
from organizador.undo import undo_last
from organizador.journal import write_journal


def touch(p: Path, content: str = "x") -> None:
    p.write_text(content, encoding="utf-8")


def test_type_organize_and_undo(tmp_path: Path):
    root = tmp_path
    touch(root / "a.jpg")
    touch(root / "b.pdf")
    touch(root / "c.unknownext")

    rules = Rules.load(None)
    plan = build_plan(root, mode="type", rules=rules, group_by="month", recursive=False)
    moves = apply_plan(plan, dry_run=False)

    assert (root / "Images" / "a.jpg").exists()
    assert (root / "Documents" / "b.pdf").exists()
    assert (root / "Other" / "c.unknownext").exists()

    journal = write_journal(root, moves)
    assert journal.exists()

    reverted = undo_last(root, dry_run=False)
    # Now originals should be back at root (or with unique suffix if collision)
    assert (root / "a.jpg").exists()
    assert (root / "b.pdf").exists()
    assert (root / "c.unknownext").exists()


def test_custom_rules(tmp_path: Path):
    root = tmp_path
    touch(root / "x.zzz")

    rules_json = root / "rules.json"
    rules_json.write_text(json.dumps({"Weird": [".zzz"]}), encoding="utf-8")

    rules = Rules.load(rules_json)
    plan = build_plan(root, mode="type", rules=rules, group_by="month", recursive=False)
    apply_plan(plan, dry_run=False)
    assert (root / "Weird" / "x.zzz").exists()
