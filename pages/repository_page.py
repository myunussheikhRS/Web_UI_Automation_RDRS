from __future__ import annotations
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage

_P = "repository_page"

class RepositoryPage(BasePage):
    def __init__(self, page: Page): super().__init__(page)

    @allure.step("Click Add Repository")
    def click_add_repository(self): self.click(self._loc(_P, "btn_add_repository")); return self

    @allure.step("Enter repo name: {name}")
    def enter_repo_name(self, name): self.fill(self._loc(_P, "input_repo_name"), name); return self

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

    @allure.step("Select repo type: {repo_type}")
    def select_repo_type(self, repo_type): self.select_option_by_label(self._loc(_P, "select_repo_type"), repo_type); return self

    @allure.step("Click Test Connection")
    def click_test_connection(self): self.click(self._loc(_P, "btn_test_connection")); return self

    @allure.step("Click Save")
    def click_save(self): self.click(self._loc(_P, "btn_save")); self.wait_for_load_state("networkidle"); return self

    @allure.step("Click Cancel")
    def click_cancel(self): self.click(self._loc(_P, "btn_cancel")); return self

    @allure.step("Click Edit repo: {repo_name}")
    def click_edit_repository(self, repo_name):
        self._get_repo_row(repo_name).locator("button.edit-repository, a.edit-repository, .repo-action-edit").click(); return self

    @allure.step("Click Delete repo: {repo_name}")
    def click_delete_repository(self, repo_name):
        self._get_repo_row(repo_name).locator("button.delete-repository, .repo-action-delete").click(); return self

    @allure.step("Confirm delete")
    def confirm_delete(self): self.click(self._loc(_P, "btn_confirm_delete")); self.wait_for_load_state("networkidle"); return self

    def fill_repository_form(self, repo_name, repo_type, host, port, database, username, password):
        self.enter_repo_name(repo_name).select_repo_type(repo_type).enter_host(host).enter_port(port)
        self.enter_database(database).enter_username(username).enter_password(password)
        return self

    def get_page_title(self): return self.get_text(self._loc(_P, "page_title"))
    def is_repository_present(self, repo_name):
        rows = self._loc(_P, "repository_table_rows")
        return any(repo_name in rows.nth(i).inner_text() for i in range(rows.count()))
    def get_connection_success_message(self): return self.get_text(self._loc(_P, "connection_success_msg"))
    def _get_repo_row(self, repo_name):
        rows = self._loc(_P, "repository_table_rows")
        for i in range(rows.count()):
            r = rows.nth(i)
            if repo_name in r.inner_text(): return r
        raise ValueError(f"Repository not found: {repo_name}")
