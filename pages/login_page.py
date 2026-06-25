"""pages/login_page.py — Page Object for the Login page (Keycloak SSO).

REAL BEHAVIOUR (confirmed via debug):
  - Fresh browser:  /login → spinner → "Get started" → Keycloak → /login?token → /overview
  - Active session: /login → spinner → redirect directly to /overview (no "Get started")

SOLUTION: wait for EITHER "Get started" OR "/overview" — whichever comes first.
"""

import time
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
        """
        Wait for EITHER:
          A) Already on /overview  → session active, skip login
          B) "Get started" visible → fresh session, do full login
        """
        # Poll every 500ms for up to 30s — works across both scenarios
        deadline = time.time() + 30
        while time.time() < deadline:
            # Case A: already logged in
            if self._POST_LOGIN_URL in self.page.url:
                return

            # Case B: "Get started" button appeared
            btn = self.page.locator(self._GET_STARTED_BUTTON)
            if btn.is_visible():
                btn.click()
                # Wait for Keycloak
                self.email_input.wait_for(state="visible", timeout=20_000)
                self.email_input.fill(email)
                self.password_input.fill(password)
                self.submit_button.click()
                return

            time.sleep(0.5)

        raise RuntimeError(
            f"Login: neither '/overview' nor 'Get started' appeared in 30s.\n"
            f"URL={self.page.url}"
        )

    def wait_for_successful_login(self) -> None:
        """Wait for React to process tokens and redirect to /overview."""
        self.page.wait_for_url(
            f"**{self._POST_LOGIN_URL}**",
            timeout=30_000,
            wait_until="commit"
        )
