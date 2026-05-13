"""
review/manual_fix.py
Interactive CLI for manually fixing flagged questions.

For each needs_review question, shows the question + 4 options
and lets the teacher pick the correct one (i/ii/iii/iv).
"""

from typing import List, Dict
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import box

console = Console()

VALID_OPTIONS = ['i', 'ii', 'iii', 'iv']


def fix_flagged(questions: List[Dict]) -> List[Dict]:
    """
    Iterate over all needs_review questions and collect manual input.
    Mutates the question dicts in place, returns the updated list.
    """
    flagged = [q for q in questions if q.get("needs_review")]

    if not flagged:
        return questions

    console.rule("[bold yellow]🛠  Manual Review Mode[/bold yellow]")
    console.print(
        f"  [yellow]{len(flagged)} question(s) need your input.[/yellow]\n"
    )

    for idx, q in enumerate(flagged, 1):
        _show_question(q, idx, len(flagged))
        chosen_key = _get_user_choice(q)

        # Apply the fix
        q["correct_option"]   = chosen_key
        q["correct_text"]     = q["options"].get(chosen_key, "")
        q["detection_method"] = "manual"
        q["confidence"]       = "HIGH"
        q["needs_review"]     = False

        console.print(f"  [green]✔ Saved: {chosen_key}. {q['correct_text']}[/green]\n")

    console.rule("[green]✅ All flagged questions resolved[/green]")
    return questions


def _show_question(q: Dict, idx: int, total: int):
    q_text  = q.get("question_clean") or q.get("question_raw", "")
    options = q.get("options", {})

    opt_lines = "\n".join(
        f"  [cyan]{k}.[/cyan]  {options.get(k, '[dim]—[/dim]')}"
        for k in VALID_OPTIONS
    )

    console.print(Panel(
        f"[bold white]{q_text}[/bold white]\n\n{opt_lines}",
        title=f"[bold yellow]Q{q['number']}[/bold yellow]  [dim]({idx}/{total})[/dim]",
        border_style="yellow",
        padding=(1, 2),
    ))


def _get_user_choice(q: Dict) -> str:
    """Prompt until a valid option key is entered."""
    options = q.get("options", {})

    while True:
        raw = console.input(
            "  Enter correct option [cyan](i / ii / iii / iv)[/cyan]: "
        ).strip().lower()

        if raw in VALID_OPTIONS:
            if options.get(raw):
                return raw
            else:
                console.print(f"  [red]Option '{raw}' has no text. Try again.[/red]")
        else:
            console.print("  [red]Invalid. Please enter: i, ii, iii, or iv[/red]")
