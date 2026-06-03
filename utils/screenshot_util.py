import os
from datetime import datetime
from playwright.sync_api import Page
from utils.config_manager import ConfigManager

class ScreenshotUtil:
    @staticmethod
    def capture(page: Page, name: str = "screenshot") -> str:
        d = ConfigManager().screenshot_dir
        os.makedirs(d, exist_ok=True)
        ts = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        safe = "".join(c if c.isalnum() or c in "-_" else "_" for c in name)
        fp = os.path.join(d, f"{safe}_{ts}.png")
        page.screenshot(path=fp, full_page=True)
        return fp
    @staticmethod
    def capture_on_failure(page: Page, test_name: str) -> str:
        return ScreenshotUtil.capture(page, f"FAILURE_{test_name}")
