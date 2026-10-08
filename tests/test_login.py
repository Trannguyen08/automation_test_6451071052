import json
import os

import allure
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
@allure.epic("Văn phòng điện tử UTC")
@allure.feature("Đăng nhập")
@allure.story("Xác thực người dùng")
def test_login_module(driver, action_delay, test_case):
    test_id = str(test_case["test_id"])
    title = str(test_case["title"])
    action = test_case["action"]
    safe_test_data = dict(test_case)
    if safe_test_data.get("password"):
        safe_test_data["password"] = "******"

    allure.dynamic.title(f"{test_id} - {title}")
    allure.dynamic.description(f"Kiểm thử module đăng nhập: {title}")
    allure.dynamic.tag("login", "selenium", "data-driven")
    allure.dynamic.label("testCaseId", test_id)
    allure.dynamic.severity(_severity_for(action))
    allure.dynamic.parameter(
        "test_case",
        json.dumps(safe_test_data, ensure_ascii=False),
    )

    with allure.step("Mở trang đăng nhập UTC"):
        page = LoginPage(driver, action_delay=action_delay).open()

    if action == "verify_form":
        with allure.step("Kiểm tra các thành phần của form đăng nhập"):
            page.assert_form_is_displayed()
    elif action == "verify_password_mask":
        with allure.step("Nhập và kiểm tra trường mật khẩu được che"):
            page.assert_password_is_masked(str(test_case["password"]))
    elif action == "submit_login":
        _submit_and_assert_message(page, driver, test_case)
    elif action == "valid_login":
        username = os.getenv("UTC_USERNAME")
        password = os.getenv("UTC_PASSWORD")
        if not username or not password:
            pytest.skip("Cần khai báo UTC_USERNAME và UTC_PASSWORD để chạy ca đăng nhập hợp lệ")
        with allure.step("Đăng nhập bằng tài khoản hợp lệ từ biến môi trường"):
            page.login(username, password)
            page.wait_for_login_success()
    elif action == "submit_with_enter":
        with allure.step("Nhập thông tin và nhấn Enter tại trường mật khẩu"):
            page.login_with_enter(str(test_case["username"]), str(test_case["password"]))
        _assert_expected_message(page, driver, test_case)
    elif action == "toggle_remember":
        with allure.step("Chọn 'Giữ tôi luôn đăng nhập'"):
            page.select_remember_me()
    elif action == "forgot_password":
        with allure.step("Mở trang lấy lại mật khẩu"):
            page.open_forgot_password()
            assert str(test_case["expected_text"]) in driver.current_url
    elif action == "utc_sso":
        with allure.step("Chuyển tới hệ thống đăng nhập e-mail UTC"):
            page.open_utc_email_login()
            assert str(test_case["expected_text"]) in driver.current_url
    else:
        pytest.fail(f"Action không được hỗ trợ trong Excel: {action}")


def _submit_and_assert_message(page, driver, test_case):
    with allure.step("Nhập dữ liệu và nhấn nút Đăng nhập"):
        page.login(str(test_case["username"]), str(test_case["password"]))
    _assert_expected_message(page, driver, test_case)


def _assert_expected_message(page, driver, test_case):
    expected_text = str(test_case["expected_text"])
    with allure.step(f"Kiểm tra thông báo: {expected_text}"):
        page.wait_for_text(expected_text)
        assert expected_text in driver.find_element(By.TAG_NAME, "body").text


def _severity_for(action):
    if action in {"valid_login", "submit_login", "submit_with_enter"}:
        return allure.severity_level.CRITICAL
    if action in {"forgot_password", "utc_sso"}:
        return allure.severity_level.NORMAL
    return allure.severity_level.MINOR

