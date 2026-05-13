"""
automation/selectors.py
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
⚠️  USER ACTION REQUIRED — Edit this file before first run
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Open your exam portal's "Add Question" page in Chrome.
Right-click each element → Inspect → copy its id, name,
or CSS selector and paste below.

HOW TO FIND A SELECTOR:
  1. Open DevTools (F12)
  2. Click the element picker (top-left arrow icon)
  3. Click the element on the page
  4. In the Elements panel, right-click the highlighted tag
     → Copy → Copy selector  (or note the id="..." attribute)
  5. Paste it into the corresponding variable below.

Example:
  If the page has  <select id="class_select"> ...
  set:  CLASS_DROPDOWN = "#class_select"
"""


# ── LOGIN PAGE ───────────────────────────────────────────────────────────────
# ⚠️ UPDATE: CSS selector for the username input field
USERNAME_FIELD = "input[name='email']"           # e.g.  input[name="username"]

# ⚠️ UPDATE: CSS selector for the password input field
PASSWORD_FIELD = "#password"           # e.g.  input[name="password"]

# ⚠️ UPDATE: CSS selector for the login/submit button
LOGIN_BUTTON = "button[type='submit']"

# ── DROPDOWN FIELDS (standard HTML <select>) ─────────────────────────────────
# ⚠️ UPDATE each selector to match your portal's <select> elements

EXAM_NAME_DROPDOWN   = "#exam-id"    # "MCQ Mastery (Multiple Choice)"
CLASS_DROPDOWN       = "#exam-question-class"        # "8", "9", etc.
SUBJECT_DROPDOWN     = "#exam-question-subject"      # "English", "Math", etc.
YEAR_DROPDOWN        = "#exam-year"         # "ACADEMIC-YEAR-2083"
CHAPTER_DROPDOWN     = "#exam-question-chapter"      # "Grammar", "Algebra", etc.
EXAM_DETAIL_DROPDOWN = "#exam-question-exam-detail"  # "Exam 1", "Exam 2", etc.
CATEGORY_DROPDOWN    = "#exam-question-category"     # "Basic Academics"
TYPE_DROPDOWN        = "#exam-question-type"         # "Objective"


# ── QUESTION TITLE TYPE RADIO ────────────────────────────────────────────────
# ⚠️ UPDATE: selector for the "Text" radio button (question title type)
QUESTION_TYPE_TEXT_RADIO = "input.question-type[type='radio']"


# ── TINYMCE EDITOR ───────────────────────────────────────────────────────────
# ⚠️ UPDATE if your TinyMCE has a specific ID.
# Leave as None to let the code auto-detect the iframe.
TINYMCE_IFRAME_SELECTOR = "#exam-question-title_ifr"
TINYMCE_TEXTAREA_ID     = "exam-question-title"


# ── ANSWER OPTION FIELDS (text inputs for each choice) ──────────────────────
# ⚠️ UPDATE: CSS selectors for the 4 answer text input boxes
ANSWER_1_FIELD = "#as"
ANSWER_2_FIELD = "#asd"
ANSWER_3_FIELD = "#asdf"
ANSWER_4_FIELD = "#asdfgh"


# ── POINTS FIELD ─────────────────────────────────────────────────────────────
# ⚠️ UPDATE: CSS selector for the points/marks input field
POINTS_FIELD = "#exam-question-point"


# ── CORRECT ANSWER TOGGLES (checkbox-switch) ────────────────────────────────
# We use the label because the actual radio button is often hidden by styling
CORRECT_TOGGLE_1 = "label[for='ch1']"
CORRECT_TOGGLE_2 = "label[for='ch2']"
CORRECT_TOGGLE_3 = "label[for='ch3']"
CORRECT_TOGGLE_4 = "label[for='ch4']"

CORRECT_TOGGLE_MAP = {
    "i":   CORRECT_TOGGLE_1,
    "ii":  CORRECT_TOGGLE_2,
    "iii": CORRECT_TOGGLE_3,
    "iv":  CORRECT_TOGGLE_4,
}

ANSWER_FIELD_MAP = {
    "i":   ANSWER_1_FIELD,
    "ii":  ANSWER_2_FIELD,
    "iii": ANSWER_3_FIELD,
    "iv":  ANSWER_4_FIELD,
}


# ── SUBMIT BUTTON ─────────────────────────────────────────────────────────────
# ⚠️ UPDATE: CSS selector for the form submit button
SUBMIT_BUTTON = "#submit-btn"
# ⚠️ UPDATE: CSS selector or text that appears after SUCCESSFUL submission
# e.g. a success toast, redirect URL fragment, or confirmation element
SUCCESS_INDICATOR = ".alert-success"   # e.g. div.success-message
