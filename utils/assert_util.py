import allure, pytest

class AssertUtil:
    @staticmethod
    def assert_equals(actual, expected, field_name="value"):
        with allure.step(f"Assert '{field_name}': expected='{expected}', actual='{actual}'"):
            if actual == expected:
                allure.attach(f"PASS | {field_name}: '{actual}' == '{expected}'",
                    name=f"PASS - {field_name}", attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach(f"FAIL | {field_name}: expected='{expected}' got='{actual}'",
                    name=f"FAIL - {field_name}", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"Assert failed '{field_name}': expected='{expected}', actual='{actual}'")
    @staticmethod
    def assert_true(condition, message="condition"):
        with allure.step(f"Assert True: {message}"):
            if condition:
                allure.attach(f"PASS | {message}", name=f"PASS - {message}",
                    attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach(f"FAIL | {message} is False", name=f"FAIL - {message}",
                    attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"Assert failed: '{message}' is not True")
    @staticmethod
    def assert_false(condition, message="condition"):
        AssertUtil.assert_true(not condition, message)
    @staticmethod
    def assert_contains(container, substring, field_name="text"):
        with allure.step(f"Assert '{field_name}' contains '{substring}'"):
            if substring in container:
                allure.attach(f"PASS | contains '{substring}'", name=f"PASS - {field_name}",
                    attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach(f"FAIL | does not contain '{substring}'",
                    name=f"FAIL - {field_name}", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"'{field_name}' value '{container}' does not contain '{substring}'")
    @staticmethod
    def assert_not_empty(value, field_name="value"):
        with allure.step(f"Assert '{field_name}' is not empty"):
            if value is not None and str(value).strip():
                allure.attach(f"PASS | '{field_name}' = '{value}'",
                    name=f"PASS - {field_name} not empty", attachment_type=allure.attachment_type.TEXT)
            else:
                allure.attach(f"FAIL | '{field_name}' is empty",
                    name=f"FAIL - {field_name} empty", attachment_type=allure.attachment_type.TEXT)
                pytest.fail(f"'{field_name}' is empty or None")
