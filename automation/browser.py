"""
automation/browser.py
Playwright browser setup and login flow.
"""

import time
import os
import pickle
import logging
from automation.playwright_wrapper import PwWrapper
from automation import selectors
from dotenv import load_dotenv

load_dotenv()

log = logging.getLogger("doctoexam")

def create_driver(config: dict) -> PwWrapper:
    """
    Create and return a Playwright wrapper instance.
    """
    return PwWrapper(config)

def login(driver: PwWrapper, config: dict) -> bool:
    """
    Navigate to the login page and authenticate using Playwright.
    """
    web_cfg  = config.get("website", {})
    login_url = web_cfg.get("login_url") or web_cfg.get("url", "")

    page = driver.page

    log.info(f"Navigating to login page: {login_url}")
    page.goto(login_url)

    # ── Attempt to load saved session cookies to bypass login entirely ──
    cookies_file = os.path.join(os.path.dirname(__file__), "..", "cookies.pkl")
    if os.path.exists(cookies_file):
        try:
            with open(cookies_file, "rb") as f:
                cookies = pickle.load(f)
                driver.context.add_cookies(cookies)
            page.reload()
            page.wait_for_timeout(2000)
            # If the username field is no longer there, we successfully bypassed login!
            if not page.locator(selectors.USERNAME_FIELD).count():
                log.info("Successfully skipped login using saved session cookies!")
                return True
        except Exception as e:
            log.warning(f"Failed to load cookies: {e}")

    try:
        # ⚠️ THE FIX IS HERE: We added .first to avoid the strict mode crash!
        page.locator(selectors.USERNAME_FIELD).first.wait_for(state="visible", timeout=15000)
        page.locator(selectors.USERNAME_FIELD).first.fill(os.getenv("USERNAME", ""))

        # Fill password
        page.locator(selectors.PASSWORD_FIELD).first.fill(os.getenv("PASSWORD", ""))

        # Click login
        page.locator(selectors.LOGIN_BUTTON).first.click()

        # Wait for navigation
        page.wait_for_timeout(4000)

        log.info("Login submitted successfully.")
        
        # ── Save the session cookies ──
        try:
            with open(cookies_file, "wb") as f:
                pickle.dump(driver.context.cookies(), f)
            log.info("Saved browser session cookies.")
        except Exception as e:
            log.warning(f"Failed to save cookies: {e}")

        return True

    except Exception as e:
        log.error(f"Login failed: {e}")
        return False

def navigate_to_add_question(driver: PwWrapper, config: dict):
    page = driver.page
    current_url = page.url
    
    if "?token=" in current_url:
        token_part = current_url.split("?token=")[1].split("#")[0]
        target_url = f"https://ingrails.com/school/client?token={token_part}#learning-questions"
    else:
        target_url = config.get("website", {}).get("url", "")

    log.info(f"Navigating to: {target_url}")
    page.goto(target_url)
    page.wait_for_timeout(5000)

def quit_driver(driver: PwWrapper):
    try:
        driver.quit()
    except Exception:
        pass