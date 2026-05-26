import os, sys
import allure
import pytest
from playwright.sync_api import Browser, BrowserContext, Page, sync_playwright

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from utils.config_manager import ConfigManager
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

@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when == "call" and report.failed:
        pg = item.funcargs.get("page")
        if pg:
            name = item.nodeid.replace("::", "_").replace("/", "_")
            try: ScreenshotUtil.capture_on_failure(pg, name)
            except Exception: pass

def pytest_configure(config):
    os.makedirs("allure-results", exist_ok=True)
    os.makedirs("reports/screenshots", exist_ok=True)
    cfg = ConfigManager()
    with open("allure-results/environment.properties", "w") as f:
        f.write(f"application.url={cfg.web_url}\n")
        f.write(f"browser={cfg.browser}\n")
        f.write(f"headless={cfg.headless}\n")
