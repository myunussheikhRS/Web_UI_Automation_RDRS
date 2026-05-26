from __future__ import annotations
from typing import Optional
import allure
from playwright.sync_api import Page, Locator, TimeoutError as PWTimeout
from utils.config_manager import ConfigManager
from utils.locator_reader import LocatorReader

class BasePage:
    def __init__(self, page: Page):
        self.page = page
        self._config = ConfigManager()
        self._locator_reader = LocatorReader()
        self._timeout = self._config.explicit_wait * 1000
    def navigate(self, url=None):
        self.page.goto(url or self._config.web_url); return self
    def get_current_url(self): return self.page.url
    def get_title(self): return self.page.title()
    def refresh(self): self.page.reload(); return self
    def _loc(self, page_name, key):
        return self.page.locator(self._locator_reader.get_selector(page_name, key))
    def click(self, loc):
        loc.wait_for(state="visible", timeout=self._timeout); loc.click(); return self
    def fill(self, loc, text):
        loc.wait_for(state="visible", timeout=self._timeout)
        loc.clear(); loc.fill(text); return self
    def select_option(self, loc, value):
        loc.wait_for(state="visible", timeout=self._timeout)
        loc.select_option(value=value); return self
    def select_option_by_label(self, loc, label):
        loc.wait_for(state="visible", timeout=self._timeout)
        loc.select_option(label=label); return self
    def check(self, loc):
        loc.wait_for(state="visible", timeout=self._timeout); loc.check(); return self
    def uncheck(self, loc):
        loc.wait_for(state="visible", timeout=self._timeout); loc.uncheck(); return self
    def get_text(self, loc):
        loc.wait_for(state="visible", timeout=self._timeout)
        return (loc.inner_text() or "").strip()
    def get_value(self, loc):
        loc.wait_for(state="visible", timeout=self._timeout)
        return (loc.input_value() or "").strip()
    def is_visible(self, loc, timeout=5000):
        try: loc.wait_for(state="visible", timeout=timeout); return True
        except PWTimeout: return False
    def is_enabled(self, loc): return loc.is_enabled()
    def wait_for_visible(self, loc):
        loc.wait_for(state="visible", timeout=self._timeout); return self
    def wait_for_hidden(self, loc):
        loc.wait_for(state="hidden", timeout=self._timeout); return self
    def wait_for_url_contains(self, fragment):
        self.page.wait_for_url(f"**{fragment}**", timeout=self._timeout); return self
    def wait_for_load_state(self, state="networkidle"):
        self.page.wait_for_load_state(state, timeout=self._timeout); return self
    def scroll_into_view(self, loc):
        loc.scroll_into_view_if_needed(); return self
