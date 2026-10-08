import os
import time
from pathlib import Path

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.utils.html_report import write_html_report


_TEST_RESULTS = {}
_SESSION_STARTED_AT = 0.0


def _is_truthy(value):
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


def pytest_sessionstart(session):
    global _SESSION_STARTED_AT
    _TEST_RESULTS.clear()
    _SESSION_STARTED_AT = time.perf_counter()


def pytest_runtest_logreport(report):
    result = _TEST_RESULTS.setdefault(
        report.nodeid,
        {"nodeid": report.nodeid, "outcome": None, "duration": 0.0, "message": ""},
    )
    result["duration"] += report.duration

    if report.when == "call":
        result["outcome"] = report.outcome
    elif report.when == "setup" and report.outcome in {"failed", "skipped"}:
        result["outcome"] = report.outcome
    elif report.when == "teardown" and report.failed:
        result["outcome"] = "failed"

    if report.failed:
        result["message"] = report.longreprtext
    elif report.skipped and not result["message"]:
        result["message"] = str(report.longrepr)


def pytest_sessionfinish(session, exitstatus):
    elapsed = time.perf_counter() - _SESSION_STARTED_AT
    results = [result for result in _TEST_RESULTS.values() if result["outcome"]]
    summary = write_html_report(results, elapsed, Path("report") / "test_report.html")

    terminal = session.config.pluginmanager.get_plugin("terminalreporter")
    if terminal is not None:
        terminal.write_sep("=", "BÁO CÁO TỶ LỆ KIỂM THỬ")
        terminal.write_line(
            f"Pass: {summary['passed']}/{summary['total']} "
            f"({summary['pass_rate']:.2f}%) | Fail: {summary['failed']} | Skip: {summary['skipped']}"
        )
        terminal.write_line(f"HTML report: {summary['path']}")


@pytest.fixture
def action_delay():
    return float(os.getenv("ACTION_DELAY", "0.8"))


@pytest.fixture
def driver():
    options = Options()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    options.add_experimental_option("excludeSwitches", ["enable-automation"])

    if _is_truthy(os.getenv("HEADLESS", "0")):
        options.add_argument("--headless=new")
        options.add_argument("--window-size=1440,1000")

    browser = webdriver.Chrome(options=options)
    browser.set_page_load_timeout(30)
    yield browser

    close_delay = float(os.getenv("BROWSER_CLOSE_DELAY", "1.0"))
    if close_delay > 0:
        time.sleep(close_delay)
    browser.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    report = outcome.get_result()
    if report.when != "call" or not report.failed:
        return

    browser = item.funcargs.get("driver")
    if browser is None:
        return

    screenshot_dir = Path("artifacts") / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    browser.save_screenshot(str(screenshot_dir / f"{item.name}.png"))

