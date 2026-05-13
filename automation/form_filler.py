import logging
from automation import selectors
from automation.tinymce_handler import set_tinymce_content

log = logging.getLogger("doctoexam")
OPTION_KEYS = ['i', 'ii', 'iii', 'iv']

class FormFiller:
    def __init__(self, driver, config: dict):
        self.driver = driver
        self.page = driver.page 
        self.config = config
        self.defaults = config.get("defaults", {})
        self._prev_dropdowns: dict = {}

    def fill_question(self, question: dict, exam_info: dict) -> bool:
        try:
            self._fill_dropdowns(exam_info)
            self._click_text_radio()
            
            q_text = question.get("question_clean") or question.get("question_raw", "")
            if not set_tinymce_content(self.driver, q_text):
                log.warning(f"Q{question.get('number', '?')}: TinyMCE fill failed.")

            self._fill_points(question.get("points", self.defaults.get("points", 5)))
            self._fill_answers(question.get("options", {}))

            correct_key = question.get("correct_option")
            if correct_key:
                self._set_correct_toggle(correct_key)
            else:
                log.warning(f"Q{question.get('number', '?')}: No correct answer set.")
            return True
        except Exception as e:
            log.error(f"Q{question.get('number', '?')}: form fill error — {e}")
            return False

    def _fill_dropdowns(self, exam_info: dict):
        mapping = {
            selectors.EXAM_NAME_DROPDOWN:   exam_info.get("exam_name",   self.defaults.get("exam_name", "")),
            selectors.CLASS_DROPDOWN:       exam_info.get("class",        ""),
            selectors.SUBJECT_DROPDOWN:     exam_info.get("subject",      ""),
            selectors.YEAR_DROPDOWN:        exam_info.get("year",         self.defaults.get("year", "")),
            selectors.CHAPTER_DROPDOWN:     exam_info.get("chapter",      ""),
            selectors.EXAM_DETAIL_DROPDOWN: exam_info.get("exam_detail",  self.defaults.get("exam_detail", "")),
            selectors.CATEGORY_DROPDOWN:    exam_info.get("category",     self.defaults.get("category", "")),
            selectors.TYPE_DROPDOWN:        self.defaults.get("type", "Objective"),
        }
        for selector, value in mapping.items():
            if not value or self._prev_dropdowns.get(selector) == value:
                continue
            self._select_dropdown(selector, value)
            self._prev_dropdowns[selector] = value

            self.page.wait_for_timeout(1000)

    def _select_dropdown(self, css_selector: str, value: str):
        try:
            # Added .first to avoid strict mode violations
            locator = self.page.locator(css_selector).first
            try:
                locator.select_option(label=str(value), timeout=2000)
            except Exception:
                locator.select_option(value=str(value), timeout=2000)
        except Exception as e:
            log.warning(f"Dropdown '{css_selector}' — could not select '{value}': {e}")

    def _click_text_radio(self):
        try:
            # We must use a more specific selector because your page has hidden elements
            radio = self.page.locator(f"#learning-question-answer-form {selectors.QUESTION_TYPE_TEXT_RADIO}").first
            if not radio.is_checked():
                radio.click(force=True)
        except Exception as e:
            pass # Ignore silently, usually it's already selected

    def _fill_points(self, points):
        try:
            self.page.locator(selectors.POINTS_FIELD).first.fill(str(points))
        except Exception as e:
            log.warning(f"Points fill error: {e}")

    def _fill_answers(self, options: dict):
        for key in OPTION_KEYS:
            field_selector = selectors.ANSWER_FIELD_MAP.get(key)
            if field_selector and options.get(key, ""):
                try:
                    self.page.locator(field_selector).first.fill(str(options.get(key, "")))
                except Exception as e:
                    log.warning(f"Answer field '{field_selector}' error: {e}")

    def _set_correct_toggle(self, correct_key: str):
        for key in OPTION_KEYS:
            toggle_label_selector = selectors.CORRECT_TOGGLE_MAP.get(key)
            if not toggle_label_selector: continue

            try:
                label_locator = self.page.locator(toggle_label_selector).first
                input_id = label_locator.get_attribute("for")
                
                is_checked = self.page.locator(f"#{input_id}").first.is_checked()

                if key == correct_key:
                    if not is_checked:
                        label_locator.click(force=True)
                        self.page.wait_for_timeout(100)
                else:
                    if is_checked:
                        label_locator.click(force=True)
                        self.page.wait_for_timeout(100)
            except Exception as e:
                log.warning(f"Toggle error on {toggle_label_selector}: {e}")