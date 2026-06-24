"""pages/login_page.py — Page Object for the Login page (Keycloak SSO)."""

from playwright.sync_api import Page
from pages.base_page import BasePage


class LoginPage(BasePage):

    _GET_STARTED_BUTTON      = 'button:has-text("Get started")'
    _EMAIL_INPUT             = '#username'
    _PASSWORD_INPUT          = '#password'
    _SUBMIT_BUTTON           = '#kc-login'
    _POST_LOGIN_URL_FRAGMENT = "/overview"
    _KEYCLOAK_URL_FRAGMENT   = "keycloak"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.email_input   = page.locator(self._EMAIL_INPUT)
        self.password_input = page.locator(self._PASSWORD_INPUT)
        self.submit_button  = page.locator(self._SUBMIT_BUTTON)

    def goto(self) -> None:
        self.page.goto("/login", wait_until="domcontentloaded")
        # Wait for page to settle — could redirect to /overview or stay on /login
        self.page.wait_for_timeout(3000)

    def login(self, email: str, password: str) -> None:

        # Case 1: Already logged in — redirected to /overview
        if self._POST_LOGIN_URL_FRAGMENT in self.page.url:
            print(f"[Login] Already logged in → {self.page.url}")
            return

        # Case 2: Already on Keycloak (rare — previous redirect)
        if self._KEYCLOAK_URL_FRAGMENT in self.page.url:
            print("[Login] Already on Keycloak — filling credentials...")
            self._fill_keycloak(email, password)
            return

        # Case 3: On /login — look for "Get started" button
        get_started = self.page.locator(self._GET_STARTED_BUTTON)
        try:
            get_started.wait_for(state="visible", timeout=5_000)
            print("[Login] Clicking 'Get started'...")
            get_started.click()
            # Wait until Keycloak URL appears
            self.page.wait_for_url(
                f"**{self._KEYCLOAK_URL_FRAGMENT}**",
                timeout=15_000,
                wait_until="domcontentloaded"
            )
            print(f"[Login] On Keycloak → {self.page.url}")
            self._fill_keycloak(email, password)

        except Exception as e:
            # "Get started" not found — check where we are
            print(f"[Login] 'Get started' not found. URL={self.page.url}. Error={e}")
            if self._POST_LOGIN_URL_FRAGMENT in self.page.url:
                print("[Login] Actually already logged in — skip.")
                return
            raise RuntimeError(
                f"Login failed: could not find 'Get started' button.\n"
                f"Current URL: {self.page.url}\n"
                f"Original error: {e}"
            )

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
        print(f"[Login] Successfully landed on: {self.page.url}")
