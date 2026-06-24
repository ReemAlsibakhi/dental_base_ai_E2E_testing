"""pages/login_page.py — Page Object for the Login page (Keycloak SSO)."""

from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):

    _GET_STARTED_BUTTON      = 'button:has-text("Get started")'
    _EMAIL_INPUT             = '#username'
    _PASSWORD_INPUT          = '#password'
    _SUBMIT_BUTTON           = '#kc-login'
    _POST_LOGIN_URL_FRAGMENT = "/overview"
    _KEYCLOAK_URL_FRAGMENT   = "keycloak"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.get_started_button = page.locator(self._GET_STARTED_BUTTON)
        self.email_input        = page.locator(self._EMAIL_INPUT)
        self.password_input     = page.locator(self._PASSWORD_INPUT)
        self.submit_button      = page.locator(self._SUBMIT_BUTTON)

    def goto(self) -> None:
        self.page.goto("/login", wait_until="domcontentloaded")

    def login(self, email: str, password: str) -> None:
        # Already logged in — skip entirely
        if self._POST_LOGIN_URL_FRAGMENT in self.page.url:
            return

        # Click "Get started" and WAIT until Keycloak URL loads
        self.get_started_button.wait_for(state="visible", timeout=8_000)
        self.get_started_button.click()

        # Wait until we are ON Keycloak (URL contains "keycloak")
        self.page.wait_for_url(
            f"**{self._KEYCLOAK_URL_FRAGMENT}**",
            timeout=15_000,
            wait_until="domcontentloaded"
        )

        # Now fill credentials
        self.email_input.wait_for(state="visible", timeout=10_000)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def wait_for_successful_login(self) -> None:
        self.page.wait_for_url(
            f"**{self._POST_LOGIN_URL_FRAGMENT}**",
            timeout=20_000,
            wait_until="domcontentloaded"
        )
