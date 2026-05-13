"""
utils/logger.py
Coloured terminal output with progress bar.
Uses `rich` for beautiful formatting.
"""

import logging
import sys
from datetime import datetime
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, TimeElapsedColumn
from rich.theme import Theme
from rich.text import Text

# ─── Shared console ─────────────────────────────────────────────────────────
_THEME = Theme({
    "ok":      "bold green",
    "warn":    "bold yellow",
    "fail":    "bold red",
    "info":    "cyan",
    "header":  "bold white",
    "dim":     "dim white",
})

console = Console(theme=_THEME)

# ─── Standard Python logger (file logging) ──────────────────────────────────
_file_logger = logging.getLogger("doctoexam")
_file_logger.setLevel(logging.DEBUG)

_handler = logging.StreamHandler(sys.stdout)
_handler.setFormatter(
    logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
)
_file_logger.addHandler(_handler)


# ─── Helper log functions ────────────────────────────────────────────────────

def log_ok(q_num: int, message: str):
    """Green ✅ line for successfully submitted questions."""
    console.print(f"  [ok]✅ Q{q_num}[/ok] [dim]→[/dim] {message}")
    _file_logger.info(f"Q{q_num} OK: {message}")


def log_warn(q_num: int, message: str):
    """Yellow ⚠️ line for low-confidence or uncertain submissions."""
    console.print(f"  [warn]⚠️  Q{q_num}[/warn] [dim]→[/dim] {message}")
    _file_logger.warning(f"Q{q_num} WARN: {message}")


def log_fail(q_num: int, message: str):
    """Red ❌ line for failed submissions."""
    console.print(f"  [fail]❌ Q{q_num}[/fail] [dim]→[/dim] {message}")
    _file_logger.error(f"Q{q_num} FAIL: {message}")


def log_info(message: str):
    """Cyan info line."""
    console.print(f"  [info]ℹ[/info]  {message}")
    _file_logger.info(message)


def log_section(title: str):
    """Print a bold section separator."""
    console.rule(f"[header]{title}[/header]")


def make_progress_bar(total: int) -> Progress:
    """
    Returns a Rich Progress object.
    Usage:
        with make_progress_bar(20) as progress:
            task = progress.add_task("Submitting...", total=20)
            progress.advance(task)
    """
    return Progress(
        TextColumn("[bold cyan]{task.description}[/bold cyan]"),
        BarColumn(bar_width=30),
        TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        TextColumn("•"),
        TextColumn("{task.completed}/{task.total}"),
        TimeElapsedColumn(),
        console=console,
        transient=False,
    )
