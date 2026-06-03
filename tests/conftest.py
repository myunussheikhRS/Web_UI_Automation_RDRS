import base64
import html
import os
import sys
from datetime import datetime

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.config_manager import ConfigManager
from utils.report_logger import ReportLogger
from utils.screenshot_util import ScreenshotUtil

@pytest.fixture(scope="session")
def config():
    return ConfigManager()

@pytest.fixture(scope="session")
def playwright_instance():
    with sync_playwright() as pw:
        yield pw

@pytest.fixture(scope="session")
def browser(playwright_instance, config):
    opts = {"headless": config.headless}
    name = config.browser.lower()
    if name == "chromium": br = playwright_instance.chromium.launch(**opts)
    elif name == "firefox": br = playwright_instance.firefox.launch(**opts)
    elif name == "webkit":  br = playwright_instance.webkit.launch(**opts)
    else: raise ValueError(f"Unsupported browser: {name}")
    yield br
    br.close()

@pytest.fixture(scope="function")
def context(browser):
    ctx = browser.new_context(viewport={"width":1920,"height":1080}, ignore_https_errors=True)
    yield ctx
    ctx.close()

@pytest.fixture(scope="function")
def page(context):
    pg = context.new_page()
    yield pg
    pg.close()


@pytest.fixture(autouse=True)
def _reset_report_logger():
    ReportLogger.clear()
    yield

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()

    if report.when != "call":
        return

    pg = item.funcargs.get("page")
    pytest_html = item.config.pluginmanager.getplugin("html")

    report.test_method = item.name
    report.test_module = item.module.__name__ if item.module else "-"
    report.test_class = item.cls.__name__ if item.cls else "-"

    entries = ReportLogger.get_entries()
    counts = ReportLogger.get_assert_counts()
    report.assert_total = counts["total"]
    report.assert_pass = counts["pass"]
    report.assert_fail = counts["fail"]

    extras = getattr(report, "extras", [])
    safe_name = item.nodeid.replace("::", "_").replace("/", "_").replace("\\", "_")

    if pg:
        try:
            status_tag = "PASS" if report.passed else "FAIL"
            screenshot_path = ScreenshotUtil.capture(pg, f"{status_tag}_{safe_name}")
            report.screenshot_name = os.path.basename(screenshot_path)

            if pytest_html:
                with open(screenshot_path, "rb") as image_file:
                    screenshot_b64 = base64.b64encode(image_file.read()).decode("utf-8")
                extras.append(
                    pytest_html.extras.image(
                        screenshot_b64,
                        mime_type="image/png",
                        extension="png",
                        name=f"Screenshot ({status_tag})",
                    )
                )
        except Exception as exc:
            report.screenshot_name = f"capture_error: {exc}"

    if pytest_html and entries:
        rows = []
        for entry in entries:
            if entry.get("kind") == "assert":
                status_class = "ok" if entry.get("status") == "PASS" else "bad"
                rows.append(
                    "<tr>"
                    f"<td>{html.escape(entry.get('time', '-'))}</td>"
                    f"<td>{html.escape(entry.get('method', '-'))}</td>"
                    f"<td>{html.escape(entry.get('field', '-'))}</td>"
                    f"<td class='{status_class}'>{html.escape(entry.get('status', '-'))}</td>"
                    f"<td>{html.escape(entry.get('expected', ''))}</td>"
                    f"<td>{html.escape(entry.get('actual', ''))}</td>"
                    "</tr>"
                )
            else:
                rows.append(
                    "<tr>"
                    f"<td>{html.escape(entry.get('time', '-'))}</td>"
                    "<td colspan='5'>"
                    f"{html.escape(entry.get('message') or entry.get('preview') or str(entry))}"
                    "</td>"
                    "</tr>"
                )

        details_html = (
            "<div class='test-details'>"
            "<h4>Validation Details</h4>"
            "<table class='detail-table'>"
            "<thead><tr>"
            "<th>Time</th><th>Method</th><th>Field</th><th>Status</th><th>Expected</th><th>Actual</th>"
            "</tr></thead>"
            f"<tbody>{''.join(rows)}</tbody>"
            "</table>"
            "</div>"
        )
        extras.append(pytest_html.extras.html(details_html))

    report.extras = extras

def pytest_configure(config):
    os.makedirs("reports/screenshots", exist_ok=True)


def pytest_html_report_title(report):
    report.title = "RDRS Extent-Style Automation Report"


def pytest_html_results_summary(prefix, summary, postfix):
    cfg = ConfigManager()
    prefix.extend(
        [
            f"<p><strong>Application:</strong> {html.escape(cfg.web_url)}</p>",
            f"<p><strong>Browser:</strong> {html.escape(cfg.browser)} | <strong>Headless:</strong> {cfg.headless}</p>",
            f"<p><strong>Generated:</strong> {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>",
        ]
    )


def pytest_html_results_table_header(cells):
    cells.insert(2, "<th>Module/Class</th>")
    cells.insert(3, "<th>Method</th>")
    cells.insert(4, "<th>Assertions</th>")
    cells.insert(5, "<th>Screenshot</th>")


def pytest_html_results_table_row(report, cells):
    module_class = f"{getattr(report, 'test_module', '-')} / {getattr(report, 'test_class', '-') }"
    cells.insert(2, f"<td>{html.escape(module_class)}</td>")
    cells.insert(3, f"<td>{html.escape(getattr(report, 'test_method', '-'))}</td>")

    total = getattr(report, "assert_total", 0)
    passed = getattr(report, "assert_pass", 0)
    failed = getattr(report, "assert_fail", 0)
    cells.insert(4, f"<td><span class='badge'>{total}</span> (P:{passed} / F:{failed})</td>")
    cells.insert(5, f"<td>{html.escape(getattr(report, 'screenshot_name', '-'))}</td>")
