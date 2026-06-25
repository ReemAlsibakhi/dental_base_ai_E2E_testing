"""
pages/login_page.py

The app uses CSRF state parameter — must go through /login to get it.
/login spinner can take up to 90s in slow environments.
Solution: wait up to 120s for either 'Get started' or '/overview'.
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
        Wait up to 120s for spinner to finish.
        Spinner resolves to either:
          A) /overview  → already logged in
          B) 'Get started' button → do Keycloak login
        """
        end_time = time.time() + 120

        while time.time() < end_time:
            if self._POST_LOGIN_URL in self.page.url:
                return

            if self.page.locator(self._GET_STARTED_BUTTON).is_visible():
                self.page.locator(self._GET_STARTED_BUTTON).click()
                # Wait for Keycloak — it provides the state param
                self.email_input.wait_for(state="visible", timeout=20_000)
                self.email_input.fill(email)
                self.password_input.fill(password)
                self.submit_button.click()
                return

            time.sleep(0.5)

        raise RuntimeError(
            f"Login spinner did not resolve after 120s.\n"
            f"URL: {self.page.url}"
        )

    def wait_for_successful_login(self) -> None:
        self.page.wait_for_url(
            f"**{self._POST_LOGIN_URL}**",
            timeout=60_000,
            wait_until="commit"
        )
