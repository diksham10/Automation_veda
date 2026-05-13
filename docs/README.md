# DocToExam — Automated MCQ Upload Tool
### Version 1.0

---

## What This Tool Does

Reads your MCQ Word document → detects correct answers automatically → fills the exam portal form for every question automatically.

---

## Quick Start

```bash
# 1. Open terminal in this folder
cd /path/to/doctoexam

# 2. Run the launcher (creates venv + installs deps automatically)
bash run.sh
```

Then follow the on-screen prompts.

---

## First-Time Setup (Required)

### Step 1 — Edit `config.json`

Open `config.json` and fill in your details:

```json
{
  "website": {
    "url":       "https://YOUR_PORTAL/add-question",
    "login_url": "https://YOUR_PORTAL/login",
    "username":  "your_email@school.com",
    "password":  "your_password"
  }
}
```

### Step 2 — Edit `automation/selectors.py`  ⚠️ IMPORTANT

This file tells the tool **where each field is** on your exam portal.
You must update the CSS selectors to match your actual website.

**How to find selectors:**
1. Open your portal in Chrome
2. Press `F12` to open DevTools
3. Click the arrow/cursor icon (top-left of DevTools)
4. Click the field you want (e.g., the Class dropdown)
5. Look at the highlighted HTML — find the `id=` or `name=` attribute
6. Paste it into `selectors.py`

**Example:**
```
If the page shows:   <select id="class_select">
Then set:            CLASS_DROPDOWN = "#class_select"
```

**Fields to update in `selectors.py`:**

| Variable | What it maps to |
|---|---|
| `USERNAME_FIELD` | Login username input |
| `PASSWORD_FIELD` | Login password input |
| `LOGIN_BUTTON` | Login submit button |
| `EXAM_NAME_DROPDOWN` | Exam Name `<select>` |
| `CLASS_DROPDOWN` | Class `<select>` |
| `SUBJECT_DROPDOWN` | Subject `<select>` |
| `YEAR_DROPDOWN` | Year `<select>` |
| `CHAPTER_DROPDOWN` | Chapter `<select>` |
| `EXAM_DETAIL_DROPDOWN` | Exam Detail `<select>` |
| `CATEGORY_DROPDOWN` | Category `<select>` |
| `TYPE_DROPDOWN` | Type `<select>` |
| `QUESTION_TYPE_TEXT_RADIO` | "Text" radio button |
| `TINYMCE_TEXTAREA_ID` | TinyMCE textarea `id` |
| `ANSWER_1_FIELD` … `ANSWER_4_FIELD` | Answer input fields |
| `POINTS_FIELD` | Points/marks input |
| `CORRECT_TOGGLE_1` … `CORRECT_TOGGLE_4` | Correct-answer checkboxes |
| `SUBMIT_BUTTON` | Form submit button |
| `SUCCESS_INDICATOR` | Element shown after success |

---

## Document Format

Your Word file should follow this structure:

```
Class 8 Grammar MCQ(083-01-26Saturday)
Tick the correct answer from the given alternatives:

1. The sentence 'Why is she dancing' is an example of ......... sentence.
i. assertive  ii.✓interrogative  iii. imperative  iv. exclamatory

2. "Ouch! my leg is paining" expresses.....
I. order  ii. blessing  iii.✓sudden emotion  iv. curse
```

**Correct answer markers supported:**
- ✓ tick symbols anywhere near the option
- **Bold** or <u>underlined</u> option text
- Coloured text (non-black)
- `(brackets)` around the option text
- ALL CAPS option (low confidence)

---

## Output Files

| File | Description |
|---|---|
| `output/parsed_data.json` | All parsed questions in JSON |
| `output/reports/report_DATE.txt` | Submission report |
| `output/screenshots/qN.png` | Screenshot after each submit |

---

## Troubleshooting

| Problem | Fix |
|---|---|
| Login fails | Check `config.json` credentials + `LOGIN_BUTTON` selector |
| Dropdown not found | Update the matching selector in `selectors.py` |
| TinyMCE not filling | Check `TINYMCE_TEXTAREA_ID` matches the `<textarea>` id |
| Correct answer toggle not working | Inspect the checkbox element, update `CORRECT_TOGGLE_*` |
| Questions not parsed | Check your doc follows the format above |

---

## Tech Stack

`python-docx` · `selenium` · `webdriver-manager` · `rich` · `colorama`

ChromeDriver is downloaded automatically — no manual installation needed.
