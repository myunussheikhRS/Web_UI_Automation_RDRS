import allure, pytest
from models.process_data import ProcessData
from pages.home_page import HomePage
from pages.process_definition_page import ProcessDefinitionPage
from pages.process_list_page import ProcessListPage
from utils.assert_util import AssertUtil
from utils.excel_reader import ExcelReader

SHEET = "BulkTransfer_VSAM_MSSQL"

@allure.feature("Bulk Transfer")
@allure.story("VSAM to MSSQL")
@pytest.mark.bulk_transfer_vsam_mssql
class TestBulkProcessVSAMMSSQL:

    @allure.title("TC001 - Create and run bulk transfer VSAM to MSSQL")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_bulk_transfer_tc001(self, page):
        data = ProcessData.from_dict(ExcelReader().get_test_data("TC001", SHEET))
        HomePage(page).open().go_to_process_definition()
        proc = ProcessDefinitionPage(page)
        proc.click_add_process().fill_process_form(
            process_name=data.process_name, process_type=data.process_type,
            source_ds=data.source_datasource, target_ds=data.target_datasource,
            source_schema=data.source_schema, source_table=data.source_table,
            target_schema=data.target_schema, target_table=data.target_table,
            transfer_mode=data.transfer_mode, truncate_target=data.truncate_target,
        ).click_save()
        AssertUtil.assert_true(proc.is_process_present(data.process_name),
            f"Process '{data.process_name}' visible after save")
        HomePage(page).go_to_process_list()
        pl = ProcessListPage(page)
        pl.click_run_process(data.process_name)
        pl.wait_for_process_status(data.process_name, data.expected_status, 120000)
        AssertUtil.assert_equals(pl.get_process_status(data.process_name).upper(),
            data.expected_status.upper(), "Process status")
