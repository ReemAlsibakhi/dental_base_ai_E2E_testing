"""
pages/login_page.py

PROFESSIONAL APPROACH: Login happens ONCE via UI, state saved to disk.
All subsequent tests load from disk — never touch the login page again.

The login_page.py is ONLY used by the session-scoped admin_auth_state
fixture in conftest.py. Tests never call login directly.
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
        Wait for spinner to resolve — then act based on where we land.
        Spinner resolves to ONE of two states:
          A) /overview URL  → already logged in, done
          B) "Get started"  → need to login via Keycloak
        We poll for either — no fixed assumptions.
        """
        end_time = time.time() + 60  # max 60s for spinner

        while time.time() < end_time:

            # State A: already on dashboard
            if self._POST_LOGIN_URL in self.page.url:
                return

            # State B: Get started button visible
            if self.page.locator(self._GET_STARTED_BUTTON).is_visible():
                self._do_keycloak_login(email, password)
                return

            time.sleep(0.3)

        raise RuntimeError(
            f"Login timed out after 60s.\n"
            f"Final URL: {self.page.url}\n"
            f"Expected either '/overview' or 'Get started' button."
        )

    def _do_keycloak_login(self, email: str, password: str) -> None:
        """Click Get started → fill Keycloak form → submit."""
        self.page.locator(self._GET_STARTED_BUTTON).click()
        self.email_input.wait_for(state="visible", timeout=20_000)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def wait_for_successful_login(self) -> None:
        """
        After submit, app goes to /login?access_token=...
        then React processes tokens and redirects to /overview.
        Wait up to 60s for that final redirect.
        """
        self.page.wait_for_url(
            f"**{self._POST_LOGIN_URL}**",
            timeout=60_000,
            wait_until="commit"
        )
