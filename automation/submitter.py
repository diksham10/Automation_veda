import logging
from automation import selectors

log = logging.getLogger("doctoexam")

def submit_question(driver_wrapper, question: dict, config: dict) -> dict:
    """Clicks the submit button and waits to see what happens."""
    page = driver_wrapper.page
    
    try:
        # 1. CRITICAL FIX: Force TinyMCE to sync its text to the hidden HTML form
        try:
            page.evaluate("if (typeof tinymce !== 'undefined') { tinymce.triggerSave(); }")
        except Exception:
            pass

        # 2. Click the submit button
        submit_btn = page.locator(selectors.SUBMIT_BUTTON).first
        submit_btn.click(force=True)
        
        # 3. Wait 4 seconds so you can watch the screen. 
        # See if a red error message pops up, or if a green success toast appears!
        page.wait_for_timeout(4000)
        
        # (I have temporarily removed the page.reload() RAM flush just in case 
        # it was cancelling the upload request).
        
        return {"status": "ok", "message": "Submitted successfully"}
        
    except Exception as e:
        log.error(f"Failed to submit Q{question.get('number', '?')}: {e}")
        return {"status": "error", "message": str(e)}