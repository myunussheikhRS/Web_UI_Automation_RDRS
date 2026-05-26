from __future__ import annotations
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage

_P = "output_target_page"

class OutputTargetPage(BasePage):
    def __init__(self, page: Page): super().__init__(page)

    @allure.step("Click Add Output Target")
    def click_add_output_target(self): self.click(self._loc(_P, "btn_add_output_target")); return self

    @allure.step("Enter OT name: {name}")
    def enter_ot_name(self, name): self.fill(self._loc(_P, "input_ot_name"), name); return self

    @allure.step("Enter host: {host}")
    def enter_host(self, host): self.fill(self._loc(_P, "input_host"), host); return self

    @allure.step("Enter port: {port}")
    def enter_port(self, port): self.fill(self._loc(_P, "input_port"), str(port)); return self

    @allure.step("Enter database: {database}")
    def enter_database(self, database): self.fill(self._loc(_P, "input_database"), database); return self

    @allure.step("Enter username: {username}")
    def enter_username(self, username): self.fill(self._loc(_P, "input_username"), username); return self

    @allure.step("Enter password")
    def enter_password(self, password): self.fill(self._loc(_P, "input_password"), password); return self

    @allure.step("Enter schema: {schema}")
    def enter_schema(self, schema): self.fill(self._loc(_P, "input_schema"), schema); return self

    @allure.step("Select OT type: {ot_type}")
    def select_ot_type(self, ot_type): self.select_option_by_label(self._loc(_P, "select_ot_type"), ot_type); return self

    @allure.step("Select agent: {agent_name}")
    def select_agent(self, agent_name): self.select_option_by_label(self._loc(_P, "select_agent"), agent_name); return self

    @allure.step("Click Test Connection")
    def click_test_connection(self): self.click(self._loc(_P, "btn_test_connection")); return self

    @allure.step("Click Save")
    def click_save(self): self.click(self._loc(_P, "btn_save")); self.wait_for_load_state("networkidle"); return self

    @allure.step("Click Cancel")
    def click_cancel(self): self.click(self._loc(_P, "btn_cancel")); return self

    @allure.step("Click Edit OT: {ot_name}")
    def click_edit_output_target(self, ot_name):
        self._get_ot_row(ot_name).locator("button.edit-output-target, .ot-action-edit").click(); return self

    @allure.step("Click Delete OT: {ot_name}")
    def click_delete_output_target(self, ot_name):
        self._get_ot_row(ot_name).locator("button.delete-output-target, .ot-action-delete").click(); return self

    @allure.step("Confirm delete")
    def confirm_delete(self): self.click(self._loc(_P, "btn_confirm_delete")); self.wait_for_load_state("networkidle"); return self

    def fill_output_target_form(self, ot_name, ot_type, host, port, database, username, password, schema="", agent_name=""):
        self.enter_ot_name(ot_name).select_ot_type(ot_type).enter_host(host).enter_port(port)
        self.enter_database(database).enter_username(username).enter_password(password)
        if schema: self.enter_schema(schema)
        if agent_name: self.select_agent(agent_name)
        return self

    def get_page_title(self): return self.get_text(self._loc(_P, "page_title"))
    def is_output_target_present(self, ot_name):
        rows = self._loc(_P, "output_target_table_rows")
        return any(ot_name in rows.nth(i).inner_text() for i in range(rows.count()))
    def get_connection_success_message(self): return self.get_text(self._loc(_P, "connection_success_msg"))
    def _get_ot_row(self, ot_name):
        rows = self._loc(_P, "output_target_table_rows")
        for i in range(rows.count()):
            r = rows.nth(i)
            if ot_name in r.inner_text(): return r
        raise ValueError(f"OutputTarget not found: {ot_name}")
