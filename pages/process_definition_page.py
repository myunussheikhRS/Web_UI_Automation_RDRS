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

#**********************************############################

    # written by Yunus
    @allure.step("Click BulkProcess")
    def click_bulk_process(self): self.click(self._loc(_P, "bulk_process")); self.page.keyboard.press("ArrowRight"); return self

    # written by Yunus
    @allure.step("Click on process in BulkProcess: {process_name}")
    def click_bulk_process_by_name(self, process_name):
        self._get_process_row(process_name).click(); return self    
    
    # written by Yunus
    @allure.step("Start the bulk process")
    def start_bulk_process(self):
        btns = self._loc(_P, "btn_start_bulk_process")
        btn = None
        for i in range(btns.count()):
            candidate = btns.nth(i)
            if candidate.is_visible():
                btn = candidate
                break
        if btn is None:
            btn = btns.first

        btn.wait_for(state="attached", timeout=self._timeout)
        btn.wait_for(state="visible", timeout=self._timeout)

        # Bring element into viewport even when nested inside a scrollable container.
        is_in_viewport = False
        for _ in range(5):
            btn.evaluate(
                """
                (el) => {
                    const isScrollable = (node) => {
                        const s = getComputedStyle(node);
                        const o = `${s.overflow}${s.overflowY}${s.overflowX}`;
                        return /(auto|scroll|overlay)/.test(o);
                    };

                    let p = el.parentElement;
                    while (p) {
                        if (isScrollable(p)) {
                            const r = el.getBoundingClientRect();
                            const pr = p.getBoundingClientRect();
                            p.scrollTop += (r.top - pr.top) - (p.clientHeight / 2) + (r.height / 2);
                            p.scrollLeft += (r.left - pr.left) - (p.clientWidth / 2) + (r.width / 2);
                        }
                        p = p.parentElement;
                    }

                    el.scrollIntoView({ block: 'center', inline: 'center', behavior: 'instant' });
                }
                """
            )
            is_in_viewport = btn.evaluate(
                """
                (el) => {
                    const r = el.getBoundingClientRect();
                    return (
                        r.width > 0 &&
                        r.height > 0 &&
                        r.top >= 0 &&
                        r.left >= 0 &&
                        r.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
                        r.right <= (window.innerWidth || document.documentElement.clientWidth)
                    );
                }
                """
            )
            if is_in_viewport:
                break
            self.page.mouse.wheel(0, 600)

        if not is_in_viewport:
            raise AssertionError("START PROCESS button is not visible in viewport before click")

        try:
            btn.click(timeout=self._timeout)
        except Exception:
            btn.click(force=True, timeout=self._timeout)

        ok_btn = self.page.get_by_role("button", name="OK")
        if ok_btn.count() == 0:
            ok_btn = self.page.get_by_text("OK", exact=True).last
        ok_btn.wait_for(state="visible", timeout=self._timeout)
        ok_btn.click()
        return self

    @allure.step("Search process: {term}")
    def search_process(self, term): self.fill(self._loc(_P, "search_process"), term); return self

    # Additional helper to fill the form in one step
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
        return self.page.get_by_text(process_name, exact=True).count() > 0
    def get_process_count(self): return self._loc(_P, "process_table_rows").count()
    def _get_process_row(self, process_name):
        self.page.wait_for_load_state("networkidle")
        loc = self.page.get_by_text(process_name, exact=True)
        if loc.count() == 0:
            print(f"\n[DEBUG] Current URL: {self.page.url}")
            print(f"[DEBUG] Page title: {self.page.title()}")
            print(f"[DEBUG] Page text snippet: {self.page.inner_text('body')[:500]}")
            raise ValueError(f"Process not found: {process_name}")
        return loc.first
