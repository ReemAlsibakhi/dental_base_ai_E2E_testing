"""pages/login_page.py — Page Object for the Login page (Keycloak SSO).

STRATEGY:
  /login shows a spinner (React checks session token with backend).
  We wait for ANY of these to appear — whichever comes first:
    - 'Get started' button  → click it → Keycloak
    - Keycloak URL          → fill credentials directly
    - /overview URL         → already logged in
"""

from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):

    _GET_STARTED_BUTTON  = 'button:has-text("Get started")'
    _EMAIL_INPUT         = '#username'
    _PASSWORD_INPUT      = '#password'
    _SUBMIT_BUTTON       = '#kc-login'
    _KEYCLOAK_HOST       = "keycloak-dev.dentalbase.ai"
    _POST_LOGIN_URL      = "/overview"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input    = page.locator(self._EMAIL_INPUT)
        self.password_input = page.locator(self._PASSWORD_INPUT)
        self.submit_button  = page.locator(self._SUBMIT_BUTTON)

    def goto(self) -> None:
        self.page.goto("/login", wait_until="domcontentloaded")

    def login(self, email: str, password: str) -> None:
        # Wait for ANY of the 3 possible states — whichever comes first
        # This handles: slow spinner, fast redirect, already logged in
        self.page.wait_for_selector(
            f'button:has-text("Get started"), #username, [data-url*="overview"]',
            timeout=60_000,
            state="attached"
        )

        url = self.page.url

        # Case 1: Already on /overview
        if self._POST_LOGIN_URL in url:
            return

        # Case 2: Redirected to Keycloak
        if self._KEYCLOAK_HOST in url:
            self._fill_keycloak(email, password)
            return

        # Case 3: "Get started" button appeared
        btn = self.page.locator(self._GET_STARTED_BUTTON)
        if btn.is_visible():
            btn.click()
            # Wait for Keycloak to load
            self.page.wait_for_selector('#username', timeout=20_000)
            self._fill_keycloak(email, password)
            return

        # Case 4: #username appeared directly (Keycloak loaded without URL change detection)
        if self.page.locator('#username').is_visible():
            self._fill_keycloak(email, password)
            return

        raise RuntimeError(f"Login: unexpected state. URL={self.page.url}")

    def _fill_keycloak(self, email: str, password: str) -> None:
        """Fill and submit Keycloak credentials."""
        self.email_input.wait_for(state="visible", timeout=10_000)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def wait_for_successful_login(self) -> None:
        self.page.wait_for_url(
            f"**{self._POST_LOGIN_URL}**",
            timeout=30_000,
            wait_until="domcontentloaded"
        )
