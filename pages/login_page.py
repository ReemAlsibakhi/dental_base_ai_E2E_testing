"""pages/login_page.py — Page Object for the Login page (Keycloak SSO)."""

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
        # Use Playwright's first() with or_() to wait for any of the states
        # This is the correct API for "wait for one of multiple locators"
        self.page.locator("#username").or_(
            self.page.locator("button:has-text('Get started')")
        ).or_(
            self.page.get_by_text("Good Afternoon", exact=False)
        ).or_(
            self.page.get_by_text("Good Morning", exact=False)
        ).or_(
            self.page.get_by_text("Good Evening", exact=False)
        ).first.wait_for(state="attached", timeout=60_000)

        url = self.page.url

        # Case 1: Already on dashboard
        if self._POST_LOGIN_URL in url:
            return

        # Case 2: On Keycloak — #username visible
        if self._KEYCLOAK_HOST in url or self.page.locator('#username').count() > 0:
            self._fill_keycloak(email, password)
            return

        # Case 3: "Get started" button visible — click → Keycloak
        if self.page.locator(self._GET_STARTED_BUTTON).is_visible():
            self.page.locator(self._GET_STARTED_BUTTON).click()
            self.page.locator('#username').wait_for(state="visible", timeout=20_000)
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
