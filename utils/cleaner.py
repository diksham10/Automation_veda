"""
utils/cleaner.py
Cleans raw parsed text — removes filler dots, normalises whitespace,
strips option labels so only the answer text remains.
"""

import re


# ─── Filler dot patterns ────────────────────────────────────────────────────
# Matches sequences of 2+ dots with optional spaces between them
_FILLER_DOT_RE = re.compile(r'\.{2,}|\. \.+')


def remove_filler_dots(text: str) -> str:
    """Instead of removing, we preserve dots for fill-in-the-blank questions."""
    # We no longer wipe out dots because examination papers often use them for blanks.
    # Just normalize spaces instead.
    return normalise_spaces(text)


def normalise_spaces(text: str) -> str:
    """Collapse multiple whitespace characters into one and strip ends."""
    return re.sub(r'\s+', ' ', text).strip()


def clean_question_text(raw: str) -> str:
    """
    Full cleaning pipeline for a question text:
      1. Remove filler dots
      2. Normalise spaces
      3. Strip trailing punctuation artifacts
    """
    text = remove_filler_dots(raw)
    # Remove lone dots/dashes at the very end that look like artifacts
    text = re.sub(r'[\s.]+$', '', text).strip()
    return text


def clean_option_text(raw: str) -> str:
    """
    Clean an individual option text:
      1. Strip any leading roman-numeral label if still attached
         e.g.  "ii. sudden emotion" → "sudden emotion"
      2. Remove filler dots
      3. Normalise spaces
    """
    # Remove leading roman numeral + separator  (i. / ii) / III. / iv) etc.)
    text = re.sub(
        r'^[ivxIVX]{1,4}[\.\)]\s*',
        '',
        raw.strip()
    )
    # Remove common answer-marker symbols left in text
    SYMBOLS = r'[✓✔☑√★✱\*►▶→=>\(\)\[\]\{\}"#@!~©®◉●]'
    text = re.sub(SYMBOLS, '', text)
    text = remove_filler_dots(text)
    return normalise_spaces(text)


def strip_answer_markers(text: str) -> str:
    """
    Remove tick / star / arrow marker symbols from a string.
    Used when extracting the option text that contains the marker.
    """
    MARKER_RE = re.compile(
        r'[✓✔☑√★✱►▶→\*#@!~]'
    )
    return normalise_spaces(MARKER_RE.sub('', text))
