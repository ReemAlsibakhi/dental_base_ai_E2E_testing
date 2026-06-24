"""pages/login_page.py — Page Object for the Login page (Keycloak SSO)."""

from playwright.sync_api import Page
from pages.base_page import BasePage
import time


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
        # Poll URL in Python — works across domain redirects
        state = self._wait_for_state(timeout=20)

        if state == "overview":
            # Already logged in
            return

        if state == "keycloak":
            # App redirected straight to Keycloak
            self._fill_keycloak(email, password)
            return

        if state == "login":
            # On /login page — click Get started → goes to Keycloak
            self.page.locator(self._GET_STARTED_BUTTON).click()
            self._wait_for_state(expected="keycloak", timeout=15)
            self._fill_keycloak(email, password)
            return

        raise RuntimeError(f"Login: unknown state after 20s. URL={self.page.url}")

    def _wait_for_state(self, timeout: int = 20, expected: str = None) -> str:
        """
        Poll self.page.url every 500ms in Python.
        Returns: 'overview' | 'keycloak' | 'login'
        Works across domain redirects (no JS execution needed).
        """
        deadline = time.time() + timeout
        while time.time() < deadline:
            url = self.page.url
            if self._POST_LOGIN_URL_FRAGMENT in url:
                return "overview"
            if self._KEYCLOAK_HOST in url:
                return "keycloak"
            if "/login" in url or "Get started" in (self.page.title() or ""):
                if expected == "keycloak":
                    time.sleep(0.5)
                    continue
                return "login"
            time.sleep(0.5)

        return "unknown"

    def _fill_keycloak(self, email: str, password: str) -> None:
        """Fill and submit the Keycloak login form."""
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
