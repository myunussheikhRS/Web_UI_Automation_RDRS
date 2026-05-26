from dataclasses import dataclass
from typing import Optional

@dataclass
class ProcessData:
    test_case_id: str = ""
    TestCase_Name: str = ""
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
