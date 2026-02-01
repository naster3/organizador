from __future__ import annotations

from pathlib import Path
from typing import Optional, Literal

import typer
from rich.console import Console
from rich.table import Table

from .errors import OrganizadorError, InvalidPathError, NothingToUndoError
from .journal import write_journal
from .organize import build_plan, apply_plan
from .rules import Rules
from .undo import undo_last

app = typer.Typer(add_completion=False, help="Organiza una carpeta por tipo o fecha, con dry-run y undo.")
console = Console()

Mode = Literal["type", "date"]
GroupBy = Literal["year", "month"]


def _print_moves(title: str, moves: list[tuple[str, str]]) -> None:
    table = Table(title=title, show_header=True, header_style="bold")
    table.add_column("Desde", overflow="fold")
    table.add_column("Hacia", overflow="fold")
    for a, b in moves:
        table.add_row(a, b)
    console.print(table)


@app.command()
def run(
    path: Path = typer.Argument(..., exists=False, help="Carpeta objetivo (ej: Downloads)."),
    mode: Mode = typer.Option("type", "--mode", help="type=por extensión, date=por fecha."),
    group_by: GroupBy = typer.Option("month", "--group-by", help="Solo para mode=date."),
    rules: Optional[Path] = typer.Option(None, "--rules", help="JSON con reglas personalizadas."),
    recursive: bool = typer.Option(False, "--recursive", help="Incluye subcarpetas."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simula: no mueve nada."),
) -> None:
    """Organiza una carpeta."""
    try:
        root = path.expanduser()
        r = Rules.load(rules)
        plan = build_plan(root=root, mode=mode, rules=r, group_by=group_by, recursive=recursive)

        # For display, only show the real changes (avoid src==dst)
        preview = [(str(p.src), str(p.dst)) for p in plan if p.src != p.dst]
        if not preview:
            console.print("[yellow]Nada que mover. Todo está ya organizado (o no hay archivos).[/yellow]")
            raise typer.Exit(code=0)

        _print_moves("Plan de movimientos" + (" (dry-run)" if dry_run else ""), preview)

        moves = apply_plan(plan, dry_run=dry_run)
        if dry_run:
            console.print(f"[cyan]Dry-run:[/cyan] {len(moves)} movimientos planeados.")
            raise typer.Exit(code=0)

        journal_path = write_journal(root, moves)
        console.print(f"[green]Listo:[/green] {len(moves)} archivos movidos.")
        console.print(f"Journal: {journal_path}")

    except typer.Exit:
        raise
    except (InvalidPathError,) as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=2)
    except Exception as e:
        console.print(f"[red]Error inesperado:[/red] {e}")
        raise typer.Exit(code=1)


@app.command()
def undo(
    path: Path = typer.Argument(..., exists=False, help="Carpeta donde se creó el journal."),
    dry_run: bool = typer.Option(False, "--dry-run", help="Simula el undo (no mueve nada)."),
) -> None:
    """Deshace la última corrida en esa carpeta usando el journal más reciente."""
    try:
        root = path.expanduser()
        reverted = undo_last(root, dry_run=dry_run)
        if not reverted:
            console.print("[yellow]No se pudo revertir nada (archivos ya no estaban donde el journal decía).[/yellow]")
            raise typer.Exit(code=0)

        _print_moves("Undo" + (" (dry-run)" if dry_run else ""), [(m.src, m.dst) for m in reverted])

        if dry_run:
            console.print(f"[cyan]Dry-run:[/cyan] {len(reverted)} reversiones planeadas.")
        else:
            console.print(f"[green]Undo listo:[/green] {len(reverted)} archivos regresados.")

    except NothingToUndoError as e:
        console.print(f"[yellow]{e}[/yellow]")
        raise typer.Exit(code=0)
    except Exception as e:
        console.print(f"[red]Error:[/red] {e}")
        raise typer.Exit(code=1)


@app.command()
def watch(
    path: Path = typer.Argument(..., exists=False, help="Carpeta a monitorear."),
    mode: Mode = typer.Option("type", "--mode"),
    group_by: GroupBy = typer.Option("month", "--group-by"),
    rules: Optional[Path] = typer.Option(None, "--rules"),
    recursive: bool = typer.Option(False, "--recursive"),
    dry_run: bool = typer.Option(False, "--dry-run"),
) -> None:
    """Monitorea una carpeta y organiza cuando entren archivos nuevos.

    Nota: hace un 'run' completo cada vez que detecta cambios. Simple pero efectivo.
    """
    from watchdog.events import FileSystemEventHandler
    from watchdog.observers import Observer
    import time

    root = path.expanduser()
    r = Rules.load(rules)

    class Handler(FileSystemEventHandler):
        def on_created(self, event):
            if event.is_directory:
                return
            try:
                plan = build_plan(root=root, mode=mode, rules=r, group_by=group_by, recursive=recursive)
                moves = apply_plan(plan, dry_run=dry_run)
                if (not dry_run) and moves:
                    write_journal(root, moves)
                if moves:
                    console.print(f"[green]watch:[/green] {len(moves)} archivos organizados.")
            except Exception as e:
                console.print(f"[red]watch error:[/red] {e}")

    console.print(f"[cyan]Vigilando:[/cyan] {root}  (Ctrl+C para salir)")
    observer = Observer()
    observer.schedule(Handler(), str(root), recursive=recursive)
    observer.start()
    try:
        while True:
            time.sleep(0.5)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
