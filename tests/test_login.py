import pytest
from selenium.webdriver.common.by import By

from src.pages.login_page import LoginPage
from src.utils.excel_reader import load_login_test_cases


TEST_CASES = load_login_test_cases()


@pytest.mark.parametrize(
    "test_case",
    TEST_CASES,
    ids=[test_case["test_id"] for test_case in TEST_CASES],
)
def test_login_module(driver, action_delay, test_case):
    page = LoginPage(driver, action_delay=action_delay).open()
    action = test_case["action"]

    if action == "verify_form":
        page.assert_form_is_displayed()
    elif action == "verify_password_mask":
        page.assert_password_is_masked(str(test_case["password"]))
    elif action == "submit_login":
        page.login(str(test_case["username"]), str(test_case["password"]))
        page.wait_for_text(str(test_case["expected_text"]))
        assert str(test_case["expected_text"]) in driver.find_element(By.TAG_NAME, "body").text
    else:
        pytest.fail(f"Action không được hỗ trợ trong Excel: {action}")

