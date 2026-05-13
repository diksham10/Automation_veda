from playwright.sync_api import sync_playwright

class PwWrapper:
    def __init__(self, config):
        self.playwright = sync_playwright().start()
        headless = config.get("automation", {}).get("headless_mode", False)
        # Using chromium or firefox? Firefox caused Marionette crashes, Chromium could be lighter. 
        # But user installed firefox playwright earlier manually.
        self.browser = self.playwright.firefox.launch(headless=headless)
        
        # We can add cookies, bypass image loading easily in playwright to save RAM?
        # Actually playwright itself is very robust to OOM.
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def quit(self):
        self.page.close()
        self.context.close()
        self.browser.close()
        self.playwright.stop()
