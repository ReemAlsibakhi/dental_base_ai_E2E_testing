"""pages/login_page.py — Page Object for the Login page (Keycloak SSO).

ROOT CAUSE DISCOVERED:
After Keycloak login, app redirects to:
  /login?access_token=eyJ...&refresh_token=eyJ...
React reads the tokens from URL, stores them, then redirects to /overview.
The wait_for_url("/overview") must wait for THIS final redirect.
"""

from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):

    _GET_STARTED_BUTTON = "button:has-text('Get started')"
    _EMAIL_INPUT        = '#username'
    _PASSWORD_INPUT     = '#password'
    _SUBMIT_BUTTON      = '#kc-login'
    _KEYCLOAK_HOST      = "keycloak-dev.dentalbase.ai"
    _POST_LOGIN_URL     = "/overview"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input    = page.locator(self._EMAIL_INPUT)
        self.password_input = page.locator(self._PASSWORD_INPUT)
        self.submit_button  = page.locator(self._SUBMIT_BUTTON)

    def goto(self) -> None:
        self.page.goto("/login", wait_until="commit", timeout=60_000)

    def login(self, email: str, password: str) -> None:
        # Wait for "Get started" button OR already on overview
        self.page.locator(self._GET_STARTED_BUTTON).wait_for(
            state="visible", timeout=30_000
        )

        # If already redirected to overview — done
        if self._POST_LOGIN_URL in self.page.url:
            return

        # Click "Get started" → Keycloak
        self.page.locator(self._GET_STARTED_BUTTON).click()

        # Wait for Keycloak #username field
        self.email_input.wait_for(state="visible", timeout=20_000)

        # Fill credentials
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def wait_for_successful_login(self) -> None:
        # After submit, app lands on /login?access_token=...
        # then React processes tokens and redirects to /overview
        # We wait for /overview to appear
        self.page.wait_for_url(
            f"**{self._POST_LOGIN_URL}**",
            timeout=30_000,
            wait_until="commit"
        )
