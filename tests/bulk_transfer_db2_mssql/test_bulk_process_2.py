import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import allure, pytest
from pages.home_page import HomePage
from pages.process_definition_page import ProcessDefinitionPage
from utils.assert_util import AssertUtil
from utils.excel_reader import ExcelReader
from pages.process_list_page import ProcessListPage

SHEET = "Release"

@allure.feature("Bulk Transfer")
@allure.story("DB2 to MSSQL - Extended")
@pytest.mark.bulk_transfer_db2_mssql
class TestBulkProcessDB2MSSQLExtended:

    @allure.title("TC010 - Start the  bulk transfer process")
    def test_Start_process_tc010(self, page):
        raw = ExcelReader().get_test_data("TC010", SHEET, id_column="TestCase")
        process_name = str(raw.get("TestCase_Name", ""))
        HomePage(page).open().go_to_process_definition()
        proc = ProcessDefinitionPage(page)
        proc.click_bulk_process().click_bulk_process_by_name(process_name).start_bulk_process()
        ProcessListPage(page).click_process_list(process_name)
        ProcessListPage(page).save_process_part_input_to_excel( "TC010", SHEET, id_column="TestCase")
        ProcessListPage(page).save_process_part_input_reslute_to_excel( "TC010", SHEET, id_column="TestCase", part_name="Source Query")
        ProcessListPage(page).save_process_part_processingApplying_to_excel( "TC010", SHEET, id_column="TestCase")
        ProcessListPage(page).save_process_part_processingApplying_reslute_to_excel( "TC010", SHEET, id_column="TestCase")

        

 