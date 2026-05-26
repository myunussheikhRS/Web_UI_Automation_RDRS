from __future__ import annotations
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage

_P = "home_page"

class HomePage(BasePage):
    def __init__(self, page: Page): super().__init__(page)

    @allure.step("Open RDRS application")
    def open(self):
        self.navigate(); self.wait_for_load_state("networkidle"); return self

    @allure.step("Navigate to Agent page")
    def go_to_agent(self):
        self.click(self._loc(_P, "menu_agent")); return self

    @allure.step("Navigate to Data Source page")
    def go_to_data_source(self):
        self.click(self._loc(_P, "menu_data_source")); return self

    @allure.step("Navigate to Process Definition page")
    def go_to_process_definition(self):
        self.click(self._loc(_P, "menu_process_definition"));
        self.page.keyboard.press("ArrowRight")
        return self

    @allure.step("Navigate to Process List page")
    def go_to_process_list(self):
        self.click(self._loc(_P, "menu_process_list")); return self

    @allure.step("Navigate to Repository page")
    def go_to_repository(self):
        self.click(self._loc(_P, "menu_repository")); return self

    @allure.step("Navigate to Output Target page")
    def go_to_output_target(self):
        self.click(self._loc(_P, "menu_output_target")); return self

    def get_page_title(self): return self.get_text(self._loc(_P, "page_title"))
    def is_menu_visible(self): return self.is_visible(self._loc(_P, "main_menu"))
    def get_success_message(self): return self.get_text(self._loc(_P, "success_message"))
    def get_error_message(self): return self.get_text(self._loc(_P, "error_message"))
