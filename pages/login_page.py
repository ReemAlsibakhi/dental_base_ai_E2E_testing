"""
pages/login_page.py

STRATEGY:
  /login shows a spinner while React checks the session.
  We poll every 300ms for up to 60s for EITHER:
    A) URL contains /overview  → already logged in
    B) "Get started" button visible → need to login

  This handles both cases without any timeout issues.
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
        Poll for one of two states — no fixed timeouts on individual elements.
        Works regardless of how long the spinner takes.
        """
        end = time.time() + 60

        while time.time() < end:

            # Case A: already logged in (session still valid)
            if self._POST_LOGIN_URL in self.page.url:
                return

            # Case B: "Get started" button appeared (spinner finished)
            try:
                btn = self.page.locator(self._GET_STARTED_BUTTON).first
                if btn.is_visible(timeout=500):
                    btn.click()
                    # Wait for Keycloak
                    self.email_input.wait_for(state="visible", timeout=20_000)
                    self.email_input.fill(email)
                    self.password_input.fill(password)
                    self.submit_button.click()
                    return
            except Exception:
                pass

            time.sleep(0.3)

        raise RuntimeError(
            f"Login: neither /overview nor 'Get started' appeared in 60s.\n"
            f"URL: {self.page.url}"
        )

    def wait_for_successful_login(self) -> None:
        """Wait for React to process tokens and land on /overview."""
        self.page.wait_for_url(
            f"**{self._POST_LOGIN_URL}**",
            timeout=60_000,
            wait_until="commit"
        )
