"""pages/login_page.py — Page Object for the Login page (Keycloak SSO)."""

from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):

    _GET_STARTED_BUTTON = "button:has-text('Get started')"  # single quotes inside
    _EMAIL_INPUT        = '#username'
    _PASSWORD_INPUT     = '#password'
    _SUBMIT_BUTTON      = '#kc-login'
    _KEYCLOAK_HOST      = "keycloak-dev.dentalbase.ai"
    _POST_LOGIN_URL     = "/overview"

    # Multi-selector — wait for whichever appears first
    # Uses single quotes inside to avoid nested double-quote issue
    _ANY_STATE_SELECTOR = ", ".join([
        "button:has-text('Get started')",   # session expired → show login btn
        "#username",                         # redirected to Keycloak
        "text=Good Afternoon",               # dashboard greeting
        "text=Good Morning",                 # dashboard greeting
        "text=Good Evening",                 # dashboard greeting
    ])

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input    = page.locator(self._EMAIL_INPUT)
        self.password_input = page.locator(self._PASSWORD_INPUT)
        self.submit_button  = page.locator(self._SUBMIT_BUTTON)

    def goto(self) -> None:
        self.page.goto("/login", wait_until="commit", timeout=60_000)

    def login(self, email: str, password: str) -> None:
        # Wait for ANY visible element that tells us which state we are in
        self.page.wait_for_selector(
            self._ANY_STATE_SELECTOR,
            timeout=60_000,
            state="attached"
        )

        url = self.page.url

        # Case 1: Already on dashboard
        if self._POST_LOGIN_URL in url:
            return

        # Case 2: On Keycloak
        if self._KEYCLOAK_HOST in url:
            self._fill_keycloak(email, password)
            return

        # Case 3: "Get started" button visible
        btn = self.page.locator(self._GET_STARTED_BUTTON)
        if btn.is_visible():
            btn.click()
            self.page.wait_for_selector('#username', timeout=20_000)
            self._fill_keycloak(email, password)
            return

        # Case 4: #username appeared directly
        if self.page.locator('#username').count() > 0:
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
