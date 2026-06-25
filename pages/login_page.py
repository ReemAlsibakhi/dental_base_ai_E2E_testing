"""pages/login_page.py — Page Object for the Login page (Keycloak SSO).

STRATEGY:
  Use wait_until='commit' (fastest possible — fires on first byte received).
  Then wait for a visible element that tells us which state we are in.
  This is resilient to slow SPAs and cross-domain redirects.
"""

from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):

    _GET_STARTED_BUTTON = 'button:has-text("Get started")'
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
        # 'commit' = fires as soon as HTTP response headers are received
        # Fastest possible — does NOT wait for JS/CSS/DOM to finish
        self.page.goto("/login", wait_until="commit", timeout=60_000)

    def login(self, email: str, password: str) -> None:
        # Wait for ANY visible element that tells us where we landed
        # This covers: spinner → Get started | direct Keycloak | already logged in
        self.page.wait_for_selector(
            ', '.join([
                'button:has-text("Get started")',  # session expired → show login btn
                '#username',                        # redirected to Keycloak
                'a[href="/overview"]',              # already logged in nav
                'text=Good',                        # dashboard greeting "Good Morning..."
            ]),
            timeout=60_000,
            state="attached"
        )

        url = self.page.url

        # Already on dashboard
        if self._POST_LOGIN_URL in url or "Good" in self.page.content():
            return

        # On Keycloak
        if self._KEYCLOAK_HOST in url or self.page.locator('#username').count() > 0:
            self._fill_keycloak(email, password)
            return

        # "Get started" button visible
        if self.page.locator(self._GET_STARTED_BUTTON).is_visible():
            self.page.locator(self._GET_STARTED_BUTTON).click()
            self.page.wait_for_selector('#username', timeout=20_000)
            self._fill_keycloak(email, password)
            return

        raise RuntimeError(f"Login: unknown state. URL={url}")

    def _fill_keycloak(self, email: str, password: str) -> None:
        self.email_input.wait_for(state="visible", timeout=10_000)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def wait_for_successful_login(self) -> None:
        self.page.wait_for_url(
            f"**{self._POST_LOGIN_URL}**",
            timeout=60_000,
            wait_until="commit"
        )
