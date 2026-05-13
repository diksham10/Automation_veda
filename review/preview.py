"""
review/preview.py
Pre-submission review screen.

Displays a beautiful Rich table showing:
  - All parsed questions
  - Detected correct answer
  - Confidence badge (colour coded)
  - Needs-review flag

Then prompts: [EDIT FLAGGED]  [SKIP FLAGGED]  [PROCEED]
"""

from typing import Dict, Any, List
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.text import Text
from rich import box

console = Console()

_CONF_STYLE = {
    "HIGH":   ("✅", "bold green"),
    "MEDIUM": ("⚠️ ", "bold yellow"),
    "LOW":    ("⚠️ ", "bold yellow"),
    "NONE":   ("❌", "bold red"),
}


def show_review(exam_info: Dict, questions: List[Dict]) -> str:
    """
    Display the full review table.

    Returns user choice: 'edit' | 'skip' | 'proceed'
    """
    _print_header(exam_info, questions)
    _print_table(questions)
    return _prompt_action(questions)


def _print_header(exam_info: Dict, questions: List[Dict]):
    total       = len(questions)
    auto_det    = sum(1 for q in questions if q.get("confidence") in ("HIGH", "MEDIUM"))
    low_conf    = sum(1 for q in questions if q.get("confidence") == "LOW")
    needs_rev   = sum(1 for q in questions if q.get("needs_review"))

    header_text = (
        f"[bold white]Class:[/bold white] {exam_info.get('class','?')}  "
        f"[bold white]Subject:[/bold white] {exam_info.get('subject','?')}  "
        f"[bold white]Date:[/bold white] {exam_info.get('date','?')}\n"
        f"[bold white]Total:[/bold white] {total}  "
        f"[green]Ready:[/green] {auto_det}  "
        f"[yellow]Low Conf:[/yellow] {low_conf}  "
        f"[red]Review Needed:[/red] {needs_rev}"
    )
    console.print(Panel(header_text, title="[bold cyan]📋 PARSED QUESTIONS REVIEW[/bold cyan]",
                        border_style="cyan"))


def _print_table(questions: List[Dict]):
    table = Table(
        box=box.ROUNDED,
        show_header=True,
        header_style="bold white on dark_blue",
        border_style="blue",
        padding=(0, 1),
    )

    table.add_column("#",        style="dim",        width=4)
    table.add_column("Question", style="white",      no_wrap=False, max_width=50)
    table.add_column("Correct Answer", style="cyan", width=22)
    table.add_column("Conf",     justify="center",   width=8)
    table.add_column("Method",   style="dim",        width=16)

    for q in questions:
        icon, style = _CONF_STYLE.get(q.get("confidence", "NONE"), ("❓", "white"))

        q_num   = str(q.get("number", "?"))
        q_text  = (q.get("question_clean") or q.get("question_raw", ""))[:60]
        answer  = q.get("correct_text") or "[red]NOT DETECTED[/red]"
        conf    = f"[{style}]{icon} {q.get('confidence','?')}[/{style}]"
        method  = q.get("detection_method", "none")

        table.add_row(q_num, q_text, answer, conf, method)

    console.print(table)


def _prompt_action(questions: List[Dict]) -> str:
    flagged = [q for q in questions if q.get("needs_review")]

    console.print()
    if flagged:
        console.print(
            f"  [yellow]⚠️  {len(flagged)} question(s) need manual review.[/yellow]"
        )
        console.print(
            "  [bold]Options:[/bold]  "
            "[cyan][E][/cyan] Edit flagged  "
            "[yellow][S][/yellow] Skip flagged  "
            "[green][P][/green] Proceed with all"
        )
        while True:
            choice = console.input("  → Your choice (E/S/P): ").strip().lower()
            if choice in ('e', 's', 'p'):
                return {'e': 'edit', 's': 'skip', 'p': 'proceed'}[choice]
            console.print("  [red]Please enter E, S, or P.[/red]")
    else:
        console.print("  [green]✅ All questions auto-detected! Ready to submit.[/green]")
        console.input("  → Press Enter to start automation...")
        return 'proceed'
