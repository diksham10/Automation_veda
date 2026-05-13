import logging
from automation import selectors

log = logging.getLogger("doctoexam")

def set_tinymce_content(driver_wrapper, html_content: str) -> bool:
    """Injects content into TinyMCE editor using Playwright safely."""
    page = driver_wrapper.page
    
    # We pass html_content as an argument to avoid quote-escaping issues
    clean_html = str(html_content).replace('\n', '<br>')
    
    try:
        # Pass the JS as an arrow function, passing clean_html as the 'html' variable
        js_code = """(html) => {
            if (typeof tinymce !== 'undefined' && tinymce.activeEditor) {
                tinymce.activeEditor.setContent(html);
                return true;
            }
            return false;
        }"""
        
        # Evaluate the script in the browser
        success = page.evaluate(js_code, clean_html)
        if success:
            return True
            
        # Fallback: if TinyMCE API fails, type directly into the iframe
        if selectors.TINYMCE_IFRAME_SELECTOR:
            frame = page.frame_locator(selectors.TINYMCE_IFRAME_SELECTOR).first
            frame.locator("body").fill(clean_html)
            return True
            
    except Exception as e:
        log.warning(f"TinyMCE Playwright injection failed: {e}")
        
    return False