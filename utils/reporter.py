"""
utils/reporter.py
Builds and saves the final submission report after automation finishes.
"""

import os
from datetime import datetime


def build_report(exam_info: dict, results: list) -> str:
    """
    Build a text report from automation results.

    `results` is a list of dicts with keys:
        q_num, status ('ok'|'warn'|'fail'|'skip'), message, confidence
    """
    submitted   = [r for r in results if r['status'] == 'ok']
    warned      = [r for r in results if r['status'] == 'warn']
    failed      = [r for r in results if r['status'] == 'fail']
    skipped     = [r for r in results if r['status'] == 'skip']

    total = len(results)
    date_str = exam_info.get('date', datetime.now().strftime('%Y-%m-%d'))

    lines = [
        "",
        "═" * 45,
        "       DOCTOEXAM — SUBMISSION REPORT",
        "═" * 45,
        f"  Exam    : {exam_info.get('exam_name', 'N/A')}",
        f"  Class   : {exam_info.get('class', 'N/A')}",
        f"  Subject : {exam_info.get('subject', 'N/A')}",
        f"  Date    : {date_str}",
        "─" * 45,
        f"  Total Questions  : {total}",
        f"  ✅ Submitted      : {len(submitted)}",
        f"  ⚠️  Submitted*     : {len(warned)}  (low/medium confidence)",
        f"  ❌ Failed         : {len(failed)}",
        f"  ⏭️  Skipped        : {len(skipped)}",
        "─" * 45,
    ]

    if failed:
        lines.append("  Failed Questions:")
        for r in failed:
            lines.append(f"    Q{r['q_num']} — {r['message']}")

    if warned:
        lines.append("  Please manually verify:")
        for r in warned:
            lines.append(
                f"    Q{r['q_num']} — confidence: {r.get('confidence','?')}"
            )

    lines += [
        "─" * 45,
        f"  *Low/medium confidence answers were submitted",
        f"   but should be manually verified.",
        "═" * 45,
        "",
    ]

    return "\n".join(lines)


def save_report(report_text: str, date_str: str, output_dir: str = "output/reports") -> str:
    """
    Save report to output/reports/report_<date>.txt
    Returns the file path.
    """
    os.makedirs(output_dir, exist_ok=True)
    safe_date = date_str.replace('/', '-').replace('\\', '-')
    filename = f"report_{safe_date}.txt"
    filepath = os.path.join(output_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(report_text)

    return filepath
