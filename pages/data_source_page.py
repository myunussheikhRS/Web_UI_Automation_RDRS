from __future__ import annotations
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage

_P = "data_source_page"

class DataSourcePage(BasePage):
    def __init__(self, page: Page): super().__init__(page)

    @allure.step("Click Add Data Source")
    def click_add_datasource(self): self.click(self._loc(_P, "btn_add_datasource")); return self

    @allure.step("Enter DS name: {name}")
    def enter_ds_name(self, name): self.fill(self._loc(_P, "input_ds_name"), name); return self

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

    @allure.step("Select DB type: {db_type}")
    def select_db_type(self, db_type): self.select_option_by_label(self._loc(_P, "select_db_type"), db_type); return self

    @allure.step("Select agent: {agent_name}")
    def select_agent(self, agent_name): self.select_option_by_label(self._loc(_P, "select_agent"), agent_name); return self

    @allure.step("Click Test Connection")
    def click_test_connection(self): self.click(self._loc(_P, "btn_test_connection")); return self

    @allure.step("Click Save")
    def click_save(self): self.click(self._loc(_P, "btn_save")); self.wait_for_load_state("networkidle"); return self

    @allure.step("Click Cancel")
    def click_cancel(self): self.click(self._loc(_P, "btn_cancel")); return self

    @allure.step("Click Edit DS: {ds_name}")
    def click_edit_datasource(self, ds_name):
        self._get_ds_row(ds_name).locator("button.edit-datasource, a.edit-datasource, .ds-action-edit").click(); return self

    @allure.step("Click Delete DS: {ds_name}")
    def click_delete_datasource(self, ds_name):
        self._get_ds_row(ds_name).locator("button.delete-datasource, .ds-action-delete").click(); return self

    @allure.step("Confirm delete")
    def confirm_delete(self): self.click(self._loc(_P, "btn_confirm_delete")); self.wait_for_load_state("networkidle"); return self

    def fill_datasource_form(self, ds_name, db_type, host, port, database, username, password, schema="", agent_name=""):
        self.enter_ds_name(ds_name).select_db_type(db_type).enter_host(host).enter_port(port)
        self.enter_database(database).enter_username(username).enter_password(password)
        if schema: self.enter_schema(schema)
        if agent_name: self.select_agent(agent_name)
        return self

    def get_page_title(self): return self.get_text(self._loc(_P, "page_title"))
    def is_datasource_present(self, ds_name):
        rows = self._loc(_P, "datasource_table_rows")
        return any(ds_name in rows.nth(i).inner_text() for i in range(rows.count()))
    def get_connection_success_message(self): return self.get_text(self._loc(_P, "connection_success_msg"))
    def get_connection_error_message(self): return self.get_text(self._loc(_P, "connection_error_msg"))
    def _get_ds_row(self, ds_name):
        rows = self._loc(_P, "datasource_table_rows")
        for i in range(rows.count()):
            r = rows.nth(i)
            if ds_name in r.inner_text(): return r
        raise ValueError(f"DataSource not found: {ds_name}")
