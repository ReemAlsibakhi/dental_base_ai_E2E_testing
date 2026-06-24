"""pages/login_page.py — Page Object for the Login page (Keycloak SSO)."""

from playwright.sync_api import Page, expect
from pages.base_page import BasePage


class LoginPage(BasePage):

    # Landing page CTA
    _GET_STARTED_BUTTON = 'button:has-text("Get started")'

    # Keycloak form
    _EMAIL_INPUT    = '#username'
    _PASSWORD_INPUT = '#password'
    _SUBMIT_BUTTON  = '#kc-login'

    # Post-login URL
    _POST_LOGIN_URL_FRAGMENT = "/overview"

    def __init__(self, page: Page) -> None:
        super().__init__(page)
        self.get_started_button = page.locator(self._GET_STARTED_BUTTON)
        self.email_input        = page.locator(self._EMAIL_INPUT)
        self.password_input     = page.locator(self._PASSWORD_INPUT)
        self.submit_button      = page.locator(self._SUBMIT_BUTTON)

    def goto(self) -> None:
        self.page.goto("/login")
        self.page.wait_for_load_state("networkidle")

    def login(self, email: str, password: str) -> None:
        # إذا كان already logged in يوديه لـ /overview مباشرة
        if "/overview" in self.page.url or "/settings" in self.page.url:
            return

        # إذا ظهر زر "Get started" اضغطه
        try:
            self.get_started_button.wait_for(timeout=5_000)
            self.get_started_button.click()
            self.page.wait_for_load_state("networkidle")
        except Exception:
            pass  # ربما وصل مباشرة لـ Keycloak

        # Keycloak form
        self.email_input.wait_for(timeout=10_000)
        self.email_input.fill(email)
        self.password_input.fill(password)
        self.submit_button.click()

    def wait_for_successful_login(self) -> None:
        self.page.wait_for_url(f"**{self._POST_LOGIN_URL_FRAGMENT}**", timeout=15_000)
