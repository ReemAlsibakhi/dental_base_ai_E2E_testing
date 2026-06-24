"""pages/login_page.py — Page Object for the Login page (Keycloak SSO).

STRATEGY:
  /login shows a spinner while React checks the session.
  After spinner, app either:
    A) Redirects to /overview (already logged in)
    B) Redirects to Keycloak (needs login)
    C) Shows "Get started" button (rare)

  We wait for the spinner to disappear FIRST, then act.
"""

from playwright.sync_api import Page
from pages.base_page import BasePage
import time


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
        # Step 1: Wait for spinner to disappear + URL to change from /login
        # The spinner means React is still checking session — don't act yet
        self._wait_until_redirected(timeout=30)

        url = self.page.url

        # Case A: Already logged in
        if self._POST_LOGIN_URL in url:
            return

        # Case B: Redirected to Keycloak
        if self._KEYCLOAK_HOST in url:
            self._fill_keycloak(email, password)
            return

        # Case C: Still on /login with "Get started" button
        if self.page.locator(self._GET_STARTED_BUTTON).is_visible():
            self.page.locator(self._GET_STARTED_BUTTON).click()
            self._poll_for_keycloak(timeout=15)
            self._fill_keycloak(email, password)
            return

        raise RuntimeError(f"Login: unexpected state. URL={url}")

    def _wait_until_redirected(self, timeout: int = 30) -> None:
        """
        Poll until URL is no longer /login (spinner finished + redirect happened).
        The spinner on /login means the app is still deciding where to send us.
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            url = self.page.url
            # Left /login — redirect happened
            if "/login" not in url:
                return
            # Still on /login but "Get started" button appeared — spinner done
            if self.page.locator(self._GET_STARTED_BUTTON).is_visible():
                return
            time.sleep(0.5)

        raise RuntimeError(
            f"Login: spinner never resolved after {timeout}s. URL={self.page.url}"
        )

    def _poll_for_keycloak(self, timeout: int = 15) -> None:
        """Poll until we land on Keycloak."""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self._KEYCLOAK_HOST in self.page.url:
                return
            time.sleep(0.5)
        raise RuntimeError(f"Login: never reached Keycloak. URL={self.page.url}")

    def _fill_keycloak(self, email: str, password: str) -> None:
        """Fill and submit Keycloak credentials."""
        self.email_input.wait_for(state="visible", timeout=10_000)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def wait_for_successful_login(self) -> None:
        self.page.wait_for_url(
            f"**{self._POST_LOGIN_URL}**",
            timeout=25_000,
            wait_until="domcontentloaded"
        )
