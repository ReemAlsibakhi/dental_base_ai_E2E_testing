"""pages/login_page.py — Page Object for the Login page."""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):
    # ------------------------------------------------------------------
    # TODO: Replace these selector strings with the real ones from the
    # live DOM.  Use `playwright codegen` or browser DevTools.
    # ------------------------------------------------------------------

    # TODO: Confirm selector — e.g. page.get_by_label("Email") or
    #       page.locator('[data-testid="email-input"]')
    _EMAIL_INPUT = '[data-testid="email-input"]'          # TODO

    # TODO: Confirm selector
    _PASSWORD_INPUT = '[data-testid="password-input"]'    # TODO

    # TODO: Confirm selector
    _SUBMIT_BUTTON = '[data-testid="login-submit"]'       # TODO

    # TODO: URL path or partial match that confirms a successful login
    _POST_LOGIN_URL_FRAGMENT = "/dashboard"               # TODO

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input = page.locator(self._EMAIL_INPUT)
        self.password_input = page.locator(self._PASSWORD_INPUT)
        self.submit_button = page.locator(self._SUBMIT_BUTTON)

    def goto(self) -> None:
        self.page.goto("/login")

    def login(self, email: str, password: str) -> None:
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def wait_for_successful_login(self) -> None:
        self.page.wait_for_url(f"**{self._POST_LOGIN_URL_FRAGMENT}**")
