from __future__ import annotations
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage

_P = "agent_page"

class AgentPage(BasePage):
    def __init__(self, page: Page): super().__init__(page)

    @allure.step("Click Add Agent")
    def click_add_agent(self): self.click(self._loc(_P, "btn_add_agent")); return self

    @allure.step("Enter agent name: {name}")
    def enter_agent_name(self, name): self.fill(self._loc(_P, "input_agent_name"), name); return self

    @allure.step("Enter host: {host}")
    def enter_host(self, host): self.fill(self._loc(_P, "input_host"), host); return self

    @allure.step("Enter port: {port}")
    def enter_port(self, port): self.fill(self._loc(_P, "input_port"), str(port)); return self

    @allure.step("Enter description: {description}")
    def enter_description(self, description): self.fill(self._loc(_P, "input_description"), description); return self

    @allure.step("Select agent type: {agent_type}")
    def select_agent_type(self, agent_type): self.select_option_by_label(self._loc(_P, "select_agent_type"), agent_type); return self

    @allure.step("Click Save")
    def click_save(self): self.click(self._loc(_P, "btn_save")); self.wait_for_load_state("networkidle"); return self

    @allure.step("Click Cancel")
    def click_cancel(self): self.click(self._loc(_P, "btn_cancel")); return self

    @allure.step("Click Edit for agent: {agent_name}")
    def click_edit_agent(self, agent_name):
        self._get_agent_row(agent_name).locator("button.edit-agent, a.edit-agent, .agent-action-edit").click(); return self

    @allure.step("Click Delete for agent: {agent_name}")
    def click_delete_agent(self, agent_name):
        self._get_agent_row(agent_name).locator("button.delete-agent, .agent-action-delete").click(); return self

    @allure.step("Confirm delete")
    def confirm_delete(self): self.click(self._loc(_P, "btn_confirm_delete")); self.wait_for_load_state("networkidle"); return self

    @allure.step("Search agent: {term}")
    def search_agent(self, term): self.fill(self._loc(_P, "search_agent"), term); return self

    def fill_agent_form(self, agent_name, host, port, description="", agent_type=""):
        self.enter_agent_name(agent_name).enter_host(host).enter_port(port)
        if description: self.enter_description(description)
        if agent_type: self.select_agent_type(agent_type)
        return self

    def get_page_title(self): return self.get_text(self._loc(_P, "page_title"))
    def is_agent_present(self, agent_name):
        rows = self._loc(_P, "agent_table_rows")
        return any(agent_name in rows.nth(i).inner_text() for i in range(rows.count()))
    def get_agent_count(self): return self._loc(_P, "agent_table_rows").count()
    def _get_agent_row(self, agent_name):
        rows = self._loc(_P, "agent_table_rows")
        for i in range(rows.count()):
            r = rows.nth(i)
            if agent_name in r.inner_text(): return r
        raise ValueError(f"Agent not found: {agent_name}")
