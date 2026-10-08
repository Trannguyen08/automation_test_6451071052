import os
import platform
import time
from pathlib import Path

import allure
import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from src.pages.login_page import LoginPage


def _is_truthy(value):
    return str(value).strip().lower() in {"1", "true", "yes", "on"}


@pytest.hookimpl(trylast=True)
def pytest_sessionfinish(session, exitstatus):
    allure_results = Path("report") / "allure-results"
    allure_results.mkdir(parents=True, exist_ok=True)
    (allure_results / "environment.properties").write_text(
        "\n".join(
            (
                "Application=Văn phòng điện tử UTC",
                f"Base.URL={LoginPage.URL}",
                "Browser=Chrome",
                f"Python={platform.python_version()}",
                f"Operating.System={platform.platform()}",
            )
        ),
        encoding="utf-8",
    )


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

    screenshot = browser.get_screenshot_as_png()
    allure.attach(
        screenshot,
        name=f"{item.name}-failure",
        attachment_type=allure.attachment_type.PNG,
    )

    screenshot_dir = Path("artifacts") / "screenshots"
    screenshot_dir.mkdir(parents=True, exist_ok=True)
    (screenshot_dir / f"{item.name}.png").write_bytes(screenshot)

