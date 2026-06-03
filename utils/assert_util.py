import inspect
import pytest

from utils.report_logger import ReportLogger

class AssertUtil:
    @staticmethod
    def _caller_method_name():
        frame = inspect.currentframe()
        if frame is None:
            return "-"
        caller = frame.f_back
        # Walk out of AssertUtil internals to find the test/page method.
        while caller:
            name = caller.f_code.co_name
            if name not in {"assert_equals", "assert_true", "assert_false", "assert_contains", "assert_not_empty"}:
                return name
            caller = caller.f_back
        return "-"

    @staticmethod
    def assert_equals(actual, expected, field_name="value"):
        method_name = AssertUtil._caller_method_name()
        if actual == expected:
            ReportLogger.log_assert(field_name, expected, actual, "PASS", method_name=method_name)
        else:
            ReportLogger.log_assert(field_name, expected, actual, "FAIL", method_name=method_name)
            pytest.fail(f"Assert failed '{field_name}': expected='{expected}', actual='{actual}'")

    @staticmethod
    def assert_true(condition, message="condition"):
        method_name = AssertUtil._caller_method_name()
        if condition:
            ReportLogger.log_assert(message, True, True, "PASS", method_name=method_name)
        else:
            ReportLogger.log_assert(message, True, False, "FAIL", method_name=method_name)
            pytest.fail(f"Assert failed: '{message}' is not True")

    @staticmethod
    def assert_false(condition, message="condition"):
        AssertUtil.assert_true(not condition, message)

    @staticmethod
    def assert_contains(container, substring, field_name="text"):
        method_name = AssertUtil._caller_method_name()
        if substring in container:
            ReportLogger.log_assert(field_name, f"contains '{substring}'", container, "PASS", method_name=method_name)
        else:
            ReportLogger.log_assert(field_name, f"contains '{substring}'", container, "FAIL", method_name=method_name)
            pytest.fail(f"'{field_name}' value '{container}' does not contain '{substring}'")

    @staticmethod
    def assert_not_empty(value, field_name="value"):
        method_name = AssertUtil._caller_method_name()
        if value is not None and str(value).strip():
            ReportLogger.log_assert(field_name, "non-empty", value, "PASS", method_name=method_name)
        else:
            ReportLogger.log_assert(field_name, "non-empty", value, "FAIL", method_name=method_name)
            pytest.fail(f"'{field_name}' is empty or None")
