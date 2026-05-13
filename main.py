"""
main.py — DocToExam Automation Tool (AI Powered)
Entry point that orchestrates the full pipeline:
"""

import os
import sys
import json
import time
import glob
from datetime import datetime

# ── Rich console for startup banner ─────────────────────────────────────────
from rich.console import Console
from rich.panel import Panel

console = Console()

# ── Internal modules ─────────────────────────────────────────────────────────
from parser.ai_parser       import parse_document_with_ai  
from utils.logger           import log_info, log_section, log_ok, log_warn, log_fail, make_progress_bar
from utils.reporter         import build_report, save_report
from review.preview         import show_review
from review.manual_fix      import fix_flagged
from automation.browser     import create_driver, login, navigate_to_add_question, quit_driver
from automation.form_filler import FormFiller
from automation.submitter   import submit_question

# ── Constants ────────────────────────────────────────────────────────────────
CONFIG_PATH       = "config.json"
PARSED_OUTPUT     = os.path.join("output", "parsed_data.json")

# ─────────────────────────────────────────────────────────────────────────────
def load_config() -> dict:
    if not os.path.exists(CONFIG_PATH):
        console.print(f"[red]❌  config.json not found. Please create it first.[/red]")
        sys.exit(1)
    with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
        return json.load(f)

def get_docx_from_input() -> str:
    input_dir = os.path.join(os.path.dirname(__file__), 'input')
    if not os.path.exists(input_dir):
        os.makedirs(input_dir)
        console.print(f"[cyan]📂  Created '{input_dir}' directory.[/cyan]")
        console.print("Please place your .docx file in the 'input' folder and run again.")
        return None
    
    docx_files = glob.glob(os.path.join(input_dir, '*.docx'))
    if not docx_files:
        console.print(f"[red]❌  No .docx files found in '{input_dir}'.[/red]")
        return None
    
    selected_file = docx_files[0]
    console.print(f"[cyan]📄  Found and using file: {selected_file}[/cyan]")
    return selected_file

def save_parsed_json(exam_info: dict, questions: list):
    os.makedirs("output", exist_ok=True)
    total        = len(questions)
    auto_det     = sum(1 for q in questions if q.get("confidence") in ("HIGH", "MEDIUM"))
    needs_review = sum(1 for q in questions if q.get("needs_review"))

    data = {
        "exam_info": exam_info,
        "summary": {
            "total_questions":  total,
            "auto_detected":    auto_det,
            "needs_review":     needs_review,
            "ready_to_submit":  auto_det,
        },
        "questions": questions,
    }

    with open(PARSED_OUTPUT, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    log_info(f"Parsed data saved → {PARSED_OUTPUT}")

def run_automation(exam_info: dict, questions: list, config: dict) -> list:
    log_section("Starting Browser Automation")
    driver = create_driver(config)
    results = []

    try:
        if not login(driver, config):
            console.print("[red]❌  Login failed. Check config.json credentials.[/red]")
            quit_driver(driver)
            sys.exit(1)

        navigate_to_add_question(driver, config)
        time.sleep(2)
        filler = FormFiller(driver, config)

        with make_progress_bar(len(questions)) as progress:
            task = progress.add_task("Submitting questions...", total=len(questions))

            for question in questions:
                q_num = question["number"]
                fill_ok = filler.fill_question(question, exam_info)

                if not fill_ok:
                    result = {
                        "q_num": q_num, "status": "fail", 
                        "message": "Form fill failed — skipping submit.",
                        "confidence": question.get("confidence", "NONE")
                    }
                else:
                    result = submit_question(driver, question, config)
                    # Safety net to ensure result is a dictionary
                    if isinstance(result, bool):
                        result = {"status": "ok" if result else "fail", "message": "Submitted"}

                results.append(result)

                if result.get("status") == "ok":
                    log_ok(q_num, result.get("message", "Success"))
                elif result.get("status") == "warn":
                    log_warn(q_num, result.get("message", "Warning"))
                else:
                    log_fail(q_num, result.get("message", "Failed"))

                progress.advance(task)

    finally:
        quit_driver(driver)

    return results

def show_final_report(exam_info: dict, results: list):
    log_section("Final Report")
    report_text = build_report(exam_info, results)
    console.print(report_text)
    date_str = exam_info.get("date", datetime.now().strftime("%Y-%m-%d"))
    filepath = save_report(report_text, date_str)
    console.print(f"  [dim]Report saved → {filepath}[/dim]\n")

# ─────────────────────────────────────────────────────────────────────────────
def main():
    console.print(Panel(
        "[bold cyan]DocToExam Automation Tool (AI Powered)[/bold cyan]\n"
        "[dim]Automated MCQ Upload System — v2.0[/dim]",
        border_style="cyan", padding=(1, 4),
    ))

    config = load_config()
    docx_path = get_docx_from_input()
    if not docx_path:
        sys.exit(0)

    # --- THE NEW AI PARSING PIPELINE ---
    log_section("Parsing Document with OpenAI")
    console.print("[dim]Sending document to ChatGPT for analysis... (takes 5-10 seconds)[/dim]")
    
    exam_info, questions = parse_document_with_ai(docx_path, config.get("defaults", {}))
    
    if not questions:
        console.print("[red]❌  Failed to parse document. Check API key or document text.[/red]")
        sys.exit(1)
        
    console.print(f"[green]✅  Successfully extracted {len(questions)} questions![/green]")
    save_parsed_json(exam_info, questions)

    # Review screen
    log_section("Pre-Submission Review")
    action = show_review(exam_info, questions)

    if action == 'edit':
        questions = fix_flagged(questions)
    elif action == 'skip':
        skipped = [q["number"] for q in questions if q.get("needs_review")]
        questions = [q for q in questions if not q.get("needs_review")]
        if skipped:
            console.print(f"  [yellow]Skipping {len(skipped)} flagged questions: {skipped}[/yellow]")

    if not questions:
        console.print("[red]No questions to submit.[/red]")
        sys.exit(0)

    # Automation
    results = run_automation(exam_info, questions, config)
    show_final_report(exam_info, results)

if __name__ == "__main__":
    main()