import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


class LoginPage:
    URL = "https://vanphongdientu.utc.edu.vn/Login"

    USERNAME = (By.NAME, "username")
    PASSWORD = (By.NAME, "userpwd")
    REMEMBER = (By.ID, "persistent")
    UTC_EMAIL_LOGIN = (By.CSS_SELECTOR, "a.button")
    SUBMIT = (By.CSS_SELECTOR, "input.submit_login")
    FORGOT_PASSWORD = (By.CSS_SELECTOR, ".helps a[href='/Login/GetPass']")
    REMEMBER_LABEL = (By.CSS_SELECTOR, "label.check[for='persistent']")

    def __init__(self, driver, action_delay=0.8, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
        self.action_delay = action_delay

    def open(self):
        self.driver.get(self.URL)
        self.wait.until(EC.visibility_of_element_located(self.USERNAME))
        self._pause()
        return self

    def element(self, locator):
        return self.wait.until(EC.presence_of_element_located(locator))

    def visible_element(self, locator):
        return self.wait.until(EC.visibility_of_element_located(locator))

    def fill_credentials(self, username="", password=""):
        username_input = self.visible_element(self.USERNAME)
        password_input = self.visible_element(self.PASSWORD)
        username_input.clear()
        password_input.clear()
        if username:
            username_input.send_keys(username)
        if password:
            password_input.send_keys(password)
        self._pause()

    def submit(self):
        self.visible_element(self.SUBMIT).click()
        self._pause()

    def login(self, username="", password=""):
        self.fill_credentials(username, password)
        self.submit()

    def login_with_enter(self, username="", password=""):
        self.fill_credentials(username, password)
        self.element(self.PASSWORD).send_keys(Keys.ENTER)
        self._pause()

    def select_remember_me(self):
        checkbox = self.element(self.REMEMBER)
        if not checkbox.is_selected():
            self.visible_element(self.REMEMBER_LABEL).click()
            self._pause()
        assert checkbox.is_selected()

    def open_forgot_password(self):
        self.visible_element(self.FORGOT_PASSWORD).click()
        self.wait.until(EC.url_contains("/Login/GetPass"))
        self._pause()

    def open_utc_email_login(self):
        self.visible_element(self.UTC_EMAIL_LOGIN).click()
        self.wait.until(EC.url_contains("accounts.google.com"))
        self._pause()

    def wait_for_login_success(self):
        self.wait.until(lambda driver: "/login" not in driver.current_url.lower())
        self._pause()

    def wait_for_text(self, expected_text):
        self.wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), expected_text))

    def assert_form_is_displayed(self):
        visible_locators = (
            self.USERNAME,
            self.PASSWORD,
            self.UTC_EMAIL_LOGIN,
            self.SUBMIT,
            self.FORGOT_PASSWORD,
        )
        for locator in visible_locators:
            assert self.visible_element(locator).is_displayed()
        assert self.element(self.REMEMBER).is_enabled()
        assert "Đăng nhập" in self.driver.title

    def assert_password_is_masked(self, password):
        self.fill_credentials(password=password)
        password_input = self.element(self.PASSWORD)
        assert password_input.get_attribute("type") == "password"
        assert password_input.get_attribute("value") == password

    def _pause(self):
        if self.action_delay > 0:
            time.sleep(self.action_delay)

