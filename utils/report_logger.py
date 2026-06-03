import threading
from collections import Counter
from datetime import datetime


class ReportLogger:
    _local = threading.local()

    @classmethod
    def _entries(cls):
        if not hasattr(cls._local, "entries"):
            cls._local.entries = []
        return cls._local.entries

    @classmethod
    def clear(cls):
        cls._local.entries = []

    @classmethod
    def log_step(cls, message):
        cls._entries().append({
            "kind": "step",
            "status": "INFO",
            "message": str(message),
            "time": datetime.now().strftime("%H:%M:%S"),
        })

    @classmethod
    def log_info(cls, message):
        cls._entries().append({
            "kind": "info",
            "status": "INFO",
            "message": str(message),
            "time": datetime.now().strftime("%H:%M:%S"),
        })

    @classmethod
    def log_assert(cls, field_name, expected, actual, status, method_name=""):
        cls._entries().append({
            "kind": "assert",
            "status": status,
            "field": str(field_name),
            "expected": "" if expected is None else str(expected),
            "actual": "" if actual is None else str(actual),
            "method": str(method_name or "-"),
            "time": datetime.now().strftime("%H:%M:%S"),
        })

    @classmethod
    def log_attachment(cls, name, attachment_type="TEXT", preview=""):
        cls._entries().append({
            "kind": "attachment",
            "status": "INFO",
            "name": str(name or "attachment"),
            "attachment_type": str(attachment_type),
            "preview": str(preview),
            "time": datetime.now().strftime("%H:%M:%S"),
        })

    @classmethod
    def get_entries(cls):
        return list(cls._entries())

    @classmethod
    def get_assert_counts(cls):
        statuses = [e["status"] for e in cls._entries() if e.get("kind") == "assert"]
        counts = Counter(statuses)
        return {
            "total": sum(counts.values()),
            "pass": counts.get("PASS", 0),
            "fail": counts.get("FAIL", 0),
        }
