import os, textwrap

BASE = r"C:\Users\msheikh\RDRS_Web_Automation"

def w(rel, content):
    p = os.path.join(BASE, rel.replace("/", os.sep))
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content).lstrip("\n"))
    print("OK:", rel)

w("pages/__init__.py", "")

w("pages/base_page.py", """
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
""")

w("pages/home_page.py", """
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
        self.click(self._loc(_P, "menu_process_definition")); return self

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
""")

w("pages/agent_page.py", """
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
""")

w("pages/data_source_page.py", """
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
""")

w("pages/process_definition_page.py", """
from __future__ import annotations
import allure
from playwright.sync_api import Page
from pages.base_page import BasePage

_P = "process_definition_page"

class ProcessDefinitionPage(BasePage):
    def __init__(self, page: Page): super().__init__(page)

    @allure.step("Click Add Process")
    def click_add_process(self): self.click(self._loc(_P, "btn_add_process")); return self

    @allure.step("Enter process name: {name}")
    def enter_process_name(self, name): self.fill(self._loc(_P, "input_process_name"), name); return self

    @allure.step("Enter description: {description}")
    def enter_description(self, description): self.fill(self._loc(_P, "input_description"), description); return self

    @allure.step("Select process type: {process_type}")
    def select_process_type(self, process_type): self.select_option_by_label(self._loc(_P, "select_process_type"), process_type); return self

    @allure.step("Select transfer mode: {mode}")
    def select_transfer_mode(self, mode): self.select_option_by_label(self._loc(_P, "select_transfer_mode"), mode); return self

    @allure.step("Select source DS: {ds_name}")
    def select_source_datasource(self, ds_name): self.select_option_by_label(self._loc(_P, "select_source_ds"), ds_name); return self

    @allure.step("Select target DS: {ds_name}")
    def select_target_datasource(self, ds_name): self.select_option_by_label(self._loc(_P, "select_target_ds"), ds_name); return self

    @allure.step("Enter source schema: {schema}")
    def enter_source_schema(self, schema): self.fill(self._loc(_P, "input_source_schema"), schema); return self

    @allure.step("Enter source table: {table}")
    def enter_source_table(self, table): self.fill(self._loc(_P, "input_source_table"), table); return self

    @allure.step("Enter target schema: {schema}")
    def enter_target_schema(self, schema): self.fill(self._loc(_P, "input_target_schema"), schema); return self

    @allure.step("Enter target table: {table}")
    def enter_target_table(self, table): self.fill(self._loc(_P, "input_target_table"), table); return self

    @allure.step("Set truncate target: {enabled}")
    def set_truncate_target(self, enabled):
        (self.check if enabled else self.uncheck)(self._loc(_P, "checkbox_truncate_target")); return self

    @allure.step("Set create table: {enabled}")
    def set_create_table(self, enabled):
        (self.check if enabled else self.uncheck)(self._loc(_P, "checkbox_create_table")); return self

    @allure.step("Click Next Step")
    def click_next_step(self): self.click(self._loc(_P, "btn_next_step")); return self

    @allure.step("Click Finish")
    def click_finish(self): self.click(self._loc(_P, "btn_finish")); self.wait_for_load_state("networkidle"); return self

    @allure.step("Click Save")
    def click_save(self): self.click(self._loc(_P, "btn_save")); self.wait_for_load_state("networkidle"); return self

    @allure.step("Click Cancel")
    def click_cancel(self): self.click(self._loc(_P, "btn_cancel")); return self

    @allure.step("Click Edit process: {process_name}")
    def click_edit_process(self, process_name):
        self._get_process_row(process_name).locator("button.edit-process, a.edit-process, .process-action-edit").click(); return self

    @allure.step("Click Delete process: {process_name}")
    def click_delete_process(self, process_name):
        self._get_process_row(process_name).locator("button.delete-process, .process-action-delete").click(); return self

    @allure.step("Confirm delete")
    def confirm_delete(self): self.click(self._loc(_P, "btn_confirm_delete")); self.wait_for_load_state("networkidle"); return self

    @allure.step("Click Mapping tab")
    def click_mapping_tab(self): self.click(self._loc(_P, "tab_mapping")); return self

    @allure.step("Search process: {term}")
    def search_process(self, term): self.fill(self._loc(_P, "search_process"), term); return self

    def fill_process_form(self, process_name, process_type, source_ds, target_ds,
                          source_schema="", source_table="", target_schema="", target_table="",
                          transfer_mode="", truncate_target=False, create_table=False, description=""):
        self.enter_process_name(process_name)
        if description: self.enter_description(description)
        self.select_process_type(process_type)
        if transfer_mode: self.select_transfer_mode(transfer_mode)
        self.select_source_datasource(source_ds).select_target_datasource(target_ds)
        if source_schema: self.enter_source_schema(source_schema)
        if source_table: self.enter_source_table(source_table)
        if target_schema: self.enter_target_schema(target_schema)
        if target_table: self.enter_target_table(target_table)
        self.set_truncate_target(truncate_target).set_create_table(create_table)
        return self

    def get_page_title(self): return self.get_text(self._loc(_P, "page_title"))
    def is_process_present(self, process_name):
        rows = self._loc(_P, "process_table_rows")
        return any(process_name in rows.nth(i).inner_text() for i in range(rows.count()))
    def get_process_count(self): return self._loc(_P, "process_table_rows").count()
    def _get_process_row(self, process_name):
        rows = self._loc(_P, "process_table_rows")
        for i in range(rows.count()):
            r = rows.nth(i)
            if process_name in r.inner_text(): return r
        raise ValueError(f"Process not found: {process_name}")
""")

