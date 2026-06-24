"""pages/login_page.py — Page Object for the Login page (Keycloak SSO).

STRATEGY: Go directly to /login and immediately wait for any of 3 states:
  1. Already on /overview  → already logged in, skip
  2. Redirect to Keycloak  → fill credentials
  3. Shows "Get started"   → click it, then fill credentials

No fixed sleeps. No guessing. Pure event-driven waiting.
"""

from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):

    _GET_STARTED_BUTTON      = 'button:has-text("Get started")'
    _EMAIL_INPUT             = '#username'
    _PASSWORD_INPUT          = '#password'
    _SUBMIT_BUTTON           = '#kc-login'
    _KEYCLOAK_HOST           = "keycloak-dev.dentalbase.ai"
    _POST_LOGIN_URL_FRAGMENT = "/overview"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input    = page.locator(self._EMAIL_INPUT)
        self.password_input = page.locator(self._PASSWORD_INPUT)
        self.submit_button  = page.locator(self._SUBMIT_BUTTON)

    def goto(self) -> None:
        self.page.goto("/login", wait_until="domcontentloaded")

    def login(self, email: str, password: str) -> None:
        """
        Wait for whichever state appears first — no fixed timeouts on steps.
        Uses Playwright's expect_one_of pattern via wait_for_function.
        """
        # Wait until URL is one of: overview, keycloak, or /login with button
        self.page.wait_for_function(
            """() => {
                const url = window.location.href;
                if (url.includes('overview')) return 'overview';
                if (url.includes('keycloak')) return 'keycloak';
                const btn = document.querySelector('button');
                if (btn && btn.innerText.includes('Get started')) return 'login';
                return false;
            }""",
            timeout=20_000
        )

        current_url = self.page.url

        # Already logged in
        if self._POST_LOGIN_URL_FRAGMENT in current_url:
            return

        # On Keycloak directly (app auto-redirected)
        if self._KEYCLOAK_HOST in current_url:
            self._fill_keycloak(email, password)
            return

        # On /login with "Get started" button
        self.page.locator(self._GET_STARTED_BUTTON).click()
        self.page.wait_for_url(f"**{self._KEYCLOAK_HOST}**", timeout=15_000)
        self._fill_keycloak(email, password)

    def _fill_keycloak(self, email: str, password: str) -> None:
        self.email_input.wait_for(state="visible", timeout=10_000)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def wait_for_successful_login(self) -> None:
        self.page.wait_for_url(
            f"**{self._POST_LOGIN_URL_FRAGMENT}**",
            timeout=25_000,
            wait_until="domcontentloaded"
        )