w("pages/process_list_page.py", """
from __future__ import annotations
import time, allure
from playwright.sync_api import Page
from pages.base_page import BasePage

_P = "process_list_page"

class ProcessListPage(BasePage):
    def __init__(self, page: Page): super().__init__(page)

    @allure.step("Run process: {process_name}")
    def click_run_process(self, process_name):
        self._get_process_row(process_name).locator("button.run-process, a.run-process, .process-action-run").click(); return self

    @allure.step("Stop process: {process_name}")
    def click_stop_process(self, process_name):
        self._get_process_row(process_name).locator("button.stop-process, .process-action-stop").click(); return self

    @allure.step("View log: {process_name}")
    def click_view_log(self, process_name):
        self._get_process_row(process_name).locator("button.view-log, .process-action-log").click(); return self

    @allure.step("Click Refresh")
    def click_refresh(self): self.click(self._loc(_P, "btn_refresh")); self.wait_for_load_state("networkidle"); return self

    @allure.step("Filter by status: {status}")
    def filter_by_status(self, status): self.select_option_by_label(self._loc(_P, "filter_status"), status); return self

    @allure.step("Search: {term}")
    def search_process(self, term): self.fill(self._loc(_P, "search_process"), term); return self

    @allure.step("Close log modal")
    def close_log_modal(self): self.click(self._loc(_P, "btn_close_log")); return self

    @allure.step("Wait for process '{process_name}' to reach '{expected_status}'")
    def wait_for_process_status(self, process_name, expected_status, timeout_ms=60000):
        deadline = time.time() + timeout_ms / 1000
        while time.time() < deadline:
            if self.get_process_status(process_name).upper() == expected_status.upper():
                return self
            self.click_refresh()
            self.page.wait_for_timeout(2000)
        raise TimeoutError(f"Process '{process_name}' did not reach '{expected_status}'")

    def get_page_title(self): return self.get_text(self._loc(_P, "page_title"))
    def get_process_status(self, process_name):
        return self._get_process_row(process_name).locator("td.process-status, td:nth-child(3), span.status").inner_text().strip()
    def is_process_present(self, process_name):
        rows = self._loc(_P, "process_table_rows")
        return any(process_name in rows.nth(i).inner_text() for i in range(rows.count()))
    def get_log_content(self): return self.get_text(self._loc(_P, "log_content"))
    def get_process_count(self): return self._loc(_P, "process_table_rows").count()
    def _get_process_row(self, process_name):
        rows = self._loc(_P, "process_table_rows")
        for i in range(rows.count()):
            r = rows.nth(i)
            if process_name in r.inner_text(): return r
        raise ValueError(f"Process not found in list: {process_name}")
""")

w("pages/repository_page.py", """
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
""")

w("pages/output_target_page.py", """
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
""")

# ── models ────────────────────────────────────────────────────────────────────
w("models/__init__.py", "")
w("models/process_data.py", """
from dataclasses import dataclass
from typing import Optional

@dataclass
class ProcessData:
    test_case_id: str = ""
    process_name: str = ""
    description: str = ""
    process_type: str = ""
    transfer_mode: str = ""
    source_datasource: str = ""
    source_schema: str = ""
    source_table: str = ""
    target_datasource: str = ""
    target_schema: str = ""
    target_table: str = ""
    truncate_target: bool = False
    create_table: bool = False
    schedule_enabled: bool = False
    cron_expression: str = ""
    expected_status: str = "COMPLETED"
    expected_row_count: Optional[int] = None

    @classmethod
    def from_dict(cls, data: dict) -> "ProcessData":
        def b(v): return str(v).strip().lower() in ("true","yes","1","y") if v else False
        def i(v):
            try: return int(v) if v is not None else None
            except: return None
        return cls(
            test_case_id=str(data.get("test_case_id","")).strip(),
            process_name=str(data.get("process_name","")).strip(),
            description=str(data.get("description","")).strip(),
            process_type=str(data.get("process_type","")).strip(),
            transfer_mode=str(data.get("transfer_mode","")).strip(),
            source_datasource=str(data.get("source_datasource","")).strip(),
            source_schema=str(data.get("source_schema","")).strip(),
            source_table=str(data.get("source_table","")).strip(),
            target_datasource=str(data.get("target_datasource","")).strip(),
            target_schema=str(data.get("target_schema","")).strip(),
            target_table=str(data.get("target_table","")).strip(),
            truncate_target=b(data.get("truncate_target")),
            create_table=b(data.get("create_table")),
            schedule_enabled=b(data.get("schedule_enabled")),
            cron_expression=str(data.get("cron_expression","")).strip(),
            expected_status=str(data.get("expected_status","COMPLETED")).strip(),
            expected_row_count=i(data.get("expected_row_count")),
        )
""")

print("pages/ and models/ done")